# Sync Strings GitHub Action

This GitHub Action syncs strings between two checked out copies of an Android project. It requires that these projects have a a `l10n.toml` project configuration.

Example usage in a _GitHub Workflow_ file:

```
      - name: Checkout main branch
        uses: actions/checkout@v3
        with:
          path: main
          ref: main
      - name: Checkout beta branch
        uses: actions/checkout@v3
        with:
          path: beta
          ref: releases_v88.0.0
      - name: Sync strings
        uses: mozilla-mobile/sync-strings-action@main
        with:
          toml_path: android-components/l10n.toml
          src: main
          dest: beta
```

This action will copy individual `strings.xml` files from `src` to `dest`. Adding and committing them to the repository would be the responsibility of another step in the workflow.
