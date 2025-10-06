"""
Web Crawler for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced web crawling and form detection engine
"""

import asyncio
import re
from typing import List, Dict, Any, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs
from dataclasses import dataclass, field

@dataclass
class CrawledPage:
    """Information about a crawled page"""
    url: str
    status_code: int
    content_length: int
    content_type: str
    title: str = ""
    forms: List[Dict[str, Any]] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    parameters: Set[str] = field(default_factory=set)
    depth: int = 0

class WebCrawler:
    """Advanced web crawler with form and input detection"""

    def __init__(self, max_depth: int = 3, max_pages: int = 100, verbose: bool = False):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.verbose = verbose

        self.visited_urls = set()
        self.crawled_pages = []
        self.discovered_forms = []
        self.discovered_inputs = []
        self.discovered_parameters = set()

        # URL patterns to avoid
        self.ignore_patterns = [
            r'\.(?:png|jpg|jpeg|gif|svg|ico|css|js|woff|woff2|ttf|eot)$',
            r'logout|signout|exit',
            r'mailto:',
            r'javascript:',
            r'tel:',
            r'\#'
        ]

        # Interesting file extensions
        self.interesting_extensions = [
            '.php', '.asp', '.aspx', '.jsp', '.do', '.action',
            '.html', '.htm', '.shtml', '.cgi', '.pl', '.py'
        ]

    async def crawl_domain(self, base_url: str, session) -> List[CrawledPage]:
        """Crawl domain starting from base URL"""

        if self.verbose:
            print(f"🕷️ Starting web crawl from {base_url}")

        # Initialize with base URL
        urls_to_crawl = [(base_url, 0)]  # (url, depth)

        while urls_to_crawl and len(self.visited_urls) < self.max_pages:
            current_url, depth = urls_to_crawl.pop(0)

            # Skip if already visited or max depth reached
            if current_url in self.visited_urls or depth > self.max_depth:
                continue

            # Skip ignored patterns
            if self._should_ignore_url(current_url):
                continue

            # Crawl current page
            try:
                crawled_page = await self._crawl_single_page(current_url, depth, session)
                if crawled_page:
                    self.crawled_pages.append(crawled_page)

                    # Add discovered links to crawl queue
                    if depth < self.max_depth:
                        for link in crawled_page.links:
                            if self._is_same_domain(link, base_url):
                                urls_to_crawl.append((link, depth + 1))

                    if self.verbose:
                        print(f"[+] Crawled: {current_url} [{crawled_page.status_code}] "
                              f"({len(crawled_page.forms)} forms, {len(crawled_page.inputs)} inputs)")

            except Exception as e:
                if self.verbose:
                    print(f"[!] Crawl error for {current_url}: {e}")
                continue

        if self.verbose:
            print(f"🎯 Crawl complete: {len(self.crawled_pages)} pages, "
                  f"{len(self.discovered_forms)} forms, {len(self.discovered_inputs)} inputs")

        return self.crawled_pages

    async def _crawl_single_page(self, url: str, depth: int, session) -> Optional[CrawledPage]:
        """Crawl a single page and extract information"""

        self.visited_urls.add(url)

        if not session:
            return None

        try:
            # Import HTTP utils
            from ..utils.http_utils import HTTPUtils

            # Make HTTP request
            response = await HTTPUtils.safe_request(session, 'GET', url)

            if not response or response.get('status', 0) not in [200, 201, 202]:
                return None

            content = response.get('content', '')
            if not content:
                return None

            # Create crawled page object
            crawled_page = CrawledPage(
                url=url,
                status_code=response.get('status', 0),
                content_length=len(content),
                content_type=response.get('content_type', ''),
                depth=depth
            )

            # Extract page information
            crawled_page.title = self._extract_title(content)
            crawled_page.forms = self._extract_forms(content, url)
            crawled_page.links = self._extract_links(content, url)
            crawled_page.inputs = self._extract_inputs(content, url)
            crawled_page.technologies = self._detect_technologies(content, response.get('headers', {}))
            crawled_page.parameters = self._extract_parameters(content, url)

            # Update global collections
            self.discovered_forms.extend(crawled_page.forms)
            self.discovered_inputs.extend(crawled_page.inputs)
            self.discovered_parameters.update(crawled_page.parameters)

            return crawled_page

        except Exception as e:
            if self.verbose:
                print(f"[!] Error crawling {url}: {e}")
            return None

    def _extract_title(self, content: str) -> str:
        """Extract page title"""
        try:
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()[:100]
        except:
            pass
        return ""

    def _extract_forms(self, content: str, base_url: str) -> List[Dict[str, Any]]:
        """Extract all forms from page content"""
        forms = []

        try:
            # Try using BeautifulSoup if available
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')

                for form in soup.find_all('form'):
                    form_data = {
                        'action': urljoin(base_url, form.get('action', '')),
                        'method': form.get('method', 'get').upper(),
                        'enctype': form.get('enctype', 'application/x-www-form-urlencoded'),
                        'inputs': [],
                        'url': base_url
                    }

                    # Extract form inputs
                    for input_elem in form.find_all(['input', 'textarea', 'select']):
                        input_data = {
                            'name': input_elem.get('name', ''),
                            'type': input_elem.get('type', 'text'),
                            'value': input_elem.get('value', ''),
                            'placeholder': input_elem.get('placeholder', ''),
                            'required': input_elem.has_attr('required')
                        }

                        if input_data['name']:
                            form_data['inputs'].append(input_data)

                    if form_data['inputs']:  # Only add forms with inputs
                        forms.append(form_data)

            except ImportError:
                # Fallback regex parsing
                form_pattern = r'<form[^>]*>(.*?)</form>'
                form_matches = re.finditer(form_pattern, content, re.IGNORECASE | re.DOTALL)

                for match in form_matches:
                    form_content = match.group(1)

                    # Extract form attributes
                    action_match = re.search(r'action=["\']([^"\']*)["\']', match.group(0), re.IGNORECASE)
                    method_match = re.search(r'method=["\']([^"\']*)["\']', match.group(0), re.IGNORECASE)

                    action = urljoin(base_url, action_match.group(1) if action_match else '')
                    method = method_match.group(1).upper() if method_match else 'GET'

                    # Extract inputs
                    input_pattern = r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>'
                    input_names = re.findall(input_pattern, form_content, re.IGNORECASE)

                    if input_names:
                        form_data = {
                            'action': action,
                            'method': method,
                            'inputs': [{'name': name, 'type': 'text'} for name in input_names],
                            'url': base_url
                        }
                        forms.append(form_data)

        except Exception as e:
            if self.verbose:
                print(f"[!] Form extraction error: {e}")

        return forms

    def _extract_links(self, content: str, base_url: str) -> List[str]:
        """Extract all links from page content"""
        links = set()

        try:
            # Extract href links
            link_pattern = r'href=["\']([^"\']*)["\']'
            href_matches = re.findall(link_pattern, content, re.IGNORECASE)

            for href in href_matches:
                if href and not href.startswith('#') and not href.startswith('javascript:'):
                    absolute_url = urljoin(base_url, href)
                    if self._is_valid_url(absolute_url):
                        links.add(absolute_url)

            # Extract src links (images, scripts, etc.)
            src_pattern = r'src=["\']([^"\']*)["\']'
            src_matches = re.findall(src_pattern, content, re.IGNORECASE)

            for src in src_matches:
                if src and any(src.endswith(ext) for ext in self.interesting_extensions):
                    absolute_url = urljoin(base_url, src)
                    if self._is_valid_url(absolute_url):
                        links.add(absolute_url)

        except Exception as e:
            if self.verbose:
                print(f"[!] Link extraction error: {e}")

        return list(links)[:50]  # Limit links per page

    def _extract_inputs(self, content: str, base_url: str) -> List[Dict[str, Any]]:
        """Extract all input fields from page content"""
        inputs = []

        try:
            # Extract all input elements
            input_pattern = r'<input[^>]*>'
            input_matches = re.finditer(input_pattern, content, re.IGNORECASE)

            for match in input_matches:
                input_tag = match.group(0)

                # Extract input attributes
                name_match = re.search(r'name=["\']([^"\']*)["\']', input_tag, re.IGNORECASE)
                type_match = re.search(r'type=["\']([^"\']*)["\']', input_tag, re.IGNORECASE)

                if name_match:
                    input_data = {
                        'name': name_match.group(1),
                        'type': type_match.group(1) if type_match else 'text',
                        'url': base_url,
                        'element': 'input'
                    }
                    inputs.append(input_data)

            # Extract textarea elements
            textarea_pattern = r'<textarea[^>]*name=["\']([^"\']*)["\'][^>]*>'
            textarea_matches = re.findall(textarea_pattern, content, re.IGNORECASE)

            for name in textarea_matches:
                input_data = {
                    'name': name,
                    'type': 'textarea',
                    'url': base_url,
                    'element': 'textarea'
                }
                inputs.append(input_data)

        except Exception as e:
            if self.verbose:
                print(f"[!] Input extraction error: {e}")

        return inputs

    def _extract_parameters(self, content: str, url: str) -> Set[str]:
        """Extract parameters from URLs in content"""
        parameters = set()

        try:
            # Extract from current URL
            parsed_url = urlparse(url)
            if parsed_url.query:
                query_params = parse_qs(parsed_url.query)
                parameters.update(query_params.keys())

            # Extract from JavaScript variables and AJAX calls
            js_param_patterns = [
                r'["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']\s*:\s*',
                r'\?([a-zA-Z_][a-zA-Z0-9_]*)=',
                r'data\.([a-zA-Z_][a-zA-Z0-9_]*)',
                r'params\.([a-zA-Z_][a-zA-Z0-9_]*)'
            ]

            for pattern in js_param_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                parameters.update(matches)

            # Common parameter names from URLs in content
            url_pattern = r'https?://[^\s"\'<>]+\?([^\s"\'<>&]+)'
            url_matches = re.findall(url_pattern, content)

            for query_string in url_matches:
                try:
                    query_params = parse_qs(query_string)
                    parameters.update(query_params.keys())
                except:
                    pass

        except Exception as e:
            if self.verbose:
                print(f"[!] Parameter extraction error: {e}")

        # Filter out common non-parameter strings
        filtered_params = set()
        for param in parameters:
            if (len(param) > 1 and len(param) < 30 and 
                param.isalnum() or '_' in param or '-' in param):
                filtered_params.add(param)

        return filtered_params

    def _detect_technologies(self, content: str, headers: Dict[str, str]) -> List[str]:
        """Detect technologies used on the page"""
        technologies = []

        # Header-based detection
        server = headers.get('server', '').lower()
        if 'nginx' in server:
            technologies.append('nginx')
        if 'apache' in server:
            technologies.append('apache')
        if 'iis' in server:
            technologies.append('iis')

        powered_by = headers.get('x-powered-by', '').lower()
        if 'php' in powered_by:
            technologies.append('php')
        if 'asp.net' in powered_by:
            technologies.append('asp.net')

        # Content-based detection
        content_lower = content.lower()

        tech_signatures = {
            'wordpress': ['wp-content', 'wp-includes', '/wp-'],
            'drupal': ['drupal', '/sites/default/', '/modules/'],
            'joomla': ['joomla', '/components/', '/templates/'],
            'magento': ['magento', '/skin/frontend/'],
            'react': ['react', 'reactjs', '_react'],
            'vue': ['vue.js', 'vue', '__vue__'],
            'angular': ['angular', 'ng-app', 'ng-controller'],
            'jquery': ['jquery', '$.', 'jquery.min.js'],
            'bootstrap': ['bootstrap', 'bootstrap.min.css'],
            'cloudflare': ['cloudflare', '__cf_bm'],
            'google-analytics': ['google-analytics', 'gtag('],
            'php': ['<?php', '.php'],
            'asp': ['asp.net', '.aspx', '.asp'],
            'jsp': ['.jsp', '<%'],
            'python': ['django', 'flask', 'python']
        }

        for tech, signatures in tech_signatures.items():
            if any(sig in content_lower for sig in signatures):
                technologies.append(tech)

        return list(set(technologies))

    def _should_ignore_url(self, url: str) -> bool:
        """Check if URL should be ignored during crawling"""
        url_lower = url.lower()

        for pattern in self.ignore_patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                return True

        return False

    def _is_same_domain(self, url: str, base_url: str) -> bool:
        """Check if URL belongs to same domain as base URL"""
        try:
            url_domain = urlparse(url).netloc
            base_domain = urlparse(base_url).netloc
            return url_domain == base_domain or url_domain.endswith('.' + base_domain)
        except:
            return False

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and crawlable"""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ['http', 'https'] and parsed.netloc
        except:
            return False

    def get_crawl_summary(self) -> Dict[str, Any]:
        """Get summary of crawl results"""
        return {
            'total_pages_crawled': len(self.crawled_pages),
            'total_forms_found': len(self.discovered_forms),
            'total_inputs_found': len(self.discovered_inputs),
            'total_parameters_found': len(self.discovered_parameters),
            'technologies_detected': list(set(
                tech for page in self.crawled_pages for tech in page.technologies
            )),
            'input_types_found': list(set(
                inp.get('type', 'unknown') for inp in self.discovered_inputs
            )),
            'form_methods_found': list(set(
                form.get('method', 'GET') for form in self.discovered_forms
            ))
        }
