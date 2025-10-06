"""
CSRF Hunter for ShadowRecon v1.0
"""

from typing import List, Dict, Any
import asyncio

class CSRFHunter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for CSRF vulnerabilities"""
        vulnerabilities = []

        if not session:
            return vulnerabilities

        url = endpoint.get('url', '')
        if not url:
            return vulnerabilities

        try:
            from ..utils.http_utils import HTTPUtils

            # Check for forms without CSRF tokens
            response = await HTTPUtils.safe_request(session, 'GET', url)

            if response and response.get('status') == 200:
                content = response.get('content', '')

                # Look for forms
                if '<form' in content.lower():
                    # Check if CSRF tokens are present
                    csrf_indicators = ['csrf', '_token', 'authenticity_token', 'anti-forgery']
                    has_csrf_protection = any(indicator in content.lower() for indicator in csrf_indicators)

                    if not has_csrf_protection:
                        vulnerability = {
                            'type': 'csrf',
                            'severity': 'medium',
                            'url': url,
                            'payload': 'No CSRF token detected',
                            'evidence': 'Forms found without CSRF protection',
                            'method': 'GET'
                        }
                        vulnerabilities.append(vulnerability)

                        if self.verbose:
                            print(f"[!] Potential CSRF vulnerability: {url}")

        except Exception as e:
            if self.verbose:
                print(f"[!] Error testing CSRF: {e}")

        return vulnerabilities
