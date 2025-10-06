"""
DNS Analysis Engine for ShadowRecon v1.0
"""

import socket
from typing import List, Dict, Any

class DNSAnalyzer:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def analyze_dns(self, domain: str) -> Dict[str, Any]:
        """Perform comprehensive DNS analysis"""
        analysis = {
            'domain': domain,
            'a_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': []
        }

        # A records
        try:
            ip = socket.gethostbyname(domain)
            analysis['a_records'].append(ip)
        except:
            pass

        # Try to get additional DNS info if dns module is available
        try:
            import dns.resolver

            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                analysis['mx_records'] = [str(mx) for mx in mx_records]
            except:
                pass

            # NS records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                analysis['ns_records'] = [str(ns) for ns in ns_records]
            except:
                pass

            # TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                analysis['txt_records'] = [str(txt) for txt in txt_records]
            except:
                pass

        except ImportError:
            if self.verbose:
                print("[!] dnspython not available for advanced DNS analysis")

        return analysis

    def check_wildcard_dns(self, domain: str) -> bool:
        """Check if domain has wildcard DNS"""
        try:
            # Generate random subdomain
            import random
            import string
            random_sub = ''.join(random.choices(string.ascii_lowercase, k=20))
            test_domain = f"{random_sub}.{domain}"

            socket.gethostbyname(test_domain)
            return True  # If resolved, wildcard exists
        except:
            return False
