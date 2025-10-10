"""ShadowRecon vulnerability detection modules"""

try:
    from .xss_hunter import XSSHunter
    from .lfi_hunter import LFIHunter
    from .ssrf_hunter import SSRFHunter
    from .sqli_hunter import SQLiHunter
    from .graphql_hunter import GraphQLHunter
    from .s3_hunter import S3Hunter
    from .rce_hunter import RCEHunter
    from .xxe_hunter import XXEHunter

    __all__ = [
        'XSSHunter',
        'LFIHunter',
        'SSRFHunter',
        'SQLiHunter',
        'GraphQLHunter',
        'S3Hunter',
        'RCEHunter',
        'XXEHunter'
    ]
except ImportError:
    __all__ = []
