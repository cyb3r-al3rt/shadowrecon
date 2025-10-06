#!/usr/bin/env python3
"""
ShadowRecon v1.0 - Ultimate Web Attack Surface Discovery Framework
Developed by kernelpanic | A product of infosbios

"In the shadows, we find the truth. In reconnaissance, we find power."

An advanced automated framework for comprehensive web attack surface discovery,
designed for CTFs, bug hunting, and penetration testing.
"""

import asyncio
import argparse
import sys
import os
import signal
from pathlib import Path

def find_shadowrecon_modules():
    """Find ShadowRecon modules using multiple strategies"""

    # Strategy 1: Current directory
    if os.path.exists('./shadowrecon') and os.path.isdir('./shadowrecon'):
        sys.path.insert(0, '.')
        return True

    # Strategy 2: Same directory as script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shadowrecon_path = os.path.join(script_dir, 'shadowrecon')
    if os.path.exists(shadowrecon_path):
        sys.path.insert(0, script_dir)
        return True

    # Strategy 3: Installed package
    try:
        import shadowrecon
        return True
    except ImportError:
        pass

    return True

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 ShadowRecon interrupted by user")
    print("💀 'In the shadows, we retreat to fight another day...'")
    print("\nDeveloped by kernelpanic | A product of infosbios")
    sys.exit(0)

def main():
    """Main entry point for ShadowRecon"""

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Find ShadowRecon modules
    if not find_shadowrecon_modules():
        print("❌ Cannot find ShadowRecon modules")
        print("🔧 Run from shadowrecon directory")
        return 1

    # Import ShadowRecon modules
    try:
        from shadowrecon.utils.banner import ShadowBanner, ShadowQuotes
        from shadowrecon.utils.colors import ShadowColors
        from shadowrecon.utils.validators import validate_domain, clean_domain
        from shadowrecon.core.shadow_engine import ShadowEngine
    except ImportError as e:
        print(f"❌ Error importing ShadowRecon: {e}")
        print("🔧 Install dependencies: pip3 install -r requirements.txt")
        return 1

    # Argument parser
    parser = argparse.ArgumentParser(
        description='ShadowRecon v1.0 - Ultimate Web Attack Surface Discovery',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  shadowrecon -d example.com
  shadowrecon -d example.com --deep --crawl --inject
  shadowrecon -d example.com --nuclei --subfinder --threads 200
  shadowrecon -l targets.txt --output ./results --format html,json,csv
        '''
    )

    # Target options
    parser.add_argument('-d', '--domain', help='Target domain for scanning')
    parser.add_argument('-l', '--list', help='File containing list of target domains')
    parser.add_argument('--scope', help='Scope file for in-scope domains/IPs')

    # Scanning modes
    parser.add_argument('--deep', action='store_true', help='Enable deep reconnaissance mode')
    parser.add_argument('--crawl', action='store_true', help='Enable web crawling and form detection')
    parser.add_argument('--inject', action='store_true', help='Enable payload injection testing')
    parser.add_argument('--passive', action='store_true', help='Passive reconnaissance only')

    # Payload options
    parser.add_argument('--payloads', help='Comma-separated payload types (xss,lfi,ssrf,sqli,rce,xxe)')
    parser.add_argument('--wordlist', help='Custom wordlist file for enumeration')
    parser.add_argument('--seclists', action='store_true', help='Use SecLists wordlists automatically')

    # Performance options
    parser.add_argument('--threads', type=int, default=100, help='Concurrent threads (default: 100)')
    parser.add_argument('--timeout', type=int, default=30, help='HTTP timeout in seconds (default: 30)')
    parser.add_argument('--retries', type=int, default=2, help='Retries for failed requests (default: 2)')
    parser.add_argument('--delay', type=float, default=0, help='Delay between requests in seconds (default: 0)')

    # Output options
    parser.add_argument('-o', '--output', default='./shadowrecon_output', help='Output directory')
    parser.add_argument('--format', default='html,json', help='Report formats: html,json,csv,xml')
    parser.add_argument('--quiet', action='store_true', help='Suppress banner and non-essential output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable detailed verbose output')

    # External tool integration
    parser.add_argument('--nuclei', action='store_true', help='Enable Nuclei vulnerability scanner')
    parser.add_argument('--subfinder', action='store_true', help='Enable Subfinder subdomain discovery')
    parser.add_argument('--ffuf', action='store_true', help='Enable FFUF web fuzzer')
    parser.add_argument('--sqlmap', action='store_true', help='Enable SQLMap SQL injection testing')
    parser.add_argument('--nmap', action='store_true', help='Enable Nmap port scanning')

    # Advanced options
    parser.add_argument('--user-agent', help='Custom User-Agent string')
    parser.add_argument('--proxy', help='HTTP proxy (http://proxy:port or socks5://proxy:port)')
    parser.add_argument('--headers', help='Custom headers (key:value,key:value)')
    parser.add_argument('--cookies', help='Custom cookies (name=value;name=value)')
    parser.add_argument('--config', help='Configuration file path')

    # Information
    parser.add_argument('--version', action='version', version='ShadowRecon v1.0.0')

    args = parser.parse_args()

    # Display banner (unless quiet mode)
    if not args.quiet:
        try:
            print(ShadowBanner.generate_banner())
        except Exception:
            print("🎭 ShadowRecon v1.0 - Ultimate Web Attack Surface Discovery Framework")
            print("Developed by kernelpanic | A product of infosbios")
            print("💀 'In the shadows, we find the truth...'")
            print()

    # Validate input
    if not args.domain and not args.list:
        parser.error("Either --domain or --list must be specified")
        return 1

    # Handle domain list
    targets = []
    if args.list:
        try:
            with open(args.list, 'r') as f:
                targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"❌ Target list file not found: {args.list}")
            return 1
        except Exception as e:
            print(f"❌ Error reading target list: {e}")
            return 1
    else:
        targets = [args.domain]

    # Validate domains
    valid_targets = []
    for target in targets:
        if validate_domain(target):
            valid_targets.append(clean_domain(target))
        else:
            print(f"❌ Invalid domain: {target}")

    if not valid_targets:
        print("❌ No valid targets found")
        return 1

    # Parse payload types
    payload_types = []
    if args.payloads:
        payload_types = [p.strip().lower() for p in args.payloads.split(',')]
    else:
        payload_types = ['xss', 'lfi', 'ssrf', 'sqli'] if args.inject else []

    # Parse report formats
    report_formats = [f.strip().lower() for f in args.format.split(',')]

    try:
        # Initialize ShadowRecon engine
        shadow_engine = ShadowEngine(
            output_dir=args.output,
            threads=args.threads,
            timeout=args.timeout,
            retries=args.retries,
            delay=args.delay,
            verbose=args.verbose,
            deep_mode=args.deep,
            crawl_mode=args.crawl,
            inject_mode=args.inject,
            passive_mode=args.passive,
            payloads=payload_types,
            wordlist_file=args.wordlist,
            use_seclists=args.seclists,
            report_formats=report_formats,
            user_agent=args.user_agent,
            proxy=args.proxy,
            headers=args.headers,
            cookies=args.cookies,
            enable_nuclei=args.nuclei,
            enable_subfinder=args.subfinder,
            enable_ffuf=args.ffuf,
            enable_sqlmap=args.sqlmap
        )

        # Run attack surface discovery
        if len(valid_targets) == 1:
            asyncio.run(shadow_engine.discover_attack_surface(valid_targets[0]))
        else:
            asyncio.run(shadow_engine.discover_multiple_targets(valid_targets))

        return 0

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
