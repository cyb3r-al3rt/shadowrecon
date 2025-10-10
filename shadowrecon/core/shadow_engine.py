"""
ShadowRecon Core Engine v1.0
Developed by kernelpanic | A product of infosbios

The main orchestration engine that coordinates all attack surface discovery activities
"""

import asyncio
import time
from typing import Dict, List, Any, Optional

# Import with fallback handling
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

class ShadowEngine:
    """Main orchestration engine for ShadowRecon"""

    def __init__(self, 
                 output_dir: str = "./shadowrecon_output",
                 threads: int = 100,
                 timeout: int = 30,
                 retries: int = 2,
                 delay: float = 0,
                 verbose: bool = False,
                 deep_mode: bool = False,
                 crawl_mode: bool = False,
                 inject_mode: bool = False,
                 passive_mode: bool = False,
                 payloads: Optional[List[str]] = None,
                 wordlist_file: Optional[str] = None,
                 use_seclists: bool = False,
                 report_formats: List[str] = ['html', 'json'],
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
        self.payloads = payloads or ['xss', 'lfi', 'ssrf', 'sqli']
        self.wordlist_file = wordlist_file
        self.use_seclists = use_seclists
        self.report_formats = report_formats
        self.user_agent = user_agent
        self.proxy = proxy
        self.headers = headers
        self.cookies = cookies
        self.enable_nuclei = enable_nuclei
        self.enable_subfinder = enable_subfinder
        self.enable_ffuf = enable_ffuf
        self.enable_sqlmap = enable_sqlmap

        # Results storage
        self.results = {
            'subdomains': [],
            'directories': [],
            'parameters': [],
            'vulnerabilities': [],
            'technologies': [],
            'inputs': [],
            'endpoints': [],
            'screenshots': []
        }

        # Initialize components
        self._initialize_components()

        # Session management
        self.session = None

    def _initialize_components(self):
        """Initialize all ShadowRecon components"""
        try:
            from ..utils.colors import ShadowColors
            from ..utils.file_utils import FileUtils
            from ..utils.http_utils import HTTPUtils
            from ..engines.subdomain_engine import SubdomainEngine
            from ..engines.directory_engine import DirectoryEngine
            from ..engines.parameter_engine import ParameterEngine
            from ..modules.xss_hunter import XSSHunter
            from ..modules.lfi_hunter import LFIHunter
            from ..modules.ssrf_hunter import SSRFHunter
            from ..modules.sqli_hunter import SQLiHunter
            from ..modules.graphql_hunter import GraphQLHunter
            from ..modules.s3_hunter import S3Hunter

            self.colors = ShadowColors
            self.file_utils = FileUtils
            self.http_utils = HTTPUtils

            # Initialize engines
            self.subdomain_engine = SubdomainEngine(verbose=self.verbose)
            self.directory_engine = DirectoryEngine(verbose=self.verbose)
            self.parameter_engine = ParameterEngine(verbose=self.verbose)

            # Initialize vulnerability hunters
            self.hunters = {
                'xss': XSSHunter(verbose=self.verbose),
                'lfi': LFIHunter(verbose=self.verbose),
                'ssrf': SSRFHunter(verbose=self.verbose),
                'sqli': SQLiHunter(verbose=self.verbose),
                'graphql': GraphQLHunter(verbose=self.verbose),
                's3': S3Hunter(verbose=self.verbose)
            }

            # Create output structure
            self.output_structure = self.file_utils.create_output_structure(self.output_dir)

        except ImportError as e:
            if self.verbose:
                print(f"[!] Error importing components: {e}")
            # Set minimal fallbacks
            self.colors = None
            self.file_utils = None
            self.http_utils = None

    async def discover_attack_surface(self, target_domain: str):
        """Main attack surface discovery orchestration"""

        start_time = time.time()

        try:
            # Phase 1: Information Gathering
            if self.verbose:
                print(f"{self._colorize('[PHASE 1]', 'shadow')} Attack Surface Mapping")
                print(f"{self._colorize('[*]', 'info')} Target: {target_domain}")
                print(f"{self._colorize('[*]', 'info')} Mode: {'Deep' if self.deep_mode else 'Standard'}")

            # Initialize HTTP session
            await self._initialize_session()

            # Subdomain discovery
            subdomains = await self._discover_subdomains(target_domain)

            # Directory discovery for each subdomain
            all_directories = await self._discover_directories(target_domain, subdomains)

            # Parameter discovery
            parameters = await self._discover_parameters(target_domain, subdomains)

            # Phase 2: Web Crawling (if enabled)
            if self.crawl_mode:
                if self.verbose:
                    print(f"{self._colorize('[PHASE 2]', 'shadow')} Web Crawling and Form Detection")

                inputs = await self._crawl_and_detect_inputs(target_domain, subdomains, all_directories)
                self.results['inputs'] = inputs

            # Phase 3: Vulnerability Testing (if enabled)
            if self.inject_mode:
                if self.verbose:
                    print(f"{self._colorize('[PHASE 3]', 'shadow')} Vulnerability Testing")

                vulnerabilities = await self._test_vulnerabilities()
                self.results['vulnerabilities'] = vulnerabilities

            # Phase 4: External Tool Integration
            if any([self.enable_nuclei, self.enable_subfinder, self.enable_ffuf]):
                if self.verbose:
                    print(f"{self._colorize('[PHASE 4]', 'shadow')} External Tool Integration")

                await self._run_external_tools(target_domain)

            # Phase 5: Report Generation
            if self.verbose:
                print(f"{self._colorize('[PHASE 5]', 'shadow')} Report Generation")

            duration = time.time() - start_time
            await self._generate_reports(target_domain, duration)

            # Final summary
            await self._display_summary(target_domain, duration)

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Fatal error in attack surface discovery: {e}")
            raise
        finally:
            await self._cleanup_session()

    async def _discover_subdomains(self, target_domain: str) -> List[str]:
        """Discover subdomains using multiple techniques"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting subdomain discovery...")

        subdomains = []

        try:
            if self.subdomain_engine:
                subdomains = await self.subdomain_engine.discover_subdomains(
                    target_domain, 
                    deep_mode=self.deep_mode,
                    use_seclists=self.use_seclists,
                    enable_subfinder=self.enable_subfinder
                )
        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Subdomain discovery error: {e}")

        self.results['subdomains'] = subdomains

        if self.verbose:
            print(f"{self._colorize('[+]', 'success')} Found {len(subdomains)} subdomains")

        return subdomains

    async def _discover_directories(self, target_domain: str, subdomains: List[str]) -> List[Dict[str, Any]]:
        """Discover directories for target and subdomains"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting directory discovery...")

        all_directories = []
        targets = [target_domain] + subdomains[:10]  # Limit to first 10 subdomains for performance

        try:
            if self.directory_engine and self.session:
                for target in targets:
                    target_urls = [f"https://{target}", f"http://{target}"]

                    for url in target_urls:
                        try:
                            directories = await self.directory_engine.discover_directories(
                                url, 
                                self.session,
                                deep_mode=self.deep_mode,
                                use_seclists=self.use_seclists
                            )
                            all_directories.extend(directories)
                        except Exception as e:
                            if self.verbose:
                                print(f"{self._colorize('[!]', 'warning')} Error scanning {url}: {e}")

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Directory discovery error: {e}")

        self.results['directories'] = all_directories

        if self.verbose:
            print(f"{self._colorize('[+]', 'success')} Found {len(all_directories)} directories")

        return all_directories

    async def _discover_parameters(self, target_domain: str, subdomains: List[str]) -> List[str]:
        """Discover parameters using various techniques"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting parameter discovery...")

        parameters = []

        try:
            if self.parameter_engine:
                targets = [target_domain] + subdomains[:5]  # Limit for performance

                for target in targets:
                    target_params = await self.parameter_engine.discover_parameters(
                        target,
                        self.session,
                        deep_mode=self.deep_mode
                    )
                    parameters.extend(target_params)

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Parameter discovery error: {e}")

        self.results['parameters'] = parameters

        if self.verbose:
            print(f"{self._colorize('[+]', 'success')} Found {len(parameters)} parameters")

        return parameters

    async def _crawl_and_detect_inputs(self, target_domain: str, subdomains: List[str], directories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Crawl websites and detect input fields and forms"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting web crawling and input detection...")

        inputs = []

        try:
            # Create list of URLs to crawl
            urls_to_crawl = []

            # Add main domain URLs
            urls_to_crawl.extend([f"https://{target_domain}", f"http://{target_domain}"])

            # Add subdomain URLs (limited)
            for subdomain in subdomains[:5]:
                urls_to_crawl.extend([f"https://{subdomain}", f"http://{subdomain}"])

            # Add directory URLs (limited)
            for directory in directories[:20]:
                if isinstance(directory, dict) and 'url' in directory:
                    urls_to_crawl.append(directory['url'])

            # Crawl and detect inputs
            for url in urls_to_crawl:
                try:
                    if self.session and self.http_utils:
                        response = await self.http_utils.safe_request(
                            self.session, 'GET', url
                        )

                        if response and response.get('status') == 200:
                            page_inputs = self.http_utils.parse_response_for_inputs(
                                response.get('content', ''), url
                            )
                            inputs.extend(page_inputs)

                            if self.verbose and page_inputs:
                                print(f"{self._colorize('[+]', 'success')} Found {len(page_inputs)} inputs on {url}")

                except Exception as e:
                    if self.verbose:
                        print(f"{self._colorize('[!]', 'warning')} Error crawling {url}: {e}")

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Crawling error: {e}")

        if self.verbose:
            print(f"{self._colorize('[+]', 'success')} Found {len(inputs)} total inputs")

        return inputs

    async def _test_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Test for vulnerabilities using enabled hunters"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting vulnerability testing...")

        vulnerabilities = []

        try:
            # Get all testable endpoints
            endpoints = self._get_testable_endpoints()

            if self.verbose:
                print(f"{self._colorize('[*]', 'info')} Testing {len(endpoints)} endpoints")

            # Test each enabled payload type
            for payload_type in self.payloads:
                if payload_type in self.hunters:
                    hunter = self.hunters[payload_type]

                    if self.verbose:
                        print(f"{self._colorize('[*]', 'info')} Testing {payload_type.upper()} vulnerabilities...")

                    for endpoint in endpoints:
                        try:
                            vuln_results = await hunter.test_endpoint(endpoint, self.session)
                            if vuln_results:
                                vulnerabilities.extend(vuln_results)
                                if self.verbose:
                                    for vuln in vuln_results:
                                        print(f"{self._colorize('[!]', 'vulnerable')} {payload_type.upper()} found: {vuln.get('url', 'Unknown')}")

                        except Exception as e:
                            if self.verbose:
                                print(f"{self._colorize('[!]', 'warning')} Error testing {endpoint}: {e}")

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Vulnerability testing error: {e}")

        if self.verbose:
            print(f"{self._colorize('[+]', 'success')} Found {len(vulnerabilities)} vulnerabilities")

        return vulnerabilities

    def _get_testable_endpoints(self) -> List[Dict[str, Any]]:
        """Get all endpoints that can be tested for vulnerabilities"""
        endpoints = []

        # Add directories as endpoints
        for directory in self.results.get('directories', []):
            if isinstance(directory, dict):
                endpoints.append(directory)

        # Add form inputs as endpoints
        for input_form in self.results.get('inputs', []):
            if isinstance(input_form, dict) and input_form.get('type') == 'form':
                endpoints.append(input_form)

        # Add parameter-based endpoints
        for param in self.results.get('parameters', []):
            if isinstance(param, str):
                endpoints.append({'url': param, 'type': 'parameter'})

        return endpoints

    async def _run_external_tools(self, target_domain: str):
        """Run external security tools"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Running external tools...")

        try:
            # Nuclei integration
            if self.enable_nuclei:
                try:
                    from ..integrations.nuclei_integration import NucleiIntegration
                    nuclei = NucleiIntegration(verbose=self.verbose)
                    nuclei_results = nuclei.run(target_domain)

                    if nuclei_results:
                        self.results['vulnerabilities'].extend(nuclei_results)
                        if self.verbose:
                            print(f"{self._colorize('[+]', 'success')} Nuclei found {len(nuclei_results)} issues")

                except ImportError:
                    if self.verbose:
                        print(f"{self._colorize('[!]', 'warning')} Nuclei integration not available")

            # Subfinder integration
            if self.enable_subfinder:
                try:
                    from ..integrations.subfinder_integration import SubfinderIntegration
                    subfinder = SubfinderIntegration(verbose=self.verbose)
                    subfinder_results = subfinder.run(target_domain)

                    if subfinder_results:
                        # Add to existing subdomains
                        existing = set(self.results.get('subdomains', []))
                        new_subdomains = [s for s in subfinder_results if s not in existing]
                        self.results['subdomains'].extend(new_subdomains)

                        if self.verbose:
                            print(f"{self._colorize('[+]', 'success')} Subfinder found {len(new_subdomains)} new subdomains")

                except ImportError:
                    if self.verbose:
                        print(f"{self._colorize('[!]', 'warning')} Subfinder integration not available")

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} External tools error: {e}")

    async def _initialize_session(self):
        """Initialize HTTP session with configuration"""
        if not AIOHTTP_AVAILABLE:
            if self.verbose:
                print(f"{self._colorize('[!]', 'warning')} aiohttp not available - limited functionality")
            return

        try:
            if self.http_utils:
                config = self.http_utils.create_session_config(
                    timeout=self.timeout,
                    threads=self.threads,
                    user_agent=self.user_agent,
                    proxy=self.proxy,
                    headers=self._parse_headers(),
                    cookies=self.cookies
                )

                self.session = await self.http_utils.create_session(config)

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Session initialization error: {e}")

    def _parse_headers(self) -> Dict[str, str]:
        """Parse header string into dictionary"""
        headers = {}
        if self.headers:
            try:
                for header_pair in self.headers.split(','):
                    if ':' in header_pair:
                        key, value = header_pair.split(':', 1)
                        headers[key.strip()] = value.strip()
            except Exception:
                pass
        return headers

    async def _cleanup_session(self):
        """Clean up HTTP session"""
        if self.session:
            try:
                await self.session.close()
            except Exception:
                pass

    async def _generate_reports(self, target_domain: str, duration: float):
        """Generate reports in specified formats"""
        try:
            if self.file_utils:
                saved_files = self.file_utils.save_scan_results(
                    self.output_dir, target_domain, self.results
                )

                for format_type, filepath in saved_files.items():
                    if self.verbose:
                        print(f"{self._colorize('[+]', 'success')} {format_type.upper()} report saved: {filepath}")

        except Exception as e:
            if self.verbose:
                print(f"{self._colorize('[!]', 'error')} Report generation error: {e}")

    async def _display_summary(self, target_domain: str, duration: float):
        """Display final summary"""
        if self.verbose:
            print()
            print(self._colorize("=" * 80, 'shadow'))
            print(f"{self._colorize('[ATTACK SURFACE DISCOVERY COMPLETE]', 'success')}")
            print(self._colorize("=" * 80, 'shadow'))
            print()
            print(f"{self._colorize('[*]', 'info')} Target: {target_domain}")
            print(f"{self._colorize('[*]', 'info')} Duration: {duration:.2f} seconds")
            print(f"{self._colorize('[*]', 'info')} Subdomains: {len(self.results.get('subdomains', []))}")
            print(f"{self._colorize('[*]', 'info')} Directories: {len(self.results.get('directories', []))}")
            print(f"{self._colorize('[*]', 'info')} Parameters: {len(self.results.get('parameters', []))}")
            print(f"{self._colorize('[*]', 'info')} Input Forms: {len(self.results.get('inputs', []))}")
            print(f"{self._colorize('[*]', 'info')} Vulnerabilities: {len(self.results.get('vulnerabilities', []))}")
            print(f"{self._colorize('[*]', 'info')} Output Directory: {self.output_dir}")
            print()
            print(f"{self._colorize('💀', 'shadow')} 'In the shadows, we have mapped the entire attack surface...'")
            print()

    def _colorize(self, text: str, color_type: str) -> str:
        """Apply color to text if colors are available"""
        if self.colors:
            color_methods = {
                'success': self.colors.success,
                'error': self.colors.error,
                'warning': self.colors.warning,
                'info': self.colors.info,
                'shadow': self.colors.shadow,
                'vulnerable': self.colors.vulnerable
            }
            method = color_methods.get(color_type, lambda x: x)
            return method(text)
        return text

    async def discover_multiple_targets(self, targets: List[str]):
        """Discover attack surface for multiple targets"""
        if self.verbose:
            print(f"{self._colorize('[*]', 'info')} Starting multi-target attack surface discovery...")
            print(f"{self._colorize('[*]', 'info')} Targets: {len(targets)}")

        for i, target in enumerate(targets):
            if self.verbose:
                print(f"\n{self._colorize(f'[TARGET {i+1}/{len(targets)}]', 'shadow')} {target}")
                print(self._colorize("-" * 60, 'shadow'))

            try:
                await self.discover_attack_surface(target)
            except Exception as e:
                if self.verbose:
                    print(f"{self._colorize('[!]', 'error')} Error with target {target}: {e}")
                continue

        if self.verbose:
            print(f"\n{self._colorize('[MULTI-TARGET DISCOVERY COMPLETE]', 'success')}")
            print(f"{self._colorize('💀', 'shadow')} 'All shadows have been explored...'")
