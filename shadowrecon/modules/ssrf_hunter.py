"""
SSRF Hunter Module for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

from typing import List, Dict, Any
import asyncio

class SSRFHunter:
    """Server-Side Request Forgery vulnerability hunter"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.vulnerability_type = "ssrf"

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for SSRF vulnerabilities"""

        vulnerabilities = []

        if not session:
            return vulnerabilities

        try:
            # Import payloads
            from ..payloads.ssrf_payloads import SSRFPayloads

            # Get AWS metadata payloads
            payloads = SSRFPayloads.AWS_METADATA[:2]  # Limit for demo

            url = endpoint.get('url', '')
            if not url:
                return vulnerabilities

            # Test each payload
            for payload in payloads:
                try:
                    # Import http_utils here to avoid circular imports
                    from ..utils.http_utils import HTTPUtils

                    # Simple URL parameter injection
                    test_url = f"{url}?url={payload}"
                    response = await HTTPUtils.safe_request(session, 'GET', test_url)

                    if response and response.get('status') == 200:
                        content = response.get('content', '')
                        if 'instance-id' in content or 'ami-id' in content:  # AWS metadata indicators
                            vulnerability = {
                                'type': 'ssrf',
                                'severity': 'critical',
                                'url': test_url,
                                'payload': payload,
                                'evidence': f'SSRF successful - AWS metadata exposed: {content[:100]}...',
                                'method': 'GET'
                            }
                            vulnerabilities.append(vulnerability)

                            if self.verbose:
                                print(f"[!] SSRF found: {test_url}")
                            break

                except Exception as e:
                    if self.verbose:
                        print(f"[!] Error testing SSRF payload: {e}")
                    continue

        except ImportError:
            if self.verbose:
                print("[!] SSRF payloads not available")

        return vulnerabilities
