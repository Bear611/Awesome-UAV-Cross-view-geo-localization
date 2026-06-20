#!/usr/bin/env python3
"""Initialize a visible Chromium session for CARSI/CAS publisher access."""

from __future__ import annotations

import argparse

from browser_session_utils import (
    add_common_browser_args,
    ensure_paths,
    export_netscape_cookies,
    import_playwright,
    print_cookie_domain_summary,
)


DEFAULT_URLS = [
    "https://ieeexplore.ieee.org/",
    "https://dl.acm.org/",
    "https://link.springer.com/",
    "https://www.sciencedirect.com/",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open a visible browser for manual CARSI/CAS login and export cookies.")
    add_common_browser_args(parser)
    parser.add_argument("--url", action="append", default=[], help="Publisher URL to open. Can be repeated.")
    parser.add_argument("--no-default-urls", action="store_true", help="Only open URLs supplied with --url.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    urls = args.url or ([] if args.no_default_urls else DEFAULT_URLS)
    ensure_paths(args.profile, args.cookie_output, args.download_dir)
    sync_playwright = import_playwright()

    print(f"Persistent profile: {args.profile}")
    print(f"Cookie export path: {args.cookie_output}")
    print("A visible Chromium window will open. Complete CARSI/CAS login manually there.")
    print("After login, open a publisher paper/PDF page and confirm access, then return here.")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            args.profile,
            headless=False,
            accept_downloads=True,
            downloads_path=args.download_dir,
        )
        page = context.new_page()
        for idx, url in enumerate(urls):
            target = page if idx == 0 else context.new_page()
            target.goto(url, wait_until="domcontentloaded", timeout=90000)
        input("When login/access checks are complete, press Enter to export cookies and close Chromium...")
        cookies = context.cookies()
        count = export_netscape_cookies(cookies, args.cookie_output)
        print(f"Exported {count} cookies to {args.cookie_output}")
        print_cookie_domain_summary(cookies)
        context.close()


if __name__ == "__main__":
    main()
