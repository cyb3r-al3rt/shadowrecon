"""
Integration tests for external tools
"""

import pytest
from shadowrecon.integrations.nuclei_integration import NucleiIntegration
from shadowrecon.integrations.subfinder_integration import SubfinderIntegration

class TestExternalIntegrations:

    def test_nuclei_availability(self):
        """Test Nuclei integration availability"""
        integration = NucleiIntegration()
        assert hasattr(integration, 'available')
        assert isinstance(integration.available, bool)

    def test_subfinder_availability(self):
        """Test Subfinder integration availability"""
        integration = SubfinderIntegration()
        assert hasattr(integration, 'available')
        assert isinstance(integration.available, bool)

    @pytest.mark.skip("External tool not available in CI")
    def test_nuclei_run(self):
        """Test Nuclei execution"""
        integration = NucleiIntegration()
        results = integration.run("example.com")
        assert isinstance(results, list)
