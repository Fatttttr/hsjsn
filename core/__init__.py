"""
Core VPN testing modules for Bot VPN Checker
"""

from .github_client import GitHubClient
from .extractor import extract_vpn_accounts
from .tester import test_account
from .core import ensure_ws_path_field

import asyncio
import json

# VPN test result class that matches main branch logic
class VPNTestResult:
    def __init__(self, account_dict: dict, result_dict: dict):
        self.account = account_dict
        self.result = result_dict
        # Main branch uses '✅' for success, check for that exactly
        self.is_working = result_dict.get('Status') == '✅'
        self.latency = result_dict.get('Latency', -1)
        self.error = None if self.is_working else f"Status: {result_dict.get('Status', 'Unknown')}"
        self.country = result_dict.get('Country', '❓')
        self.provider = result_dict.get('Provider', '-')
        self.tested_ip = result_dict.get('Tested IP', '-')
        self.test_type = result_dict.get('TestType', 'N/A')

# Enhanced VPN tester using main branch logic
class VPNTester:
    def __init__(self, max_concurrent: int = 5, timeout: int = 10):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
    
    async def test_multiple_accounts(self, accounts: list) -> list:
        """Test multiple VPN accounts using main branch testing logic"""
        # Accounts should already be dict objects from extract_vpn_accounts
        # No conversion needed - use directly like main branch
        
        # Create semaphore and live_results exactly like main branch
        semaphore = asyncio.Semaphore(self.max_concurrent)
        live_results = [
            {
                "index": i,
                "OriginalTag": acc.get("tag", f"account-{i}"),
                "OriginalAccount": acc,
                "VpnType": acc.get("type", "-"),
                "Country": "❓",
                "Provider": "-",
                "Tested IP": "-",
                "Latency": -1,
                "Jitter": -1,
                "ICMP": "N/A",
                "Status": "WAIT",
            }
            for i, acc in enumerate(accounts)
        ]
        
        # Use main branch test_account function exactly the same way
        tasks = [
            test_account(acc, semaphore, i, live_results)
            for i, acc in enumerate(accounts)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert to VPNTestResult objects exactly like main branch results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = {
                    'Status': '❌',
                    'error': str(result),
                    'Latency': -1,
                    'Country': '❓',
                    'Provider': '-'
                }
                final_results.append(VPNTestResult(accounts[i], error_result))
            else:
                # Use actual test result from main branch logic
                final_results.append(VPNTestResult(accounts[i], result))
        
        return final_results
    
    def _extract_server_from_url(self, url: str) -> str:
        """Extract server from URL for basic parsing"""
        import re
        # Try to extract host from various URL formats
        patterns = [
            r'://([^:/@]+):(\d+)',  # protocol://host:port
            r'://([^/@]+)',         # protocol://host
            r'server["\']?\s*:\s*["\']?([^"\',:]+)',  # server field
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return 'unknown.host'

__all__ = [
    'GitHubClient',
    'VPNTester', 
    'VPNTestResult',
    'extract_vpn_accounts',
    'ensure_ws_path_field'
]