# Drupal 11 upgrade record

## Result

| Component | Before | After |
| --- | --- | --- |
| Drupal core and core Composer packages | 10.6.15 | 11.4.11 |
| Drush | 12.5.3 | 13.8.0 |
| composer/installers | 1.12.0 | 2.3.0 |
| menu_link_attributes | 1.7.0 | 1.10.0 |
| Webform | 6.3.0 | 6.3.1 |
| PHP in DDEV | 8.3.30 | 8.3.30 |
| MariaDB in DDEV | 11.8.6 | 11.8.6 |

Composer also updated the core dependency tree, including Symfony 7.4. Exact versions are recorded in `composer.lock`. Core requirements are `^11.4`, Drush `^13`, and PHP `^8.3`. Stable releases remain preferred; no compatibility checks or security advisories were bypassed.

## Preparation

- Confirmed Drupal 10.6.15 bootstrapped and had no pending database updates.
- Created DDEV database snapshot `pre-drupal11` before mutations.
- Saved original Composer files, `.htaccess`, libraries, and `/sync` outside the repository in `/tmp/telliodora11-pre-upgrade/`. This is a temporary local rollback aid, not a durable backup.
- Recorded differences between active configuration and `/sync`: backup schedule, enabled modules, Webform format/settings/contact form, and the obsolete `httpswww.settings` file. The active site had HTTPSWWW uninstalled already.
- Ran Upgrade Status against the custom theme on Drupal 10. Its only finding was the theme's core version declaration.

## Implementation

- Updated Composer core constraints and Drush, then resolved dependencies with `composer update --with-all-dependencies` after a successful dry run.
- Allowed the Symfony Runtime plugin required by Drupal 11.4 and upgraded the Composer installer.
- Changed `themes/custom/telliodora/telliodora.info.yml` to support `^10.3 || ^11`.
- Installed all standalone libraries using Composer; see [inventory](libraries.md).
- Replaced the Font Awesome kit script in `html.html.twig` with a Drupal theme library using local CSS and webfonts.
- Added a shared configuration-directory setting; see [configuration](configuration.md).
- Ran `ddev drush updatedb -y` and `ddev drush cr`; all database updates completed.
- Changed local `.ddev/config.yaml` project type from `drupal10` to `drupal11` and restarted DDEV. This directory remains ignored by the pre-existing repository policy.

## Required compatibility patch

Public-page checks exposed an `ArgumentCountError` in Background Images Formatter 1.18.0: its formatter constructor passed ten arguments to Drupal 11.4's `ImageFormatter`, which requires eleven. This broke pages with background-image fields despite the module declaring Drupal 11 compatibility.

`patches/bg_image_formatter-drupal-11.4-constructor.patch` injects `ImageDerivativeUtilities` through the formatter's factory and constructor and passes it to the parent. The patch was authored against the installed release after inspecting core. Related upstream issue: [3608185](https://www.drupal.org/project/bg_image_formatter/issues/3608185).

`cweagans/composer-patches` 2.0.0 applies the local patch during Composer installation. Its SHA-256 and depth are pinned in both `composer.json` and `patches.lock.json`. The module was reinstalled through Composer to prove patch application. Remove the patch only after an upstream release fixes the constructor and the page checks pass without it.

## Deployment onto an existing site

1. Back up production database, public/private files, code, and environment settings. Confirm the target meets [Drupal 11 requirements](https://www.drupal.org/docs/getting-started/system-requirements): PHP 8.3+, Composer 2.7+, and a supported database (MariaDB 10.6+).
2. Deploy the project source, Composer lock files, local patch, theme, `sites/default/settings.project.php`, and final `/sync` together. Run Composer from the repository root. Production must have Git available for Composer Patches.
3. Ensure production `sites/default/settings.php` includes the shared settings **after** other settings overrides:

   ```php
   require __DIR__ . '/settings.project.php';
   ```

   The local environment's ignored `settings.php` has been updated. Production settings are not managed by this repository. Review any customised `.htaccess` rules against Drupal 11 scaffolding.
4. Enable maintenance mode and install the locked dependencies, then run database updates before importing the Drupal 11 configuration:

   ```sh
   vendor/bin/drush state:set system.maintenance_mode 1
   composer install --no-dev --prefer-dist --no-interaction --optimize-autoloader
   vendor/bin/drush updatedb -y
   vendor/bin/drush config:import -y
   vendor/bin/drush cache:rebuild
   ```

5. Verify pages, menus, sliders, icons, video embeds and contact forms in both languages; review logs. Disable maintenance mode and rebuild caches when ready.

The existing `.cpanel.yml` only copies files. It does not install Composer dependencies, apply patches, update the database or import configuration. Those steps must be added to the deployment process or run explicitly. No deployment was performed during this upgrade.

## Rollback

Restore code, dependency lock files, libraries, configuration and database as a matched pre-upgrade set. Do not run Drupal 10 against the upgraded database. Locally, the original database can be restored with `ddev snapshot restore pre-drupal11`; restore original code/Composer requirements and run `composer install` as part of the same rollback. Restore the original libraries archive because they were unmanaged before this upgrade, and restore the original sync settings. The temporary archives are outside version control and may be removed by the operating system.

Reference: [official Drupal 10 to 11 upgrade guide](https://www.drupal.org/docs/upgrading-drupal/upgrading-drupal/how-to-upgrade-from-drupal-10-to-drupal-11).
