"""
Template Injection Hunter for ShadowRecon v1.0
"""

from typing import List, Dict, Any
import asyncio

class TemplateInjectionHunter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.template_payloads = [
            '{{7*7}}',
            '${7*7}',
            '#{7*7}',
            '<%= 7*7 %>',
            '{{config}}',
            '${object}',
            '#{config}',
            '<%= config %>'
        ]

    async def test_endpoint(self, endpoint: Dict[str, Any], session) -> List[Dict[str, Any]]:
        """Test endpoint for template injection vulnerabilities"""
        vulnerabilities = []

        if not session:
            return vulnerabilities

        url = endpoint.get('url', '')
        if not url:
            return vulnerabilities

        for payload in self.template_payloads[:3]:  # Limit for performance
            try:
                from ..utils.http_utils import HTTPUtils

                test_url = f"{url}?template={payload}"
                response = await HTTPUtils.safe_request(session, 'GET', test_url)

                if response and response.get('status') == 200:
                    content = response.get('content', '')
                    # Look for template evaluation (49 is 7*7)
                    if '49' in content and payload in content:
                        vulnerability = {
                            'type': 'template_injection',
                            'severity': 'high',
                            'url': test_url,
                            'payload': payload,
                            'evidence': f'Template injection successful: {content[:100]}...',
                            'method': 'GET'
                        }
                        vulnerabilities.append(vulnerability)

                        if self.verbose:
                            print(f"[!] Template injection found: {test_url}")
                        break

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error testing template injection: {e}")
                continue

        return vulnerabilities
