"""
Advanced input validation utilities for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive validation for domains, URLs, payloads, and attack surfaces
"""

import re
import urllib.parse
from typing import Union, Optional, List
import ipaddress

def validate_domain(domain: str) -> bool:
    """Validate domain name format with advanced checks"""
    if not domain or not isinstance(domain, str):
        return False

    try:
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '').strip('/')

        # Remove port if present
        if ':' in domain and not _is_ipv6(domain):
            domain = domain.split(':')[0]

        # Check for IPv4 address
        if _is_ipv4(domain):
            return True

        # Check for IPv6 address  
        if _is_ipv6(domain):
            return True

        # Advanced domain name validation
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'
            r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )

        # Single label domains (like localhost)
        single_label_pattern = re.compile(r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$')

        # Wildcard domain support
        wildcard_pattern = re.compile(r'^\*\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\..*')

        return bool(domain_pattern.match(domain) or 
                   single_label_pattern.match(domain) or
                   wildcard_pattern.match(domain))

    except Exception:
        return False

def validate_url(url: str) -> bool:
    """Validate URL format with advanced scheme support"""
    if not url or not isinstance(url, str):
        return False

    try:
        result = urllib.parse.urlparse(url)
        return all([
            result.scheme in ['http', 'https', 'ftp', 'ftps', 'file', 'ws', 'wss'],
            result.netloc or result.path
        ])
    except Exception:
        return False

def validate_ip(ip: str) -> bool:
    """Validate IP address (IPv4 or IPv6)"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_cidr(cidr: str) -> bool:
    """Validate CIDR notation"""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def validate_payload(payload: str, payload_type: str = 'generic') -> bool:
    """Validate payload format and safety"""
    if not payload or not isinstance(payload, str):
        return False

    # Check payload length
    if len(payload) > 10000:  # Max payload length
        return False

    # Basic XSS payload validation
    if payload_type.lower() == 'xss':
        xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<img[^>]*onerror',
            r'<svg[^>]*onload'
        ]
        return any(re.search(pattern, payload, re.IGNORECASE) for pattern in xss_patterns)

    # Basic SQLi payload validation
    elif payload_type.lower() == 'sqli':
        sqli_patterns = [
            r"'.*OR.*'",
            r"UNION\s+SELECT",
            r"INSERT\s+INTO",
            r"DROP\s+TABLE",
            r"--\s*$"
        ]
        return any(re.search(pattern, payload, re.IGNORECASE) for pattern in sqli_patterns)

    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    if not filename or not isinstance(filename, str):
        return "unknown"

    try:
        # Remove or replace unsafe characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[\x00-\x1f]', '', filename)  # Remove control characters
        filename = filename.strip('. ')  # Remove leading/trailing dots and spaces

        # Handle reserved names on Windows
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
            'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4',
            'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }

        name_without_ext = filename.split('.')[0].upper()
        if name_without_ext in reserved_names:
            filename = f"shadow_{filename}"

        return filename[:200] if filename else "unknown"

    except Exception:
        return "unknown"

def sanitize_payload(payload: str) -> str:
    """Sanitize payload for safe logging and reporting"""
    if not payload or not isinstance(payload, str):
        return ""

    try:
        # Escape HTML entities
        payload = payload.replace('&', '&amp;')
        payload = payload.replace('<', '&lt;')
        payload = payload.replace('>', '&gt;')
        payload = payload.replace('"', '&quot;')
        payload = payload.replace("'", '&#x27;')

        # Truncate if too long
        if len(payload) > 1000:
            payload = payload[:997] + "..."

        return payload

    except Exception:
        return ""

def validate_port(port: Union[str, int]) -> bool:
    """Validate port number"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False

def clean_domain(domain: str) -> str:
    """Clean and normalize domain input"""
    if not domain or not isinstance(domain, str):
        return ""

    try:
        # Remove protocol and trailing slashes
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.strip('/')

        # Remove port if present (but not for IPv6)
        if ':' in domain and not _is_ipv6(domain):
            domain = domain.split(':')[0]

        return domain.lower()
    except Exception:
        return ""

def normalize_url(url: str) -> str:
    """Normalize URL format"""
    if not url or not isinstance(url, str):
        return ""

    try:
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"

        # Remove trailing slash except for root
        if url.endswith('/') and url.count('/') > 3:
            url = url.rstrip('/')

        return url
    except Exception:
        return ""

def extract_domains_from_text(text: str) -> List[str]:
    """Extract domains from text using regex"""
    if not text or not isinstance(text, str):
        return []

    try:
        domain_pattern = re.compile(
            r'(?:https?://)?(?:www\.)?([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'
            r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
        )

        domains = domain_pattern.findall(text)
        return [domain for domain in domains if validate_domain(domain)]

    except Exception:
        return []

def _is_ipv4(address: str) -> bool:
    """Check if string is valid IPv4 address"""
    try:
        parts = address.split('.')
        if len(parts) != 4:
            return False

        for part in parts:
            if not (0 <= int(part) <= 255):
                return False

        return True
    except (ValueError, AttributeError, TypeError):
        return False

def _is_ipv6(address: str) -> bool:
    """Check if string is valid IPv6 address"""
    try:
        import socket
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except (socket.error, AttributeError, OSError):
        return False
