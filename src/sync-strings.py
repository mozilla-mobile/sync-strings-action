#!/usr/bin/env python


# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


import datetime, filecmp, glob, os, pathlib, re, shutil, sys, tempfile
import git, tomlkit


def ts():
    return str(datetime.datetime.now())


def log(s):
    print(f"{ts()} {s}")


def android_locale(locale):
    """Convert the given Pontoon locale to the code Android uses"""
    ANDROID_COMPATIBILITY_MAPPINGS = {"he": "iw", "yi": "ji", "id": "in"}
    if locale in ANDROID_COMPATIBILITY_MAPPINGS:
        return ANDROID_COMPATIBILITY_MAPPINGS[locale]
    if matches := re.match(r"([a-z]+)-([A-Z]+)", locale):
        return f"{matches.group(1)}-r{matches.group(2)}"
    return locale


def release_locales(repo_path):
    """Load the list of locales from l10n-release.toml or from l10n.toml as fallback."""
    for filename in ("l10n-release.toml", "l10n.toml"):
        toml_path = os.path.join(repo_path, filename)
        if os.path.exists(toml_path):
            with open(toml_path) as toml_fp:
                l10n_toml = tomlkit.loads(toml_fp.read())
                log(f"Returning strings from {toml_path}")
                return l10n_toml["locales"]
        

def all_strings_xml_paths(repo_path, locales):
    """Yield all combinations of strings.xml paths and locales. Returns a relative path."""
    with open(os.path.join(repo_path, "l10n.toml")) as main_toml_fp:
        main_l10n_toml = tomlkit.loads(main_toml_fp.read())
        for locale in main_l10n_toml["locales"]:
            pathname = main_l10n_toml["paths"][0]["l10n"].replace("{android_locale}", android_locale(locale))
            for strings_xml_path in glob.glob(os.path.join(repo_path, pathname), recursive=True):
                yield os.path.relpath(strings_xml_path, repo_path)


def inspect_path(p):
    parts = p.split("/")
    for i in range(1, len(parts)):
        path = "./" + "/".join(parts[1:i+1])
        os.system("ls -ld " + path)



if __name__ == "__main__":

    src_repo_path = os.environ.get("INPUT_SRC")
    if src_repo_path is None:
        log("Empty INPUT_SRC. Exiting.")
        sys.exit(1)

    if not os.path.exists(src_repo_path):
        log("Could not find the src repo. Exiting.")
        sys.exit(1)

    src_repo = git.Repo(src_repo_path)

    dst_repo_path = os.environ.get("INPUT_DST")
    if dst_repo_path is None:
        log("Empty INPUT_DST. Exiting.")
        sys.exit(1)

    if not os.path.exists(dst_repo_path):
        log("Could not find the dst repo. Exiting.")
        sys.exit(1)

    dst_repo = git.Repo(dst_repo_path)

    # Take the list of locales to sync from the destination repository
    locales = release_locales(dst_repo_path)
    if not locales:
        log("Could not determine locales to sync. Exiting.")
        sys.exit(1)

    for path in all_strings_xml_paths(src_repo_path, locales):
        try:
            src = os.path.join(src_repo_path, path)
            dst = os.path.join(dst_repo_path, path)
            if not os.path.exists(dst) or not filecmp.cmp(src, dst):
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    log(f"Creating {dst_dir}")
                    pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)
                log(f"Copying {src} to {dst}")
                shutil.copyfile(src, dst)
                dst_repo.git.add(path)
                dst_repo.index.commit(f"Strings - {path}")
        except Exception as e:
            log(f"Could not update {path}: {e}")
