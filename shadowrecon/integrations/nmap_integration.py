"""
Nmap Integration for ShadowRecon v1.0
"""

import subprocess
from typing import List, Dict, Any

class NmapIntegration:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.tool_name = "nmap"
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Nmap is available"""
        try:
            result = subprocess.run(['nmap', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def scan_ports(self, target: str, ports: str = '1-1000') -> List[Dict[str, Any]]:
        """Scan ports using Nmap"""
        if not self.available:
            return []

        results = []

        try:
            cmd = [
                'nmap',
                '-p', ports,
                '--open',
                '-T4',
                '-oG', '-',  # Greppable output
                target
            ]

            if self.verbose:
                print(f"[*] Running Nmap: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                results = self._parse_nmap_output(result.stdout, target)

        except Exception as e:
            if self.verbose:
                print(f"[!] Nmap error: {e}")

        return results

    def _parse_nmap_output(self, output: str, target: str) -> List[Dict[str, Any]]:
        """Parse Nmap greppable output"""
        results = []

        lines = output.split('\n')
        for line in lines:
            if 'Ports:' in line and '/open/' in line:
                # Extract port information
                ports_section = line.split('Ports: ')[1]
                port_entries = ports_section.split(', ')

                for entry in port_entries:
                    if '/open/' in entry:
                        parts = entry.split('/')
                        if len(parts) >= 3:
                            port = parts[0]
                            service = parts[4] if len(parts) > 4 else 'unknown'

                            results.append({
                                'host': target,
                                'port': int(port),
                                'state': 'open',
                                'service': service
                            })

        return results

    def service_detection(self, target: str, ports: List[int]) -> List[Dict[str, Any]]:
        """Perform service detection on specific ports"""
        if not self.available or not ports:
            return []

        results = []
        port_list = ','.join(map(str, ports))

        try:
            cmd = [
                'nmap',
                '-p', port_list,
                '-sV',  # Service detection
                '--version-intensity', '1',
                '-T4',
                target
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

            if result.returncode == 0:
                results = self._parse_service_output(result.stdout, target)

        except Exception as e:
            if self.verbose:
                print(f"[!] Nmap service detection error: {e}")

        return results

    def _parse_service_output(self, output: str, target: str) -> List[Dict[str, Any]]:
        """Parse Nmap service detection output"""
        results = []

        lines = output.split('\n')
        for line in lines:
            line = line.strip()

            # Look for port lines (format: PORT   STATE SERVICE VERSION)
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 3 and parts[1] == 'open':
                    port_info = parts[0].split('/')
                    port = int(port_info[0])
                    protocol = port_info[1]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    version = ' '.join(parts[3:]) if len(parts) > 3 else ''

                    results.append({
                        'host': target,
                        'port': port,
                        'protocol': protocol,
                        'service': service,
                        'version': version
                    })

        return results
