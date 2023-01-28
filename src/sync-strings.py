#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from compare_locales import paths
import os
import shutil
import sys


def getAllFilesToml(toml_path, search_path):
    """
    Extract a list of all files referenced in the project configuration file
    (TOML). Files are stored with path relative to `search_path`.
    """

    basedir = os.path.dirname(toml_path)
    project_config = paths.TOMLParser().parse(toml_path, env={"l10n_base": ""})
    basedir = os.path.join(basedir, project_config.root)

    print(f"Analyzing files in {toml_path}")
    toml_files = []

    files = paths.ProjectFiles(None, [project_config])
    for l10n_file, reference_file, _, _ in files:
        toml_files.append(os.path.relpath(reference_file, search_path))

    for locale in project_config.all_locales:
        files = paths.ProjectFiles(locale, [project_config])
        for l10n_file, reference_file, _, _ in files:
            # Ignore missing files for locale
            if not os.path.exists(l10n_file):
                continue

            # Ignore file is the reference is missing
            if not os.path.exists(reference_file):
                continue

            toml_files.append(os.path.relpath(l10n_file, search_path))
    toml_files.sort()

    return toml_files


def main():
    src_repo_path = os.environ.get("INPUT_SRC")
    if src_repo_path is None:
        sys.exit("Empty 'src' parameter. Exiting.")
    if not os.path.isdir(src_repo_path):
        sys.exit("Could not find the src repo. Exiting.")

    dest_repo_path = os.environ.get("INPUT_DEST")
    if dest_repo_path is None:
        sys.exit("Empty 'dest' parameter. Exiting.")
    if not os.path.isdir(dest_repo_path):
        sys.exit("Could not find the dest repo. Exiting.")

    toml_path = os.environ.get("INPUT_TOML_PATH")
    if toml_path is None:
        sys.exit("Empty 'toml_path' parameter. Exiting.")
    toml_path = os.path.join(src_repo_path, os.environ.get("INPUT_TOML_PATH"))
    if not os.path.isfile(toml_path):
        sys.exit("File defined in 'toml_path' does not exist. Exiting.")

    # Get a list of all files referenced in the TOML file in the src folder
    filenames = getAllFilesToml(toml_path, src_repo_path)

    # Copy files from src to dest
    if filenames:
        for filename in filenames:
            print(f"- {filename}.")

            src_file = os.path.join(src_repo_path, filename)
            dest_file = os.path.join(dest_repo_path, filename)

            # Make sure that the folder exists, then copy file as is
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy(src_file, dest_file)
    else:
        print("No files copied.")


if __name__ == "__main__":
    main()
