"""
Network utilities for ShadowRecon v1.0
"""

import socket
try:
    import ipaddress
except ImportError:
    ipaddress = None

class NetworkUtils:
    @staticmethod
    def resolve_domain(domain: str) -> str:
        try:
            return socket.gethostbyname(domain)
        except:
            return ""

    @staticmethod
    def is_private_ip(ip: str) -> bool:
        if not ipaddress:
            return False
        try:
            return ipaddress.ip_address(ip).is_private
        except:
            return False

    @staticmethod
    def check_port(host: str, port: int, timeout: int = 3) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
