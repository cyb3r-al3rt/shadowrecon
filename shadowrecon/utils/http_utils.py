"""
HTTP utilities for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced HTTP request handling, session management, and response analysis
"""

import asyncio
import ssl
from typing import Dict, Optional, List, Any
import urllib.parse

# Handle aiohttp import
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

class HTTPUtils:
    """Advanced HTTP utilities for shadow reconnaissance"""

    @staticmethod
    def create_session_config(
        timeout: int = 30,
        threads: int = 100,
        user_agent: Optional[str] = None,
        proxy: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create session configuration"""

        if not user_agent:
            user_agent = 'ShadowRecon/1.0 (Advanced Web Attack Surface Discovery Framework)'

        config = {
            'timeout': aiohttp.ClientTimeout(total=timeout) if AIOHTTP_AVAILABLE else timeout,
            'headers': {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            'connector_limit': threads,
            'ssl_verify': False
        }

        # Add custom headers
        if headers:
            for key, value in headers.items():
                config['headers'][key] = value

        # Add cookies
        if cookies:
            config['headers']['Cookie'] = cookies

        # Add proxy
        if proxy:
            config['proxy'] = proxy

        return config

    @staticmethod
    async def create_session(config: Dict[str, Any]):
        """Create aiohttp session with configuration"""
        if not AIOHTTP_AVAILABLE:
            return None

        try:
            connector = aiohttp.TCPConnector(
                limit=config.get('connector_limit', 100),
                ssl=False if not config.get('ssl_verify', True) else None
            )

            session = aiohttp.ClientSession(
                connector=connector,
                timeout=config.get('timeout'),
                headers=config.get('headers', {}),
                trust_env=True
            )

            return session

        except Exception:
            return None

    @staticmethod
    async def safe_request(
        session, 
        method: str,
        url: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make safe HTTP request with error handling"""

        if not session:
            return None

        try:
            async with session.request(method, url, **kwargs) as response:
                # Read response data
                try:
                    text_content = await response.text()
                except Exception:
                    text_content = ""

                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'content': text_content,
                    'url': str(response.url),
                    'method': method,
                    'content_length': len(text_content),
                    'content_type': response.headers.get('Content-Type', ''),
                    'server': response.headers.get('Server', ''),
                    'redirected': response.history is not None and len(response.history) > 0
                }

        except asyncio.TimeoutError:
            return {'status': 0, 'error': 'timeout', 'url': url, 'method': method}
        except Exception as e:
            return {'status': 0, 'error': str(e), 'url': url, 'method': method}

    @staticmethod
    def parse_response_for_inputs(content: str, url: str) -> List[Dict[str, Any]]:
        """Parse HTML response for input fields and forms"""
        inputs = []

        if not content:
            return inputs

        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Find all forms
            forms = soup.find_all('form')
            for form in forms:
                form_data = {
                    'type': 'form',
                    'url': url,
                    'method': form.get('method', 'get').upper(),
                    'action': form.get('action', ''),
                    'inputs': []
                }

                # Find all inputs in the form
                form_inputs = form.find_all(['input', 'textarea', 'select'])
                for inp in form_inputs:
                    input_data = {
                        'name': inp.get('name', ''),
                        'type': inp.get('type', 'text'),
                        'value': inp.get('value', ''),
                        'placeholder': inp.get('placeholder', ''),
                        'required': inp.has_attr('required')
                    }
                    form_data['inputs'].append(input_data)

                inputs.append(form_data)

            # Find standalone inputs (not in forms)
            standalone_inputs = soup.find_all(['input', 'textarea'], attrs={'form': None})
            for inp in standalone_inputs:
                if not inp.find_parent('form'):
                    input_data = {
                        'type': 'standalone_input',
                        'url': url,
                        'name': inp.get('name', ''),
                        'input_type': inp.get('type', 'text'),
                        'value': inp.get('value', ''),
                        'placeholder': inp.get('placeholder', '')
                    }
                    inputs.append(input_data)

        except ImportError:
            # Fallback parsing without BeautifulSoup
            import re

            # Basic form detection
            form_pattern = r'<form[^>]*>(.*?)</form>'
            forms = re.findall(form_pattern, content, re.IGNORECASE | re.DOTALL)

            for form_content in forms:
                # Basic input detection
                input_pattern = r'<input[^>]*name=["']([^"']*)["'][^>]*>'
                input_names = re.findall(input_pattern, form_content, re.IGNORECASE)

                for name in input_names:
                    inputs.append({
                        'type': 'form_input',
                        'url': url,
                        'name': name,
                        'input_type': 'text'
                    })

        return inputs

    @staticmethod
    def extract_urls_from_response(content: str, base_url: str) -> List[str]:
        """Extract URLs from response content"""
        urls = set()

        if not content:
            return list(urls)

        try:
            # Parse base URL
            parsed_base = urllib.parse.urlparse(base_url)
            base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

            # URL patterns
            import re
            patterns = [
                r'href=["']([^"']*)["']',
                r'src=["']([^"']*)["']',
                r'action=["']([^"']*)["']',
                r'url\(["']([^"']*)["']\)',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if match and not match.startswith('#'):
                        # Convert relative URLs to absolute
                        if match.startswith('//'):
                            full_url = f"{parsed_base.scheme}:{match}"
                        elif match.startswith('/'):
                            full_url = f"{base_domain}{match}"
                        elif not match.startswith(('http://', 'https://')):
                            full_url = urllib.parse.urljoin(base_url, match)
                        else:
                            full_url = match

                        # Only include URLs from same domain for scope
                        if base_domain in full_url:
                            urls.add(full_url)

        except Exception:
            pass

        return list(urls)

    @staticmethod
    def detect_technologies(headers: Dict[str, str], content: str) -> List[str]:
        """Detect technologies from headers and content"""
        technologies = []

        # Check headers
        header_signatures = {
            'Server': ['nginx', 'apache', 'iis', 'cloudflare'],
            'X-Powered-By': ['php', 'asp.net', 'express'],
            'X-Generator': ['wordpress', 'drupal', 'joomla'],
            'Set-Cookie': ['PHPSESSID', 'JSESSIONID', 'ASP.NET_SessionId']
        }

        for header, signatures in header_signatures.items():
            header_value = headers.get(header, '').lower()
            for sig in signatures:
                if sig.lower() in header_value:
                    technologies.append(sig)

        # Check content
        if content:
            content_lower = content.lower()
            content_signatures = [
                ('WordPress', 'wp-content'),
                ('Drupal', 'drupal'),
                ('Joomla', 'joomla'),
                ('React', 'react'),
                ('Vue.js', 'vue'),
                ('Angular', 'angular'),
                ('jQuery', 'jquery'),
                ('Bootstrap', 'bootstrap')
            ]

            for tech, signature in content_signatures:
                if signature in content_lower:
                    technologies.append(tech)

        return list(set(technologies))
