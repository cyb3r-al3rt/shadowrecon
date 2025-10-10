"""
XSS Hunter Module for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

from typing import List, Dict, Any, Optional
import asyncio

class XSSHunter:
    """Cross-Site Scripting vulnerability hunter"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.vulnerability_type = "xss"

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for XSS vulnerabilities"""

        vulnerabilities = []

        if not session:
            return vulnerabilities

        try:
            # Import payloads
            from ..payloads.xss_payloads import XSSPayloads

            # Get basic XSS payloads
            payloads = XSSPayloads.BASIC_PAYLOADS[:5]  # Limit for demo

            url = endpoint.get('url', '')
            if not url:
                return vulnerabilities

            # Test each payload
            for payload in payloads:
                try:
                    # Import http_utils here to avoid circular imports
                    from ..utils.http_utils import HTTPUtils

                    # Simple GET parameter injection
                    test_url = f"{url}?test={payload}"
                    response = await HTTPUtils.safe_request(session, 'GET', test_url)

                    if response and response.get('status') == 200:
                        content = response.get('content', '')
                        if payload in content and '<script>' in payload:
                            vulnerability = {
                                'type': 'xss',
                                'severity': 'high',
                                'url': test_url,
                                'payload': payload,
                                'evidence': f'Payload reflected in response: {payload[:50]}...',
                                'method': 'GET'
                            }
                            vulnerabilities.append(vulnerability)

                            if self.verbose:
                                print(f"[!] XSS found: {test_url}")
                            break  # One finding per endpoint for demo

                except Exception as e:
                    if self.verbose:
                        print(f"[!] Error testing XSS payload: {e}")
                    continue

        except ImportError:
            if self.verbose:
                print("[!] XSS payloads not available")

        return vulnerabilities
