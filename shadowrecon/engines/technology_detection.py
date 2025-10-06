"""
Technology Detection Engine for ShadowRecon v1.0
"""

from typing import Dict, List, Any

class TechnologyDetector:
    def __init__(self):
        self.signatures = {
            'cms': {
                'wordpress': ['wp-content', 'wp-includes', 'wp-admin'],
                'drupal': ['/sites/default/', '/modules/', 'drupal'],
                'joomla': ['/templates/', '/components/', 'joomla']
            },
            'frameworks': {
                'react': ['react', 'reactjs', '_react'],
                'vue': ['vue.js', 'vue', '__vue__'],
                'angular': ['angular', 'ng-app', 'ng-controller']
            },
            'servers': {
                'apache': ['apache', 'server: apache'],
                'nginx': ['nginx', 'server: nginx'],
                'iis': ['iis', 'server: microsoft-iis']
            },
            'languages': {
                'php': ['<?php', '.php', 'x-powered-by: php'],
                'python': ['django', 'flask'],
                'java': ['.jsp', 'jsessionid', 'java'],
                'asp.net': ['.aspx', '__viewstate', 'x-powered-by: asp.net']
            }
        }

    def detect_technologies(self, content: str, headers: Dict[str, str] = None) -> List[str]:
        """Detect technologies from content and headers"""
        detected = []
        content_lower = content.lower()

        # Header-based detection
        if headers:
            headers_str = ' '.join([f"{k}: {v}" for k, v in headers.items()]).lower()
            content_lower += ' ' + headers_str

        # Check signatures
        for category, techs in self.signatures.items():
            for tech, signatures in techs.items():
                if any(sig.lower() in content_lower for sig in signatures):
                    detected.append(tech)

        return list(set(detected))

    def get_technology_info(self, technology: str) -> Dict[str, Any]:
        """Get information about detected technology"""
        tech_info = {
            'wordpress': {
                'type': 'CMS',
                'description': 'Popular content management system',
                'common_vulns': ['Plugin vulnerabilities', 'Theme vulnerabilities', 'Weak passwords']
            },
            'php': {
                'type': 'Language',
                'description': 'Server-side scripting language',
                'common_vulns': ['Code injection', 'File inclusion', 'SQL injection']
            },
            'apache': {
                'type': 'Web Server',
                'description': 'Apache HTTP Server',
                'common_vulns': ['Server-side includes', 'Directory traversal', 'Module vulnerabilities']
            }
        }

        return tech_info.get(technology, {
            'type': 'Unknown',
            'description': f'Detected technology: {technology}',
            'common_vulns': []
        })
