"""
File utilities for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Advanced file operations, wordlist management, and data persistence
"""

import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

class FileUtils:
    """Advanced file operations for shadow reconnaissance"""

    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> bool:
        """Ensure directory exists"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def read_wordlist(filepath: str, limit: Optional[int] = None) -> List[str]:
        """Read wordlist from file with error handling"""
        words = []

        try:
            if not os.path.exists(filepath):
                return words

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        words.append(line)

                        if limit and len(words) >= limit:
                            break

        except Exception:
            pass

        return words

    @staticmethod
    def read_json_file(filepath: str) -> Dict[str, Any]:
        """Read JSON file safely"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def write_json_file(filepath: str, data: Dict[str, Any]) -> bool:
        """Write JSON file safely"""
        try:
            # Ensure directory exists
            FileUtils.ensure_directory(os.path.dirname(filepath))

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception:
            return False

    @staticmethod
    def write_csv_file(filepath: str, data: List[Dict[str, Any]], fieldnames: List[str]) -> bool:
        """Write CSV file safely"""
        try:
            # Ensure directory exists
            FileUtils.ensure_directory(os.path.dirname(filepath))

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception:
            return False

    @staticmethod
    def append_to_file(filepath: str, content: str) -> bool:
        """Append content to file safely"""
        try:
            # Ensure directory exists
            FileUtils.ensure_directory(os.path.dirname(filepath))

            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content + '\n')
            return True
        except Exception:
            return False

    @staticmethod
    def read_domain_list(filepath: str) -> List[str]:
        """Read domain list from file"""
        domains = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Clean domain
                        domain = line.replace('http://', '').replace('https://', '').strip('/')
                        if '/' in domain:
                            domain = domain.split('/')[0]
                        if domain:
                            domains.append(domain)

        except Exception:
            pass

        return domains

    @staticmethod
    def find_seclists_path() -> Optional[str]:
        """Find SecLists installation path"""
        possible_paths = [
            '/usr/share/seclists',
            '/usr/share/SecLists',
            '/opt/SecLists',
            './SecLists',
            '../SecLists',
            os.path.expanduser('~/SecLists'),
            os.path.expanduser('~/seclists'),
            '/usr/local/share/seclists',
            '/usr/local/share/SecLists'
        ]

        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                return path

        return None

    @staticmethod
    def get_seclists_wordlist(category: str, filename: str) -> List[str]:
        """Get wordlist from SecLists"""
        seclists_path = FileUtils.find_seclists_path()
        if not seclists_path:
            return []

        filepath = os.path.join(seclists_path, category, filename)
        return FileUtils.read_wordlist(filepath)

    @staticmethod
    def save_scan_results(output_dir: str, domain: str, results: Dict[str, Any]) -> Dict[str, str]:
        """Save scan results to multiple formats"""
        saved_files = {}

        # Sanitize domain for filename
        safe_domain = domain.replace(':', '_').replace('/', '_').replace('\\', '_')
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')

        # Ensure output directories exist
        for subdir in ['json', 'csv', 'txt']:
            FileUtils.ensure_directory(os.path.join(output_dir, subdir))

        # Save JSON
        json_file = os.path.join(output_dir, 'json', f'shadowrecon_{safe_domain}_{timestamp}.json')
        if FileUtils.write_json_file(json_file, results):
            saved_files['json'] = json_file

        # Save CSV (flattened results)
        csv_data = []
        for result_type, items in results.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        row = {'type': result_type}
                        row.update(item)
                        csv_data.append(row)
                    else:
                        csv_data.append({'type': result_type, 'value': str(item)})

        if csv_data:
            fieldnames = set()
            for row in csv_data:
                fieldnames.update(row.keys())

            csv_file = os.path.join(output_dir, 'csv', f'shadowrecon_{safe_domain}_{timestamp}.csv')
            if FileUtils.write_csv_file(csv_file, csv_data, list(fieldnames)):
                saved_files['csv'] = csv_file

        # Save simple text summary
        txt_file = os.path.join(output_dir, 'txt', f'shadowrecon_{safe_domain}_{timestamp}.txt')
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"ShadowRecon Results for {domain}\n")
                f.write("=" * 50 + "\n\n")

                for result_type, items in results.items():
                    if isinstance(items, list) and items:
                        f.write(f"{result_type.upper()}:\n")
                        for item in items[:100]:  # Limit to first 100
                            if isinstance(item, dict):
                                f.write(f"  {item.get('url', item.get('name', str(item)))}\n")
                            else:
                                f.write(f"  {item}\n")
                        f.write("\n")

            saved_files['txt'] = txt_file

        except Exception:
            pass

        return saved_files

    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size safely"""
        try:
            return os.path.getsize(filepath)
        except Exception:
            return 0

    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Check if file exists"""
        try:
            return os.path.exists(filepath) and os.path.isfile(filepath)
        except Exception:
            return False

    @staticmethod
    def create_output_structure(base_dir: str) -> Dict[str, str]:
        """Create output directory structure"""
        structure = {
            'base': base_dir,
            'json': os.path.join(base_dir, 'json'),
            'csv': os.path.join(base_dir, 'csv'),
            'txt': os.path.join(base_dir, 'txt'),
            'html': os.path.join(base_dir, 'html'),
            'screenshots': os.path.join(base_dir, 'screenshots'),
            'payloads': os.path.join(base_dir, 'payloads'),
            'logs': os.path.join(base_dir, 'logs')
        }

        for path in structure.values():
            FileUtils.ensure_directory(path)

        return structure
