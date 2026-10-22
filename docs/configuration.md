# Configuration workflow

The canonical export directory is `/sync` at the project root.

Initially, the ignored `settings.local.php` named `/sync`, but it was not included from `settings.php`. DDEV therefore supplied `sites/default/files/sync`. A fresh export must not depend on that accidental fallback.

`sites/default/settings.project.php` now sets:

```php
$settings['config_sync_directory'] = DRUPAL_ROOT . '/sync';
```

It is allowed by `.gitignore`. The local ignored `settings.php` includes it after DDEV settings. Every deployment must include this shared file from its own `settings.php` after other settings overrides. Database credentials and other environment settings stay in the environment's settings files.

## Final export

After upgrade validation, the original `/sync` was backed up, every existing entry in that directory was removed, and Drupal exported a fresh configuration set from the upgraded active database. Drupal's deny-access `.htaccess` protection file was explicitly regenerated with its FileSecurity API after export. The export was then compared to active storage, and a subsequent import was checked for a no-op result.

This preserves active database changes that predated the upgrade. In particular, HTTPSWWW remains uninstalled, rather than being restored from a stale export. Core updates also remove obsolete configuration and update Views, fields and other schemas.

For later configuration tasks:

```sh
ddev drush status --fields=config-sync
ddev drush config:export -y
ddev drush config:status
```

For a future full purge, first make a backup and export to a temporary directory. Only replace `/sync` after the temporary export succeeds. Do not delete active configuration from the database to clean the export directory.

Because this project uses a root-level layout, production webserver rules must deny direct access to `/sync` and private files. Apache honours the exported `.htaccess`; Nginx requires equivalent server rules. Environment settings and access rules need review as part of the separate go-live configuration work.
