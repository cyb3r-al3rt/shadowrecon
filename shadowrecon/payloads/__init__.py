"""ShadowRecon payload collections"""

try:
    from .xss_payloads import XSSPayloads
    from .lfi_payloads import LFIPayloads
    from .ssrf_payloads import SSRFPayloads
    from .sqli_payloads import SQLiPayloads
    from .rce_payloads import RCEPayloads
    from .xxe_payloads import XXEPayloads

    __all__ = [
        'XSSPayloads',
        'LFIPayloads',
        'SSRFPayloads',
        'SQLiPayloads', 
        'RCEPayloads',
        'XXEPayloads'
    ]
except ImportError:
    __all__ = []
