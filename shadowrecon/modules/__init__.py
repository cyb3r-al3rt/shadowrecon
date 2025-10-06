"""Vulnerability detection modules"""
try:
    from .xss_hunter import XSSHunter
    from .lfi_hunter import LFIHunter
    from .ssrf_hunter import SSRFHunter
    from .sqli_hunter import SQLiHunter
    __all__ = ['XSSHunter', 'LFIHunter', 'SSRFHunter', 'SQLiHunter']
except ImportError:
    __all__ = []
