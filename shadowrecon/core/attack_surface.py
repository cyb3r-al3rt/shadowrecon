"""
Attack Surface Mapping Engine for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive attack surface discovery and analysis
"""

import asyncio
from typing import Dict, List, Any, Set, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AssetInfo:
    """Information about discovered assets"""
    asset_type: str
    url: str
    status_code: int = 0
    response_size: int = 0
    technologies: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    vulnerabilities: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)

@dataclass
class AttackSurface:
    """Complete attack surface representation"""
    target_domain: str
    subdomains: Set[str] = field(default_factory=set)
    endpoints: Set[str] = field(default_factory=set)
    parameters: Set[str] = field(default_factory=set)
    technologies: Set[str] = field(default_factory=set)
    assets: List[AssetInfo] = field(default_factory=list)
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    discovery_start: datetime = field(default_factory=datetime.now)
    discovery_end: Optional[datetime] = None

class AttackSurfaceMapper:
    """Advanced attack surface mapping engine"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.discovered_assets = {}
        self.attack_surface = None

    async def map_attack_surface(self, target_domain: str, 
                                 subdomains: List[str] = None,
                                 directories: List[Dict] = None,
                                 parameters: List[str] = None) -> AttackSurface:
        """Map complete attack surface for target"""

        if self.verbose:
            print(f"🗺️ Mapping attack surface for {target_domain}")

        # Initialize attack surface
        self.attack_surface = AttackSurface(target_domain=target_domain)

        # Add discovered subdomains
        if subdomains:
            self.attack_surface.subdomains.update(subdomains)

        # Add discovered endpoints
        if directories:
            for directory in directories:
                if isinstance(directory, dict) and 'url' in directory:
                    self.attack_surface.endpoints.add(directory['url'])

        # Add discovered parameters
        if parameters:
            self.attack_surface.parameters.update(parameters)

        # Analyze assets
        await self._analyze_assets()

        # Generate comprehensive mapping
        attack_surface_summary = self._generate_surface_summary()

        self.attack_surface.discovery_end = datetime.now()

        if self.verbose:
            print(f"🎯 Attack surface mapped: {len(self.attack_surface.assets)} assets")

        return self.attack_surface

    async def _analyze_assets(self):
        """Analyze discovered assets for additional information"""

        # Analyze each subdomain
        for subdomain in self.attack_surface.subdomains:
            try:
                asset_info = AssetInfo(
                    asset_type='subdomain',
                    url=f"https://{subdomain}"
                )

                # Basic technology detection placeholder
                asset_info.technologies = self._detect_basic_technologies(subdomain)

                self.attack_surface.assets.append(asset_info)
                self.attack_surface.technologies.update(asset_info.technologies)

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error analyzing subdomain {subdomain}: {e}")

        # Analyze each endpoint
        for endpoint in list(self.attack_surface.endpoints)[:20]:  # Limit analysis
            try:
                asset_info = AssetInfo(
                    asset_type='endpoint',
                    url=endpoint
                )

                self.attack_surface.assets.append(asset_info)

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error analyzing endpoint {endpoint}: {e}")

    def _detect_basic_technologies(self, domain: str) -> List[str]:
        """Basic technology detection based on domain patterns"""
        technologies = []

        domain_lower = domain.lower()

        # Common technology patterns
        tech_patterns = {
            'wordpress': ['wp', 'wordpress', 'blog'],
            'shopify': ['shop', 'store', 'shopify'],
            'aws': ['aws', 's3', 'cloudfront'],
            'cloudflare': ['cf', 'cloudflare'],
            'api': ['api', 'rest', 'graphql'],
            'admin': ['admin', 'administrator', 'manage'],
            'dev': ['dev', 'develop', 'staging', 'test']
        }

        for tech, patterns in tech_patterns.items():
            if any(pattern in domain_lower for pattern in patterns):
                technologies.append(tech)

        return technologies

    def _generate_surface_summary(self) -> Dict[str, Any]:
        """Generate attack surface summary"""

        if not self.attack_surface:
            return {}

        summary = {
            'target_domain': self.attack_surface.target_domain,
            'total_subdomains': len(self.attack_surface.subdomains),
            'total_endpoints': len(self.attack_surface.endpoints),
            'total_parameters': len(self.attack_surface.parameters),
            'total_assets': len(self.attack_surface.assets),
            'technologies_detected': list(self.attack_surface.technologies),
            'vulnerabilities_found': len(self.attack_surface.vulnerabilities),
            'discovery_duration': None
        }

        if self.attack_surface.discovery_end:
            duration = self.attack_surface.discovery_end - self.attack_surface.discovery_start
            summary['discovery_duration'] = duration.total_seconds()

        return summary

    def get_high_value_targets(self) -> List[str]:
        """Identify high-value targets from attack surface"""

        high_value = []

        if not self.attack_surface:
            return high_value

        # High-value subdomain patterns
        high_value_patterns = [
            'admin', 'administrator', 'panel', 'dashboard',
            'api', 'dev', 'staging', 'test', 'internal',
            'mail', 'webmail', 'ftp', 'vpn', 'remote'
        ]

        for subdomain in self.attack_surface.subdomains:
            subdomain_lower = subdomain.lower()
            for pattern in high_value_patterns:
                if pattern in subdomain_lower:
                    high_value.append(subdomain)
                    break

        # High-value endpoints
        high_value_endpoint_patterns = [
            '/admin', '/administrator', '/panel', '/dashboard',
            '/api', '/graphql', '/login', '/signin',
            '/upload', '/uploads', '/files', '/backup'
        ]

        for endpoint in self.attack_surface.endpoints:
            endpoint_lower = endpoint.lower()
            for pattern in high_value_endpoint_patterns:
                if pattern in endpoint_lower:
                    high_value.append(endpoint)
                    break

        return list(set(high_value))

    def get_attack_vectors(self) -> List[Dict[str, Any]]:
        """Generate potential attack vectors based on attack surface"""

        attack_vectors = []

        if not self.attack_surface:
            return attack_vectors

        # Parameter-based attack vectors
        for param in self.attack_surface.parameters:
            param_lower = param.lower()

            if any(keyword in param_lower for keyword in ['file', 'path', 'page', 'include']):
                attack_vectors.append({
                    'type': 'lfi',
                    'target': param,
                    'description': f'Potential LFI via parameter: {param}',
                    'priority': 'high'
                })

            if any(keyword in param_lower for keyword in ['url', 'redirect', 'proxy', 'fetch']):
                attack_vectors.append({
                    'type': 'ssrf',
                    'target': param,
                    'description': f'Potential SSRF via parameter: {param}',
                    'priority': 'high'
                })

            if any(keyword in param_lower for keyword in ['q', 'search', 'query', 'term']):
                attack_vectors.append({
                    'type': 'xss',
                    'target': param,
                    'description': f'Potential XSS via parameter: {param}',
                    'priority': 'medium'
                })

        # Technology-based attack vectors
        if 'wordpress' in self.attack_surface.technologies:
            attack_vectors.append({
                'type': 'cms',
                'target': 'wordpress',
                'description': 'WordPress installation detected - check for vulnerable plugins',
                'priority': 'medium'
            })

        if 'api' in self.attack_surface.technologies:
            attack_vectors.append({
                'type': 'api',
                'target': 'api_endpoints',
                'description': 'API endpoints detected - test for injection vulnerabilities',
                'priority': 'high'
            })

        return attack_vectors

    def export_attack_surface(self, format_type: str = 'dict') -> Any:
        """Export attack surface data in specified format"""

        if not self.attack_surface:
            return None

        if format_type == 'dict':
            return {
                'target_domain': self.attack_surface.target_domain,
                'subdomains': list(self.attack_surface.subdomains),
                'endpoints': list(self.attack_surface.endpoints),
                'parameters': list(self.attack_surface.parameters),
                'technologies': list(self.attack_surface.technologies),
                'assets': [
                    {
                        'type': asset.asset_type,
                        'url': asset.url,
                        'status_code': asset.status_code,
                        'technologies': asset.technologies
                    } for asset in self.attack_surface.assets
                ],
                'vulnerabilities': self.attack_surface.vulnerabilities,
                'high_value_targets': self.get_high_value_targets(),
                'attack_vectors': self.get_attack_vectors(),
                'summary': self._generate_surface_summary()
            }

        return self.attack_surface
