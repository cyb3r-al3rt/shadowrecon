"""
Port Scanning Engine for ShadowRecon v1.0
"""

import asyncio
import socket
from typing import List, Dict, Any

class PortEngine:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]

    async def scan_ports(self, host: str, ports: List[int] = None) -> List[Dict[str, Any]]:
        """Scan ports on target host"""
        if not ports:
            ports = self.common_ports

        open_ports = []

        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((host, port))

                if result == 0:
                    service = self._identify_service(port)
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'host': host
                    })

                    if self.verbose:
                        print(f"[+] Open port: {host}:{port} ({service})")

                sock.close()

            except Exception:
                continue

        return open_ports

    def _identify_service(self, port: int) -> str:
        """Identify service by port number"""
        services = {
            21: 'FTP',
            22: 'SSH', 
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            135: 'RPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1723: 'PPTP',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8080: 'HTTP-Proxy'
        }
        return services.get(port, 'Unknown')
