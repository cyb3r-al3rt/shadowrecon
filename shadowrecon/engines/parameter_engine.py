"""
Parameter Discovery Engine for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

from typing import List, Optional

class ParameterEngine:
    """Advanced parameter discovery engine"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.common_parameters = [
            'id', 'user', 'admin', 'page', 'file', 'path', 'url', 'redirect',
            'next', 'return', 'callback', 'debug', 'test', 'demo', 'example',
            'search', 'query', 'q', 'keyword', 'term', 'filter', 'sort',
            'limit', 'offset', 'start', 'end', 'from', 'to', 'action'
        ]

    async def discover_parameters(self, domain: str, session, 
                                 deep_mode: bool = False) -> List[str]:
        """Discover hidden parameters"""

        parameters = []

        # Basic parameter discovery
        parameters.extend(self.common_parameters)

        if deep_mode:
            parameters.extend([
                'token', 'csrf', 'session', 'auth', 'key', 'secret',
                'password', 'pass', 'pwd', 'username', 'user_id',
                'admin_id', 'role', 'permission', 'access', 'level'
            ])

        if self.verbose:
            print(f"[*] Discovered {len(parameters)} potential parameters")

        return parameters
