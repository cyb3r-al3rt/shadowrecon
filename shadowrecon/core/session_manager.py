"""
Session Manager for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced HTTP session management with connection pooling
"""

import asyncio
from typing import Dict, Optional, Any

# Handle optional aiohttp import
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

class SessionManager:
    """Advanced HTTP session manager"""

    def __init__(self, 
                 timeout: int = 30,
                 max_connections: int = 100,
                 headers: Optional[Dict[str, str]] = None,
                 proxy: Optional[str] = None,
                 verify_ssl: bool = False):

        self.timeout = timeout
        self.max_connections = max_connections
        self.headers = headers or {}
        self.proxy = proxy
        self.verify_ssl = verify_ssl
        self.session = None

        # Default headers
        default_headers = {
            'User-Agent': 'ShadowRecon/1.0 (Ultimate Web Attack Surface Discovery Framework)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Merge with custom headers
        for key, value in default_headers.items():
            if key not in self.headers:
                self.headers[key] = value

    async def create_session(self) -> Optional[Any]:
        """Create aiohttp session with configuration"""

        if not AIOHTTP_AVAILABLE:
            return None

        try:
            # Create connector with configuration
            connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                limit_per_host=20,
                ssl=False if not self.verify_ssl else None,
                enable_cleanup_closed=True
            )

            # Create client timeout
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            # Create session
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=self.headers,
                trust_env=True
            )

            return self.session

        except Exception:
            return None

    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            try:
                await self.session.close()
            except Exception:
                pass
            finally:
                self.session = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_session()

    def get_session(self):
        """Get current session"""
        return self.session
