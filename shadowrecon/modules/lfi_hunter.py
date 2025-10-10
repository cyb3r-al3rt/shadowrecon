"""
LFI Hunter Module for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

from typing import List, Dict, Any
import asyncio

class LFIHunter:
    """Local File Inclusion vulnerability hunter"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.vulnerability_type = "lfi"

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for LFI vulnerabilities"""

        vulnerabilities = []

        if not session:
            return vulnerabilities

        try:
            # Import payloads
            from ..payloads.lfi_payloads import LFIPayloads

            # Get basic LFI payloads
            payloads = LFIPayloads.BASIC_LFI[:3]  # Limit for demo

            url = endpoint.get('url', '')
            if not url:
                return vulnerabilities

            # Test each payload
            for payload in payloads:
                try:
                    # Import http_utils here to avoid circular imports
                    from ..utils.http_utils import HTTPUtils

                    # Simple parameter injection
                    test_url = f"{url}?file={payload}"
                    response = await HTTPUtils.safe_request(session, 'GET', test_url)

                    if response and response.get('status') == 200:
                        content = response.get('content', '')
                        if 'root:' in content or 'daemon:' in content:  # Basic /etc/passwd detection
                            vulnerability = {
                                'type': 'lfi',
                                'severity': 'high',
                                'url': test_url,
                                'payload': payload,
                                'evidence': f'File inclusion successful: {content[:100]}...',
                                'method': 'GET'
                            }
                            vulnerabilities.append(vulnerability)

                            if self.verbose:
                                print(f"[!] LFI found: {test_url}")
                            break

                except Exception as e:
                    if self.verbose:
                        print(f"[!] Error testing LFI payload: {e}")
                    continue

        except ImportError:
            if self.verbose:
                print("[!] LFI payloads not available")

        return vulnerabilities
