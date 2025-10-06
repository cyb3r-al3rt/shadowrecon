"""
Certificate Analysis Engine for ShadowRecon v1.0
"""

import ssl
import socket
from typing import Dict, Any, Optional

class CertificateAnalyzer:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def analyze_certificate(self, hostname: str, port: int = 443) -> Optional[Dict[str, Any]]:
        """Analyze SSL certificate for domain"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()

                    return {
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'subject_alt_names': [x[1] for x in cert.get('subjectAltName', [])],
                        'hostname': hostname,
                        'port': port
                    }

        except Exception as e:
            if self.verbose:
                print(f"[!] Certificate analysis failed for {hostname}: {e}")
            return None

    def extract_domains_from_cert(self, cert_info: Dict[str, Any]) -> list:
        """Extract domains from certificate information"""
        domains = []

        # Common name from subject
        subject = cert_info.get('subject', {})
        if 'commonName' in subject:
            domains.append(subject['commonName'])

        # Subject alternative names
        san_domains = cert_info.get('subject_alt_names', [])
        domains.extend(san_domains)

        # Clean and deduplicate
        clean_domains = []
        for domain in domains:
            domain = domain.strip().lower()
            if domain.startswith('*.'):
                domain = domain[2:]
            if domain and domain not in clean_domains:
                clean_domains.append(domain)

        return clean_domains
