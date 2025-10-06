"""
Configuration Manager for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced configuration management system
"""

import os
import json
from typing import Dict, Any, Optional

class ConfigManager:
    """Advanced configuration manager"""

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_default_config()
        self.config = self._load_default_config()

        if self.config_file and os.path.exists(self.config_file):
            self._load_config_file()

    def _find_default_config(self) -> str:
        """Find default configuration file"""
        possible_paths = [
            './shadowrecon.conf',
            './config/shadowrecon.conf',
            '/etc/shadowrecon/shadowrecon.conf',
            os.path.expanduser('~/.shadowrecon/config'),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return './shadowrecon.conf'

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            'general': {
                'version': '1.0.0',
                'author': 'kernelpanic | A product of infosbios',
                'debug': False
            },
            'scanning': {
                'default_threads': 100,
                'default_timeout': 30,
                'max_retries': 3,
                'deep_mode': False,
                'crawl_mode': False,
                'inject_mode': False
            },
            'payloads': {
                'enable_xss': True,
                'enable_lfi': True,
                'enable_ssrf': True,
                'enable_sqli': True,
                'enable_rce': False,
                'enable_xxe': False
            },
            'output': {
                'default_formats': ['html', 'json'],
                'save_screenshots': False,
                'save_raw_responses': False,
                'output_directory': './shadowrecon_output'
            },
            'wordlists': {
                'use_seclists': True,
                'custom_wordlists_dir': './wordlists',
                'subdomain_wordlist': 'subdomains-top1million-5000.txt',
                'directory_wordlist': 'directory-list-2.3-medium.txt'
            },
            'external_tools': {
                'nuclei_enabled': False,
                'subfinder_enabled': False,
                'ffuf_enabled': False,
                'sqlmap_enabled': False
            },
            'http': {
                'user_agent': 'ShadowRecon/1.0',
                'verify_ssl': False,
                'follow_redirects': True,
                'max_redirects': 5
            }
        }

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config.get(section, {})
