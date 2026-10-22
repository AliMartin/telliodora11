#!/usr/bin/env python3
"""Read-only page and frontend asset checks. Run inside DDEV with Python 3."""
import json
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'https://telliodora11.ddev.site'
PATHS = ['/', '/ru', '/music', '/videos', '/biography', '/contact',
         '/ru/biografiya', '/ru/muzyka', '/ru/video', '/ru/telliodora', '/user/login']
LIBRARIES = [
    '/libraries/slick/slick/slick.min.js', '/libraries/slick/slick/slick.css',
    '/libraries/mmenu/dist/mmenu.js', '/libraries/mmenu/dist/mmenu.css',
    '/libraries/mmenu/dist/wrappers/bootstrap/mmenu.bootstrap.css',
    '/libraries/superfish/dist/js/superfish.min.js',
    '/libraries/superfish/dist/js/hoverIntent.js', '/libraries/blazy/blazy.min.js',
    '/libraries/fitvids/jquery.fitvids.js', '/libraries/fontawesome/css/all.min.css',
    '/libraries/fontawesome/css/v4-shims.min.css',
    '/libraries/fontawesome/webfonts/fa-brands-400.woff2',
    '/libraries/fontawesome/webfonts/fa-solid-900.woff2',
    '/libraries/popperjs/dist/umd/popper.js', '/libraries/tippyjs/dist/tippy.umd.js',
    '/libraries/tippyjs/dist/tippy.css',
]


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('src'):
            self.urls.add(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.urls.add(attrs['href'])


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
        if response.status != 200 or not data:
            raise RuntimeError('Expected a nonempty HTTP 200 response')
        return data


results, errors, assets, external = [], [], set(LIBRARIES), set()
for path in PATHS:
    try:
        html = fetch(BASE + path).decode()
        if 'kit.fontawesome.com' in html:
            raise RuntimeError('Remote Font Awesome kit still present')
        parser = Assets()
        parser.feed(html)
        for url in parser.urls:
            url = urllib.parse.urljoin(BASE + path, url)
            if urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(BASE).netloc:
                assets.add(url)
            else:
                external.add(url)
        results.append({'path': path, 'status': 200})
    except Exception as exc:
        errors.append({'path': path, 'error': str(exc)})
for asset in sorted(assets):
    try:
        fetch(urllib.parse.urljoin(BASE, asset))
    except Exception as exc:
        errors.append({'asset': asset, 'error': str(exc)})
print(json.dumps({'pages': results, 'local_assets_checked': len(assets),
                  'external_scripts_or_styles': sorted(external), 'errors': errors}, indent=2))
sys.exit(bool(errors))
