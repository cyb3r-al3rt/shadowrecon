"""Payload collections"""
try:
    from .xss_payloads import XSSPayloads
    from .lfi_payloads import LFIPayloads
    from .ssrf_payloads import SSRFPayloads
    from .sqli_payloads import SQLiPayloads
    __all__ = ['XSSPayloads', 'LFIPayloads', 'SSRFPayloads', 'SQLiPayloads']
except ImportError:
    __all__ = []
