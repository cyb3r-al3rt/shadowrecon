"""
Directory Discovery Engine for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

import asyncio
from typing import List, Dict, Any, Optional

class DirectoryEngine:
    """Advanced directory discovery engine"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.common_directories = [
            'admin', 'administrator', 'login', 'panel', 'dashboard',
            'api', 'v1', 'v2', 'test', 'dev', 'staging', 'backup',
            'uploads', 'images', 'css', 'js', 'assets', 'static',
            'public', 'private', 'config', 'conf', 'settings'
        ]

    async def discover_directories(self, url: str, session, 
                                 deep_mode: bool = False, 
                                 use_seclists: bool = False) -> List[Dict[str, Any]]:
        """Discover directories using wordlist enumeration"""

        directories = []
        wordlist = self.common_directories.copy()

        if deep_mode:
            wordlist.extend([
                'phpmyadmin', 'adminer', 'wp-admin', 'wp-content', 'wp-includes',
                'drupal', 'joomla', 'magento', 'prestashop', 'opencart',
                'administrator', 'manager', 'admin.php', 'login.php',
                'dashboard.php', 'index.php', 'default.php', 'home.php'
            ])

        if not session:
            return directories

        # Test each directory
        for directory in wordlist:
            test_url = f"{url.rstrip('/')}/{directory}"
            try:
                # Import http_utils here to avoid circular imports
                from ..utils.http_utils import HTTPUtils

                response = await HTTPUtils.safe_request(session, 'GET', test_url)

                if response and response.get('status') in [200, 201, 202, 301, 302, 403]:
                    directory_info = {
                        'url': test_url,
                        'status': response.get('status'),
                        'content_length': response.get('content_length', 0),
                        'content_type': response.get('content_type', ''),
                        'directory': directory
                    }
                    directories.append(directory_info)

                    if self.verbose:
                        print(f"[+] Found directory: {test_url} [{response.get('status')}]")

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error testing {test_url}: {e}")
                continue

        return directories
