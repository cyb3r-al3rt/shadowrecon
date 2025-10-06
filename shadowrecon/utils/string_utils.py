"""
String utilities for ShadowRecon v1.0
"""

import re
import random
import string

class StringUtils:
    @staticmethod
    def clean_domain(domain: str) -> str:
        """Clean and normalize domain"""
        domain = domain.strip().lower()
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.split('/')[0]
        return domain

    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @staticmethod
    def extract_domain_from_url(url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url

    @staticmethod
    def is_subdomain(potential_sub: str, parent_domain: str) -> bool:
        """Check if potential_sub is a subdomain of parent_domain"""
        return potential_sub.endswith('.' + parent_domain) or potential_sub == parent_domain

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove or replace unsafe characters
        filename = re.sub(r'[<>:"/\|?*]', '_', filename)
        filename = filename.replace('..', '_')
        return filename[:100]  # Limit length
