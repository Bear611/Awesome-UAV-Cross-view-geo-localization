#!/usr/bin/env python3
"""Open a publisher page in the persistent CARSI/CAS browser profile."""

from __future__ import annotations

import argparse

from browser_session_utils import add_common_browser_args, ensure_paths, export_netscape_cookies, import_playwright, launch_persistent_browser, print_cookie_domain_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open one URL in the visible persistent publisher-access browser.")
    add_common_browser_args(parser)
    parser.add_argument("url", help="Publisher, DOI, paper, or PDF URL to open.")
    parser.add_argument("--export-cookies", action="store_true", help="Export Netscape cookies before closing.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    ensure_paths(args.profile, args.cookie_output, args.download_dir)
    sync_playwright = import_playwright()

    print(f"Persistent profile: {args.profile}")
    print(f"Opening: {args.url}")
    with sync_playwright() as p:
        context = launch_persistent_browser(p, args.profile, args.download_dir, args.browser_channel)
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=90000)
        input("Use the visible browser as needed. Press Enter here to continue...")
        if args.export_cookies:
            cookies = context.cookies()
            count = export_netscape_cookies(cookies, args.cookie_output)
            print(f"Exported {count} cookies to {args.cookie_output}")
            print_cookie_domain_summary(cookies)
        context.close()


if __name__ == "__main__":
    main()
