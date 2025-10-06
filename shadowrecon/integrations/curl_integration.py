"""
Curl Integration for ShadowRecon v1.0
"""

import subprocess
from typing import List, Dict, Any, Optional

class CurlIntegration:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tool_name = "curl"
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if curl is available"""
        try:
            result = subprocess.run(['curl', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def make_request(self, url: str, method: str = 'GET', 
                    headers: Dict[str, str] = None,
                    data: str = None,
                    timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Make HTTP request using curl"""
        if not self.available:
            return None

        try:
            cmd = [
                'curl',
                '-X', method,
                '--max-time', str(timeout),
                '--connect-timeout', '10',
                '-L',  # Follow redirects
                '-k',  # Ignore SSL errors
                '-s',  # Silent
                '-i',  # Include headers in output
                url
            ]

            # Add custom headers
            if headers:
                for key, value in headers.items():
                    cmd.extend(['-H', f'{key}: {value}'])

            # Add data for POST requests
            if data and method.upper() in ['POST', 'PUT', 'PATCH']:
                cmd.extend(['--data', data])

            if self.verbose:
                print(f"[*] Running curl: {' '.join(cmd[:5])}...")  # Don't show full command for security

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            if result.returncode == 0:
                return self._parse_curl_output(result.stdout, url)

        except Exception as e:
            if self.verbose:
                print(f"[!] Curl error: {e}")

        return None

    def _parse_curl_output(self, output: str, url: str) -> Dict[str, Any]:
        """Parse curl output"""
        lines = output.split('\n')

        # Parse HTTP status line
        status_code = 0
        headers = {}
        content = ""

        parsing_headers = True
        for i, line in enumerate(lines):
            if i == 0 and line.startswith('HTTP/'):
                # Parse status line
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        status_code = int(parts[1])
                    except:
                        pass
            elif parsing_headers and line.strip():
                # Parse headers
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            elif not line.strip() and parsing_headers:
                # Empty line separates headers from content
                parsing_headers = False
            elif not parsing_headers:
                # Content
                content += line + '\n'

        return {
            'url': url,
            'status_code': status_code,
            'headers': headers,
            'content': content.strip(),
            'content_length': len(content.strip())
        }

    def test_http_methods(self, url: str) -> List[str]:
        """Test which HTTP methods are allowed"""
        if not self.available:
            return []

        allowed_methods = []
        methods_to_test = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

        for method in methods_to_test:
            try:
                cmd = [
                    'curl',
                    '-X', method,
                    '--max-time', '10',
                    '-s', '-o', '/dev/null', '-w', '%{http_code}',
                    '-k',
                    url
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

                if result.returncode == 0:
                    status_code = result.stdout.strip()
                    # Consider method allowed if it doesn't return 405 (Method Not Allowed)
                    if status_code and status_code != '405':
                        allowed_methods.append(method)

            except Exception:
                continue

        return allowed_methods
