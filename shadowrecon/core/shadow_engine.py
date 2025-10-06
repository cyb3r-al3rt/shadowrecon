"""
Main Shadow Engine for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

"In the shadows, we orchestrate the hunt. In coordination, we find victory."

This is the main orchestration engine that coordinates all ShadowRecon components
for comprehensive web attack surface discovery and vulnerability testing.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class ShadowEngine:
    """Main orchestration engine for ShadowRecon"""

    def __init__(self, 
                 output_dir: str = './shadowrecon_output',
                 threads: int = 100,
                 timeout: int = 30,
                 retries: int = 2,
                 delay: float = 0,
                 verbose: bool = False,
                 deep_mode: bool = False,
                 crawl_mode: bool = False,
                 inject_mode: bool = False,
                 passive_mode: bool = False,
                 payloads: List[str] = None,
                 wordlist_file: Optional[str] = None,
                 use_seclists: bool = False,
                 report_formats: List[str] = None,
                 user_agent: Optional[str] = None,
                 proxy: Optional[str] = None,
                 headers: Optional[str] = None,
                 cookies: Optional[str] = None,
                 enable_nuclei: bool = False,
                 enable_subfinder: bool = False,
                 enable_ffuf: bool = False,
                 enable_sqlmap: bool = False):

        self.output_dir = output_dir
        self.threads = threads
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.verbose = verbose
        self.deep_mode = deep_mode
        self.crawl_mode = crawl_mode
        self.inject_mode = inject_mode
        self.passive_mode = passive_mode
        self.payloads = payloads or []
        self.wordlist_file = wordlist_file
        self.use_seclists = use_seclists
        self.report_formats = report_formats or ['html', 'json']
        self.user_agent = user_agent
        self.proxy = proxy
        self.headers = self._parse_headers(headers)
        self.cookies = cookies
        self.enable_nuclei = enable_nuclei
        self.enable_subfinder = enable_subfinder
        self.enable_ffuf = enable_ffuf
        self.enable_sqlmap = enable_sqlmap

        # Results storage
        self.results = {
            'target': '',
            'subdomains': [],
            'directories': [],
            'parameters': [],
            'vulnerabilities': [],
            'technologies': [],
            'attack_surface': {},
            'metadata': {}
        }

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all ShadowRecon components"""
        try:
            from .attack_surface import AttackSurfaceMapper
            from .crawler import WebCrawler
            from .payload_engine import PayloadEngine
            from .reporter import ShadowReporter
            from .session_manager import SessionManager

            from ..engines.subdomain_engine import SubdomainEngine
            from ..engines.directory_engine import DirectoryEngine
            from ..engines.parameter_engine import ParameterEngine
            from ..engines.technology_detection import TechnologyDetector

            # Initialize engines
            self.subdomain_engine = SubdomainEngine(verbose=self.verbose)
            self.directory_engine = DirectoryEngine(verbose=self.verbose)
            self.parameter_engine = ParameterEngine(verbose=self.verbose)
            self.technology_detector = TechnologyDetector()

            # Initialize core components
            self.attack_surface_mapper = AttackSurfaceMapper(verbose=self.verbose)
            self.web_crawler = WebCrawler(verbose=self.verbose)
            self.payload_engine = PayloadEngine(verbose=self.verbose)
            self.reporter = ShadowReporter(output_dir=self.output_dir)

            # Initialize session manager
            session_headers = {'User-Agent': self.user_agent or 'ShadowRecon/1.0'}
            if self.headers:
                session_headers.update(self.headers)

            self.session_manager = SessionManager(
                timeout=self.timeout,
                max_connections=self.threads,
                headers=session_headers,
                proxy=self.proxy
            )

        except ImportError as e:
            if self.verbose:
                print(f"[!] Component initialization error: {e}")
            # Create minimal fallback components
            self._create_fallback_components()

    def _create_fallback_components(self):
        """Create minimal fallback components"""

        class FallbackComponent:
            def __init__(self, verbose=False):
                self.verbose = verbose

        self.subdomain_engine = FallbackComponent(self.verbose)
        self.directory_engine = FallbackComponent(self.verbose)
        self.parameter_engine = FallbackComponent(self.verbose)
        self.technology_detector = FallbackComponent(self.verbose)
        self.attack_surface_mapper = FallbackComponent(self.verbose)
        self.web_crawler = FallbackComponent(self.verbose)
        self.payload_engine = FallbackComponent(self.verbose)
        self.reporter = FallbackComponent(self.verbose)
        self.session_manager = FallbackComponent(self.verbose)

    def _parse_headers(self, headers_str: Optional[str]) -> Dict[str, str]:
        """Parse headers string into dictionary"""
        headers = {}
        if headers_str:
            try:
                pairs = headers_str.split(',')
                for pair in pairs:
                    if ':' in pair:
                        key, value = pair.split(':', 1)
                        headers[key.strip()] = value.strip()
            except Exception as e:
                if self.verbose:
                    print(f"[!] Header parsing error: {e}")
        return headers

    async def discover_attack_surface(self, target_domain: str) -> Dict[str, Any]:
        """Main attack surface discovery workflow"""

        if self.verbose:
            print(f"\n🎭 SHADOWRECON v1.0 - ATTACK SURFACE DISCOVERY")
            print(f"🎯 Target: {target_domain}")
            print(f"💀 'In the shadows, the hunt begins...'")
            print(f"🔧 Developed by kernelpanic | A product of infosbios\n")

        self.results['target'] = target_domain
        self.results['metadata'] = {
            'scan_start': datetime.now(),
            'deep_mode': self.deep_mode,
            'crawl_mode': self.crawl_mode,
            'inject_mode': self.inject_mode,
            'threads': self.threads,
            'timeout': self.timeout
        }

        try:
            # Initialize session
            async with self.session_manager as session_mgr:
                session = session_mgr.get_session() if session_mgr else None

                # Phase 1: Attack Surface Mapping
                if self.verbose:
                    print("🗺️ [PHASE 1] Attack Surface Mapping")

                await self._discover_subdomains(target_domain)
                await self._discover_directories(target_domain, session)
                await self._discover_parameters(target_domain, session)

                # Phase 2: Technology Detection
                if self.verbose:
                    print("🔍 [PHASE 2] Technology Stack Detection")

                await self._detect_technologies(target_domain, session)

                # Phase 3: Web Crawling (if enabled)
                if self.crawl_mode:
                    if self.verbose:
                        print("🕷️ [PHASE 3] Web Crawling and Form Detection")

                    await self._crawl_target(target_domain, session)

                # Phase 4: Vulnerability Testing (if enabled)
                if self.inject_mode:
                    if self.verbose:
                        print("💉 [PHASE 4] Payload Injection and Vulnerability Testing")

                    await self._test_vulnerabilities(session)

                # Phase 5: External Tool Integration
                if any([self.enable_nuclei, self.enable_subfinder, self.enable_ffuf]):
                    if self.verbose:
                        print("🔧 [PHASE 5] External Tool Integration")

                    await self._run_external_tools(target_domain)

        except Exception as e:
            if self.verbose:
                print(f"[!] Attack surface discovery error: {e}")

        # Final processing
        self.results['metadata']['scan_end'] = datetime.now()

        # Generate attack surface map
        if hasattr(self.attack_surface_mapper, 'map_attack_surface'):
            attack_surface = await self.attack_surface_mapper.map_attack_surface(
                target_domain,
                self.results.get('subdomains', []),
                self.results.get('directories', []),
                self.results.get('parameters', [])
            )
            self.results['attack_surface'] = attack_surface

        # Generate reports
        if self.verbose:
            print("📊 [PHASE 6] Report Generation")

        generated_reports = {}
        if hasattr(self.reporter, 'generate_all_reports'):
            generated_reports = self.reporter.generate_all_reports(
                self.results, target_domain, self.report_formats
            )

        # Display summary
        self._display_summary(generated_reports)

        return self.results

    async def _discover_subdomains(self, target_domain: str):
        """Discover subdomains using multiple techniques"""
        try:
            if hasattr(self.subdomain_engine, 'discover_subdomains'):
                subdomains = await self.subdomain_engine.discover_subdomains(
                    target_domain, 
                    deep_mode=self.deep_mode,
                    use_seclists=self.use_seclists,
                    enable_subfinder=self.enable_subfinder
                )
                self.results['subdomains'] = subdomains

                if self.verbose:
                    print(f"[+] Found {len(subdomains)} subdomains")
        except Exception as e:
            if self.verbose:
                print(f"[!] Subdomain discovery error: {e}")

    async def _discover_directories(self, target_domain: str, session):
        """Discover directories using wordlist enumeration"""
        try:
            base_url = f"https://{target_domain}"

            if hasattr(self.directory_engine, 'discover_directories'):
                directories = await self.directory_engine.discover_directories(
                    base_url, 
                    session,
                    deep_mode=self.deep_mode,
                    use_seclists=self.use_seclists
                )
                self.results['directories'] = directories

                if self.verbose:
                    print(f"[+] Found {len(directories)} directories")
        except Exception as e:
            if self.verbose:
                print(f"[!] Directory discovery error: {e}")

    async def _discover_parameters(self, target_domain: str, session):
        """Discover parameters using multiple techniques"""
        try:
            if hasattr(self.parameter_engine, 'discover_parameters'):
                parameters = await self.parameter_engine.discover_parameters(
                    target_domain,
                    session,
                    deep_mode=self.deep_mode
                )
                self.results['parameters'] = parameters

                if self.verbose:
                    print(f"[+] Found {len(parameters)} parameters")
        except Exception as e:
            if self.verbose:
                print(f"[!] Parameter discovery error: {e}")

    async def _detect_technologies(self, target_domain: str, session):
        """Detect technologies used by target"""
        try:
            base_url = f"https://{target_domain}"

            # Make request to get content and headers
            if session:
                from ..utils.http_utils import HTTPUtils
                response = await HTTPUtils.safe_request(session, 'GET', base_url)

                if response:
                    content = response.get('content', '')
                    headers = response.get('headers', {})

                    if hasattr(self.technology_detector, 'detect_technologies'):
                        technologies = self.technology_detector.detect_technologies(content, headers)
                        self.results['technologies'] = technologies

                        if self.verbose:
                            print(f"[+] Detected {len(technologies)} technologies: {', '.join(technologies)}")
        except Exception as e:
            if self.verbose:
                print(f"[!] Technology detection error: {e}")

    async def _crawl_target(self, target_domain: str, session):
        """Crawl target for forms and inputs"""
        try:
            base_url = f"https://{target_domain}"

            if hasattr(self.web_crawler, 'crawl_domain'):
                crawled_pages = await self.web_crawler.crawl_domain(base_url, session)

                # Extract additional data from crawl
                if hasattr(self.web_crawler, 'discovered_forms'):
                    forms = getattr(self.web_crawler, 'discovered_forms', [])
                    inputs = getattr(self.web_crawler, 'discovered_inputs', [])
                    discovered_params = getattr(self.web_crawler, 'discovered_parameters', set())

                    # Merge with existing results
                    self.results['parameters'].extend(list(discovered_params))
                    self.results['parameters'] = list(set(self.results['parameters']))  # Deduplicate

                    if self.verbose:
                        print(f"[+] Crawled {len(crawled_pages)} pages, found {len(forms)} forms, {len(inputs)} inputs")
        except Exception as e:
            if self.verbose:
                print(f"[!] Web crawling error: {e}")

    async def _test_vulnerabilities(self, session):
        """Test for vulnerabilities using payloads"""
        try:
            vulnerabilities = []

            # Test endpoints discovered during reconnaissance
            test_endpoints = []

            # Add directories as test endpoints
            for directory in self.results.get('directories', []):
                if isinstance(directory, dict) and 'url' in directory:
                    test_endpoints.append({
                        'url': directory['url'],
                        'method': 'GET'
                    })

            # Add main domain endpoints
            target = self.results.get('target', '')
            if target:
                test_endpoints.append({
                    'url': f"https://{target}",
                    'method': 'GET'
                })

                # Add common parameter testing
                for param in self.results.get('parameters', []):
                    test_endpoints.append({
                        'url': f"https://{target}?{param}=test",
                        'method': 'GET'
                    })

            # Test each payload type
            for payload_type in self.payloads:
                if self.verbose:
                    print(f"[*] Testing {payload_type.upper()} payloads...")

                # Load appropriate hunter module
                try:
                    hunter = self._load_vulnerability_hunter(payload_type)

                    if hunter:
                        for endpoint in test_endpoints[:10]:  # Limit endpoints for performance
                            try:
                                found_vulns = await hunter.test_endpoint(endpoint, session)
                                vulnerabilities.extend(found_vulns)

                                if found_vulns and self.verbose:
                                    print(f"[!] Found {len(found_vulns)} {payload_type} vulnerabilities")

                            except Exception as e:
                                if self.verbose:
                                    print(f"[!] Vulnerability testing error for {endpoint.get('url', 'unknown')}: {e}")
                                continue

                except ImportError:
                    if self.verbose:
                        print(f"[!] Could not load {payload_type} hunter")

            self.results['vulnerabilities'] = vulnerabilities

            if self.verbose:
                print(f"[+] Total vulnerabilities found: {len(vulnerabilities)}")

        except Exception as e:
            if self.verbose:
                print(f"[!] Vulnerability testing error: {e}")

    def _load_vulnerability_hunter(self, payload_type: str):
        """Load appropriate vulnerability hunter"""
        try:
            if payload_type.lower() == 'xss':
                from ..modules.xss_hunter import XSSHunter
                return XSSHunter(verbose=self.verbose)
            elif payload_type.lower() == 'lfi':
                from ..modules.lfi_hunter import LFIHunter
                return LFIHunter(verbose=self.verbose)
            elif payload_type.lower() == 'ssrf':
                from ..modules.ssrf_hunter import SSRFHunter
                return SSRFHunter(verbose=self.verbose)
            elif payload_type.lower() == 'sqli':
                from ..modules.sqli_hunter import SQLiHunter
                return SQLiHunter(verbose=self.verbose)
        except ImportError:
            pass

        return None

    async def _run_external_tools(self, target_domain: str):
        """Run external security tools"""
        try:
            if self.enable_nuclei:
                if self.verbose:
                    print("[*] Running Nuclei templates...")
                # Nuclei integration would go here

            if self.enable_subfinder:
                if self.verbose:
                    print("[*] Running Subfinder...")
                # Subfinder integration would go here

            if self.enable_ffuf:
                if self.verbose:
                    print("[*] Running FFUF...")
                # FFUF integration would go here

        except Exception as e:
            if self.verbose:
                print(f"[!] External tool error: {e}")

    async def discover_multiple_targets(self, targets: List[str]):
        """Discover attack surface for multiple targets"""
        if self.verbose:
            print(f"🎯 Processing {len(targets)} targets...")

        all_results = []

        for i, target in enumerate(targets, 1):
            if self.verbose:
                print(f"\n[{i}/{len(targets)}] Processing {target}...")

            try:
                result = await self.discover_attack_surface(target)
                all_results.append(result)

                # Add delay between targets if specified
                if self.delay > 0 and i < len(targets):
                    await asyncio.sleep(self.delay)

            except Exception as e:
                if self.verbose:
                    print(f"[!] Error processing {target}: {e}")
                continue

        return all_results

    def _display_summary(self, generated_reports: Dict[str, str]):
        """Display scan summary"""
        if not self.verbose:
            return

        print("\n" + "="*80)
        print("🎭 SHADOWRECON SCAN SUMMARY")
        print("="*80)

        target = self.results.get('target', 'Unknown')
        subdomains = len(self.results.get('subdomains', []))
        directories = len(self.results.get('directories', []))
        parameters = len(self.results.get('parameters', []))
        vulnerabilities = len(self.results.get('vulnerabilities', []))
        technologies = len(self.results.get('technologies', []))

        print(f"🎯 Target: {target}")
        print(f"🌐 Subdomains Found: {subdomains}")
        print(f"📁 Directories Found: {directories}")
        print(f"🔍 Parameters Found: {parameters}")
        print(f"🛡️ Technologies Detected: {technologies}")

        if vulnerabilities > 0:
            print(f"🚨 VULNERABILITIES FOUND: {vulnerabilities}")
        else:
            print("✅ No vulnerabilities detected")

        print("\n📊 GENERATED REPORTS:")
        for format_type, filepath in generated_reports.items():
            print(f"   {format_type.upper()}: {filepath}")

        # Calculate scan duration
        metadata = self.results.get('metadata', {})
        if 'scan_start' in metadata and 'scan_end' in metadata:
            duration = metadata['scan_end'] - metadata['scan_start']
            print(f"\n⏱️ Scan Duration: {duration.total_seconds():.1f} seconds")

        print("\n💀 'In the shadows, the hunt is complete. The attack surface has been mapped.'")
        print("🎭 Developed by kernelpanic | A product of infosbios")
        print("="*80)
