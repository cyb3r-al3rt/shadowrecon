"""
SQLMap Integration for ShadowRecon v1.0
"""

import subprocess
from typing import List, Dict, Any

class SQLMapIntegration:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tool_name = "sqlmap"
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if SQLMap is available"""
        try:
            result = subprocess.run(['sqlmap', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def test_sql_injection(self, target_url: str, parameters: List[str] = None) -> List[Dict[str, Any]]:
        """Test URL for SQL injection using SQLMap"""
        if not self.available:
            return []

        results = []

        try:
            cmd = [
                'sqlmap',
                '-u', target_url,
                '--batch',
                '--random-agent',
                '--level', '1',
                '--risk', '1',
                '--threads', '5',
                '--timeout', '30'
            ]

            if parameters:
                cmd.extend(['-p', ','.join(parameters)])

            if self.verbose:
                print(f"[*] Running SQLMap: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Parse SQLMap output for vulnerabilities
            if 'is vulnerable' in result.stdout or 'sqlmap identified' in result.stdout:
                vulnerability_info = self._parse_sqlmap_output(result.stdout, target_url)
                if vulnerability_info:
                    results.append(vulnerability_info)

        except subprocess.TimeoutExpired:
            if self.verbose:
                print("[!] SQLMap timeout")
        except Exception as e:
            if self.verbose:
                print(f"[!] SQLMap error: {e}")

        return results

    def _parse_sqlmap_output(self, output: str, target_url: str) -> Dict[str, Any]:
        """Parse SQLMap output for vulnerability information"""
        vulnerability = {
            'type': 'sql_injection',
            'severity': 'critical',
            'url': target_url,
            'tool': 'sqlmap',
            'details': {}
        }

        lines = output.split('\n')
        for line in lines:
            line = line.strip()

            if 'Parameter:' in line:
                vulnerability['details']['parameter'] = line.split('Parameter:')[1].strip()
            elif 'Type:' in line:
                vulnerability['details']['injection_type'] = line.split('Type:')[1].strip()
            elif 'Payload:' in line:
                vulnerability['details']['payload'] = line.split('Payload:')[1].strip()

        return vulnerability
