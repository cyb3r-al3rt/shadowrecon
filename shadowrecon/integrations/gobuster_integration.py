"""
Gobuster Integration for ShadowRecon v1.0
"""

import subprocess
from typing import List, Dict, Any

class GobusterIntegration:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tool_name = "gobuster"
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Gobuster is available"""
        try:
            result = subprocess.run(['gobuster', '--help'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def directory_bruteforce(self, target_url: str, wordlist: str = None) -> List[Dict[str, Any]]:
        """Run Gobuster directory bruteforce"""
        if not self.available:
            return []

        results = []
        wordlist = wordlist or '/usr/share/wordlists/dirb/common.txt'

        try:
            cmd = [
                'gobuster',
                'dir',
                '-u', target_url,
                '-w', wordlist,
                '-t', '50',
                '--timeout', '10s',
                '-q'  # Quiet mode
            ]

            if self.verbose:
                print(f"[*] Running Gobuster: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                results = self._parse_gobuster_output(result.stdout, target_url)

        except Exception as e:
            if self.verbose:
                print(f"[!] Gobuster error: {e}")

        return results

    def _parse_gobuster_output(self, output: str, base_url: str) -> List[Dict[str, Any]]:
        """Parse Gobuster output"""
        results = []

        lines = output.split('\n')
        for line in lines:
            line = line.strip()

            if line and not line.startswith('=') and not line.startswith('['):
                # Typical Gobuster output format: /path (Status: 200) [Size: 1234]
                if ' (Status: ' in line:
                    path = line.split(' (Status: ')[0]
                    status_part = line.split(' (Status: ')[1]
                    status = status_part.split(')')[0]

                    # Extract size if present
                    size = 0
                    if '[Size: ' in line:
                        try:
                            size_part = line.split('[Size: ')[1]
                            size = int(size_part.split(']')[0])
                        except:
                            pass

                    results.append({
                        'path': path,
                        'url': base_url.rstrip('/') + path,
                        'status': status,
                        'size': size
                    })

        return results

    def vhost_bruteforce(self, target_domain: str, wordlist: str = None) -> List[str]:
        """Run Gobuster virtual host bruteforce"""
        if not self.available:
            return []

        results = []
        wordlist = wordlist or '/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt'

        try:
            cmd = [
                'gobuster',
                'vhost',
                '-u', f'http://{target_domain}',
                '-w', wordlist,
                '-t', '50',
                '--timeout', '10s',
                '-q'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Found:' in line and target_domain in line:
                        # Extract subdomain from Gobuster vhost output
                        found_vhost = line.split('Found: ')[1].strip()
                        if found_vhost:
                            results.append(found_vhost)

        except Exception as e:
            if self.verbose:
                print(f"[!] Gobuster vhost error: {e}")

        return results
