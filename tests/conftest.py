"""
Pytest configuration for Agent Zero testing suite.
"""

import os
import sys
from pathlib import Path
import pytest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["TESTING"] = "true"
    yield
    os.environ.pop("TESTING", None)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "opencog: mark test as requiring OpenCog installation"
    )
    config.addinivalue_line(
        "markers", "requires_opencog: mark test as requiring OpenCog"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    # Skip OpenCog tests if not installed
    try:
        from opencog.atomspace import AtomSpace
        opencog_installed = True
    except ImportError:
        opencog_installed = False

    skip_opencog = pytest.mark.skip(reason="OpenCog not installed")

    for item in items:
        if ("opencog" in item.keywords or "requires_opencog" in item.keywords) and not opencog_installed:
            item.add_marker(skip_opencog)
