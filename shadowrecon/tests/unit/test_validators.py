"""
Unit tests for validators
"""

import pytest
from shadowrecon.utils.validators import validate_domain, validate_url

class TestValidators:

    def test_validate_domain_valid(self):
        """Test valid domain validation"""
        assert validate_domain("example.com") == True
        assert validate_domain("subdomain.example.com") == True
        assert validate_domain("test-domain.co.uk") == True

    def test_validate_domain_invalid(self):
        """Test invalid domain validation"""
        assert validate_domain("") == False
        assert validate_domain("invalid..domain") == False
        assert validate_domain(None) == False

    def test_validate_url_valid(self):
        """Test valid URL validation"""
        assert validate_url("https://example.com") == True
        assert validate_url("http://test.com/path") == True
        assert validate_url("ftp://files.example.com") == True

    def test_validate_url_invalid(self):
        """Test invalid URL validation"""
        assert validate_url("not-a-url") == False
        assert validate_url("") == False
        assert validate_url(None) == False
