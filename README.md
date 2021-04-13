# Sync Strings GitHub Action

This GitHub Action syncs strings between two checked out copies of an Android project. It requires that these projects have a a `l10n.toml` and optionally an `l10n-release.toml` file in their root.

Example usage in a _GitHub Workflow_ file:

```
      - name: "Checkout Master Branch"
        uses: actions/checkout@v2
        with:
          path: main
          ref: master
      - name: "Checkout Beta Branch"
        uses: actions/checkout@v2
        with:
          path: beta
          ref: releases_v88.0.0
          
      - name: "Sync Strings"
        uses: st3fan/sync-strings-action@main
        with:
          src: main
          dst: beta

```

This action will `git add` and `git commit` the individual `strings.xml` files that are now or have changed. It will only do this in the working copy though - it will not create a PR or push these changes back. That can be the responsibility of another _Workflow Step_.

See also the `sync-strings.yml` workflows in android-components and fenix.
