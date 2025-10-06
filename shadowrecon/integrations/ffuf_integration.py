"""
FFUF Integration for ShadowRecon v1.0
"""

import subprocess
from typing import List, Dict, Any

class FFUFIntegration:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tool_name = "ffuf"
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if FFUF is available"""
        try:
            result = subprocess.run(['ffuf', '-h'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def run_directory_fuzzing(self, target_url: str, wordlist: str = None) -> List[Dict[str, Any]]:
        """Run FFUF directory fuzzing"""
        if not self.available:
            return []

        results = []
        wordlist = wordlist or '/usr/share/wordlists/dirb/common.txt'

        try:
            cmd = [
                'ffuf',
                '-u', f'{target_url}/FUZZ',
                '-w', wordlist,
                '-mc', '200,201,202,204,301,302,307,401,403,405',
                '-o', '/tmp/ffuf_output.json',
                '-of', 'json',
                '-t', '50'
            ]

            if self.verbose:
                print(f"[*] Running FFUF: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                # Parse FFUF JSON output
                import json
                try:
                    with open('/tmp/ffuf_output.json', 'r') as f:
                        ffuf_data = json.load(f)

                        for item in ffuf_data.get('results', []):
                            results.append({
                                'url': item.get('url'),
                                'status': item.get('status'),
                                'length': item.get('length'),
                                'words': item.get('words'),
                                'lines': item.get('lines')
                            })
                except:
                    pass

        except Exception as e:
            if self.verbose:
                print(f"[!] FFUF error: {e}")

        return results

    def run_parameter_fuzzing(self, target_url: str, wordlist: str = None) -> List[Dict[str, Any]]:
        """Run FFUF parameter fuzzing"""
        if not self.available:
            return []

        results = []
        wordlist = wordlist or '/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt'

        try:
            cmd = [
                'ffuf',
                '-u', f'{target_url}?FUZZ=test',
                '-w', wordlist,
                '-mc', '200,301,302,403,500',
                '-fs', '0',
                '-t', '50'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

            if result.returncode == 0:
                # Parse output for discovered parameters
                lines = result.stdout.split('\n')
                for line in lines:
                    if '200' in line or '302' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            param = parts[0]
                            status = parts[1] if len(parts) > 1 else 'Unknown'
                            results.append({
                                'parameter': param,
                                'status': status,
                                'url': f'{target_url}?{param}=test'
                            })

        except Exception as e:
            if self.verbose:
                print(f"[!] FFUF parameter fuzzing error: {e}")

        return results
