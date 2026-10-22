# Composer-managed frontend libraries

All eight standalone library directories are installed by `composer/installers` into `libraries/{$name}` from explicitly versioned package repositories in `composer.json`. npm archives include registry SHA-1 checksums; FitVids uses an immutable upstream Git commit. The lock file records the exact distributions. No npm install step or manual library download is needed.

| Composer package | Version | Installed directory | Consumer |
| --- | --- | --- | --- |
| telliodora-library/blazy | 1.8.2 | libraries/blazy | Existing bLazy library retained; modern Blazy also ships its own implementation |
| telliodora-library/fitvids | 1.1.0 | libraries/fitvids | FitVids |
| telliodora-library/fontawesome | 6.7.2 | libraries/fontawesome | Telliodora theme; free solid, regular and brand icons plus v4 shims |
| telliodora-library/mmenu | 8.5.20 | libraries/mmenu | Responsive Menu, including Bootstrap wrapper |
| telliodora-library/popperjs | 2.11.6 | libraries/popperjs | Webform tooltips |
| telliodora-library/slick | 1.8.1 | libraries/slick | Slick / Slick Views |
| telliodora-library/superfish | 1.7.10 | libraries/superfish | Responsive Menu, including hoverIntent |
| telliodora-library/tippyjs | 6.3.7 | libraries/tippyjs | Webform tooltips |

Existing versions were retained for menu and video libraries. Slick moved from 1.8.0 to 1.8.1. Popper and Tippy use the versions declared by Webform. Font Awesome Free 6.7.2 supports the brand/solid classes found in the content blocks. The original hosted kit could contain custom or Pro icons; none were found in the inspected blocks, but visual review remains necessary.

Core and contributed module/theme assets (including Bootstrap JavaScript and jQuery UI assets) already arrive through Composer packages. The custom theme's compiled CSS and its source SCSS remain project source.

`/libraries` is ignored by Git; generated assets must be installed from Composer on every environment. Package repositories expose a specific version, with matching patch-level constraints and immutable distributions. To change a library version, update its repository metadata and requirement together, then update the corresponding Composer package and test its consumer. Avoid replacing a fixed archive with a moving branch.

Reinstall check:

```sh
ddev composer reinstall 'telliodora-library/*' --no-interaction
ddev drush cr
ddev exec python3 docs/scripts/smoke-test.py
```

Webform now reports **2 installed, 12 excluded, 0 CDN** libraries. Optional excluded widgets remain excluded. Optional Slick/Blazy integrations that are not configured are not installed merely because their library definitions exist.

Google Analytics remains a remote runtime service script, and reCAPTCHA remains a provider integration. These are not static library archives that can be installed by Composer. The remote Font Awesome kit has been removed.

## Colorbox

Neither the initial active configuration nor the original `/sync` referenced Colorbox, and neither its module nor library was installed. The user subsequently asked to ignore that request. No Colorbox module, library, formatter or gallery behaviour was introduced. The existing Slick and Blazy integrations are retained.
