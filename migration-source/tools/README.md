# Sanitized WordPress content export

The exporter loads the existing WordPress installation and writes only migration-relevant public page content to JSON.

It does **not** export:

- users,
- password hashes,
- database credentials,
- WordPress auth salts,
- sessions,
- API secrets.

## Run on the existing server

From the repository root, for the current server layout:

```bash
php migration-source/tools/export-wordpress-content.php \
  /mnt/web202/b0/55/533255/htdocs/www/bloecher.de/wordpress \
  migration-source/export/wordpress-content.json
```

Then inspect:

```bash
python3 -m json.tool migration-source/export/wordpress-content.json >/dev/null
du -h migration-source/export/wordpress-content.json
```

Before committing, run a conservative secret scan:

```bash
grep -Ein 'user_pass|password|passwd|secret|auth_key|secure_auth|logged_in_key|nonce_key|db_password' \
  migration-source/export/wordpress-content.json
```

No matches are expected.

The JSON contains:

- published pages,
- parent/child structure,
- slugs and current permalinks,
- raw WordPress/Avia page content,
- Polylang language and translation relationships,
- selected Yoast SEO metadata,
- featured image references,
- referenced attachment metadata.

This file is the source for the deterministic WordPress/Avia → Hugo conversion.
