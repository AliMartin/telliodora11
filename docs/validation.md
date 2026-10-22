# Upgrade validation — 22 October 2026

## Passed

- Drupal reports **11.4.11**, successful bootstrap, connected database, and `/var/www/html/sync` as its configuration directory after a DDEV restart.
- `composer validate --strict` passes.
- `composer audit` reports no security advisories. The original lock file had advisories affecting core and other dependencies.
- `composer check-platform-reqs` passes on PHP 8.3.30.
- `composer install --dry-run --no-interaction` has nothing to install, update or remove.
- All eight standalone libraries were removed/reinstalled using Composer; no manual assets were needed.
- Background Images Formatter was reinstalled using Composer and its SHA-256-locked compatibility patch applied successfully.
- All 15 checked Drupal library asset definitions for menus, Slick, FitVids, Font Awesome and Webform resolve to existing local files.
- Webform's runtime requirements report 2 installed external libraries, 12 excluded, and 0 CDN libraries.
- Database updates completed; `drush updatedb:status` reports none pending, and entity definition change count is zero.
- PHP lint passes for the custom theme PHP file and shared project settings.
- `git diff --check` passes.

## HTTP smoke checks

`ddev exec python3 docs/scripts/smoke-test.py` passes for 11 routes:

`/`, `/ru`, `/music`, `/videos`, `/biography`, `/contact`, `/ru/biografiya`, `/ru/muzyka`, `/ru/video`, `/ru/telliodora`, `/user/login`.

All return nonempty HTTP 200 responses. All 26 checked local assets return nonempty HTTP 200 responses, including aggregated Drupal assets, menu libraries, Slick, FitVids, bLazy, Font Awesome CSS and brand/solid webfonts, Popper and Tippy. The Font Awesome kit URL is absent. The only external script/style URL in the server-rendered HTML is Google Analytics.

The initial page checks caught the Background Images Formatter constructor failure. After the patch, the same checks passed, including after restarting DDEV. Old error log entries remain for diagnosis; the failed diagnostic Drush query made during validation also remains in the logs.

Detailed HTTP results: [smoke-test-results.json](smoke-test-results.json).

## Fresh configuration

The original root export had 586 YAML files in the default collection and 173 in language collections, plus `.htaccess` and a `.DS_Store` entry. The final export has 583 YAML files in the default collection and 173 YAML files in language collections. These counts reflect a complete fresh export from active storage, not a hand-edited subset. A deny-access `.htaccess` was explicitly regenerated using Drupal's FileSecurity API after export.

After the purge and export, `drush config:status` reports no differences and `drush config:import -y` reports no changes to import.

## Remaining manual and go-live checks

No browser was available through the session's computer-use interface, so HTTP and file checks do not establish visual appearance or JavaScript behaviour. Before going live, check desktop/mobile navigation, Russian navigation, slider controls and looping, icon appearance, video playback/embeds, and contact form validation/submission in a real browser. No form submissions or messages were sent during this work.

The following existing/environment or future-version status items were left for the separate configuration work:

- DDEV disables settings-file write protection and uses development host settings; production needs its own protected settings and trusted hosts.
- The active environment has no private file path, although an unused `settings.local.php` contains one. Review private files and Webform uploads before launch.
- Stable 9 is deprecated in Drupal 11 and remains installed; replacement/removal belongs to follow-up configuration and future Drupal 12 preparation. History was uninstalled in the follow-up below.
- Drupal warns about the future HTML5 form-validation default in Drupal 12. Current behaviour was retained.
- Update-manager cached release information may need refreshing after the major upgrade. The installed version and security checks above use Composer directly.
- Production needs the shared settings include, a Composer-aware deployment process, and access protection for `/sync` (especially under Nginx). See [deployment](drupal11-upgrade.md).

Colorbox was absent at baseline and left out following the user's clarification.

## Follow-up: uninstall History — 22 October 2026

Ran `ddev drush pm:uninstall history -y`, then `ddev drush config:export -y`. Verified History is absent from both the active module handler and `core.extension`; `drush config:status` reports no differences between active configuration and `/sync`. History is supplied by Drupal core, so no Composer package removal is required.

## Follow-up: project temporary-directory cleanup — 22 October 2026

Removed generated Upgrade Status/PHPStan caches from the project's `tmp/` directory. Preserved `tmp/.htaccess`. Moved the old `tmp/config.tar.gz` configuration backup to `/private/tmp/telliodora11-pre-upgrade/project-tmp-config.tar.gz`, outside the web root; this is temporary local storage, not a durable backup. Added Git ignore rules for runtime contents while retaining `.htaccess`. No active configuration changed.
