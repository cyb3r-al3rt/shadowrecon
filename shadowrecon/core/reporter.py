"""
Reporter for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced multi-format reporting system
"""

import json
import csv
import html
from datetime import datetime
from typing import Dict, List, Any, Optional

class ShadowReporter:
    """Advanced multi-format reporter"""

    def __init__(self, output_dir: str = './shadowrecon_output'):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f'{self.output_dir}/html', exist_ok=True)
        os.makedirs(f'{self.output_dir}/json', exist_ok=True)
        os.makedirs(f'{self.output_dir}/csv', exist_ok=True)

    def generate_html_report(self, results: Dict[str, Any], target: str) -> str:
        """Generate HTML report with professional styling"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'shadowrecon_{target.replace(".", "_")}_{timestamp}.html'
        filepath = f'{self.output_dir}/html/{filename}'

        # Generate HTML content
        subdomains = results.get('subdomains', [])
        directories = results.get('directories', [])
        parameters = results.get('parameters', [])
        vulnerabilities = results.get('vulnerabilities', [])

        # Create simplified HTML with proper CSS
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShadowRecon Report - {html.escape(target)}</title>
    <style>
        body {{ 
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 30px; 
            border-bottom: 2px solid #333; 
            padding-bottom: 20px; 
        }}
        .logo {{ 
            font-size: 3em; 
            color: #ff6b6b; 
            margin-bottom: 10px; 
        }}
        .stats {{ 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 20px; 
            margin: 20px 0; 
        }}
        .stat-card {{ 
            background: #1a1a1a; 
            border: 1px solid #333; 
            padding: 20px; 
            text-align: center; 
            border-radius: 5px; 
        }}
        .stat-number {{ 
            font-size: 2em; 
            color: #4ecdc4; 
            font-weight: bold; 
        }}
        .section {{ 
            margin: 20px 0; 
            background: #1a1a1a; 
            border: 1px solid #333; 
            border-radius: 5px; 
        }}
        .section-header {{ 
            background: #2a2a2a; 
            padding: 15px; 
            font-size: 1.2em; 
            font-weight: bold; 
        }}
        .section-content {{ 
            padding: 15px; 
        }}
        .item {{ 
            background: #2a2a2a; 
            margin: 5px 0; 
            padding: 10px; 
            border-radius: 3px; 
            word-break: break-all; 
        }}
        .vulnerability {{ 
            border-left: 4px solid #ff6b6b; 
        }}
        .footer {{ 
            text-align: center; 
            margin-top: 40px; 
            color: #666; 
            border-top: 2px solid #333; 
            padding-top: 20px; 
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎭 ShadowRecon</div>
        <p>"In the shadows, we find the truth. In reconnaissance, we find power."</p>
        <p>Developed by kernelpanic | A product of infosbios</p>
    </div>

    <div>
        <h2>🎯 Target: {html.escape(target)}</h2>
        <p>📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{len(subdomains)}</div>
            <div>Subdomains</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(directories)}</div>
            <div>Directories</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(parameters)}</div>
            <div>Parameters</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(vulnerabilities)}</div>
            <div>Vulnerabilities</div>
        </div>
    </div>

    <div class="section">
        <div class="section-header">🌐 Subdomains Found</div>
        <div class="section-content">
            {self._format_simple_list(subdomains)}
        </div>
    </div>

    <div class="section">
        <div class="section-header">📁 Directories Found</div>
        <div class="section-content">
            {self._format_directories(directories)}
        </div>
    </div>

    <div class="section">
        <div class="section-header">🔍 Parameters Found</div>
        <div class="section-content">
            {self._format_simple_list(parameters)}
        </div>
    </div>

    <div class="section">
        <div class="section-header">🚨 Vulnerabilities Found</div>
        <div class="section-content">
            {self._format_vulnerabilities(vulnerabilities)}
        </div>
    </div>

    <div class="footer">
        <p>🎭 Generated by ShadowRecon v1.0</p>
        <p>💀 "The hunt ends, but the shadows remain..."</p>
    </div>
</body>
</html>"""

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception:
            pass

        return filepath

    def _format_simple_list(self, items):
        """Format simple list for HTML"""
        if not items:
            return '<div style="color: #666; font-style: italic;">None found</div>'

        html_items = []
        for item in items:
            item_str = str(item)
            html_items.append(f'<div class="item">{html.escape(item_str)}</div>')

        return ''.join(html_items)

    def _format_directories(self, directories):
        """Format directories for HTML"""
        if not directories:
            return '<div style="color: #666; font-style: italic;">None found</div>'

        html_items = []
        for directory in directories:
            if isinstance(directory, dict):
                url = directory.get('url', 'Unknown')
                status = directory.get('status', '')
                item_text = f'{url} [{status}]' if status else url
            else:
                item_text = str(directory)

            html_items.append(f'<div class="item">{html.escape(item_text)}</div>')

        return ''.join(html_items)

    def _format_vulnerabilities(self, vulnerabilities):
        """Format vulnerabilities for HTML"""
        if not vulnerabilities:
            return '<div style="color: #4ecdc4; font-style: italic;">🎉 None found</div>'

        html_items = []
        for vuln in vulnerabilities:
            if isinstance(vuln, dict):
                vuln_type = vuln.get('type', 'unknown').upper()
                url = vuln.get('url', 'Unknown')
                severity = vuln.get('severity', 'medium')
                item_text = f'{vuln_type} - {url} (Severity: {severity})'
            else:
                item_text = str(vuln)

            html_items.append(f'<div class="item vulnerability">{html.escape(item_text)}</div>')

        return ''.join(html_items)

    def generate_json_report(self, results: Dict[str, Any], target: str) -> str:
        """Generate JSON report"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'shadowrecon_{target.replace(".", "_")}_{timestamp}.json'
        filepath = f'{self.output_dir}/json/{filename}'

        # Add metadata
        report_data = {
            'shadowrecon_version': '1.0.0',
            'target': target,
            'scan_timestamp': datetime.now().isoformat(),
            'developed_by': 'kernelpanic | A product of infosbios',
            'results': results,
            'summary': {
                'subdomains_found': len(results.get('subdomains', [])),
                'directories_found': len(results.get('directories', [])),
                'parameters_found': len(results.get('parameters', [])),
                'vulnerabilities_found': len(results.get('vulnerabilities', []))
            }
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        except Exception:
            pass

        return filepath

    def generate_csv_report(self, results: Dict[str, Any], target: str) -> str:
        """Generate CSV report"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'shadowrecon_{target.replace(".", "_")}_{timestamp}.csv'
        filepath = f'{self.output_dir}/csv/{filename}'

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Write header
                writer.writerow(['Category', 'Type', 'Value', 'Status', 'Details'])

                # Write data
                for subdomain in results.get('subdomains', []):
                    writer.writerow(['Subdomain', 'Discovery', subdomain, 'Found', ''])

                for directory in results.get('directories', []):
                    if isinstance(directory, dict):
                        writer.writerow([
                            'Directory', 'Discovery', 
                            directory.get('url', ''), 
                            directory.get('status', ''), 
                            f"Length: {directory.get('content_length', 0)}"
                        ])
                    else:
                        writer.writerow(['Directory', 'Discovery', str(directory), '', ''])

                for parameter in results.get('parameters', []):
                    writer.writerow(['Parameter', 'Discovery', parameter, 'Found', ''])

                for vuln in results.get('vulnerabilities', []):
                    if isinstance(vuln, dict):
                        writer.writerow([
                            'Vulnerability', 
                            vuln.get('type', 'unknown').upper(),
                            vuln.get('url', ''),
                            vuln.get('severity', 'medium').upper(),
                            vuln.get('payload', '')[:100]
                        ])
                    else:
                        writer.writerow(['Vulnerability', 'Unknown', str(vuln), '', ''])

        except Exception:
            pass

        return filepath

    def generate_all_reports(self, results: Dict[str, Any], target: str, formats: List[str] = None) -> Dict[str, str]:
        """Generate all requested report formats"""

        if not formats:
            formats = ['html', 'json']

        generated_reports = {}

        if 'html' in formats:
            generated_reports['html'] = self.generate_html_report(results, target)

        if 'json' in formats:
            generated_reports['json'] = self.generate_json_report(results, target)

        if 'csv' in formats:
            generated_reports['csv'] = self.generate_csv_report(results, target)

        return generated_reports
