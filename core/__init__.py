# VPN Bot Core Module
# Contains VPN testing logic reused from VortexVPN Manager

__version__ = "1.0.0"
__author__ = "VPN Bot Team"

# Core modules
from .github_client import GitHubClient
from .extractor import extract_accounts_from_config
from .converter import parse_link
from .core import test_all_accounts, ensure_ws_path_field, sort_priority

__all__ = [
    'GitHubClient',
    'extract_accounts_from_config', 
    'parse_link',
    'test_all_accounts',
    'ensure_ws_path_field',
    'sort_priority'
]