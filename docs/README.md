# Telliodora maintenance documentation

Drupal 11 upgrade completed locally on 22 October 2026. This work does not deploy the site to production.

- [Upgrade record, deployment and rollback](drupal11-upgrade.md)
- [Composer library inventory](libraries.md)
- [Configuration export workflow](configuration.md)
- [Validation and remaining checks](validation.md)

The site retains its root-level Drupal layout: `core/`, `modules/`, `themes/`, `libraries/`, and `vendor/` sit alongside `composer.json`. Use `composer.json`, `composer.lock`, and `patches.lock.json`; the pre-existing `composer new.json` and `composer new.lock` are not used.
