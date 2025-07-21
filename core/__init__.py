"""
Core VPN testing modules for Bot VPN Checker
"""

from .github_client import GitHubClient
from .extractor import extract_vpn_accounts
from .tester import test_account

import asyncio
import json

# VPN test result class that matches main branch logic
class VPNTestResult:
    def __init__(self, account_dict: dict, result_dict: dict):
        self.account = account_dict
        self.result = result_dict
        self.is_working = result_dict.get('Status') in ['✅']
        self.latency = result_dict.get('Latency', -1)
        self.error = None if self.is_working else f"Status: {result_dict.get('Status', 'Unknown')}"
        self.country = result_dict.get('Country', '❓')
        self.provider = result_dict.get('Provider', '-')

# Enhanced VPN tester using main branch logic
class VPNTester:
    def __init__(self, max_concurrent: int = 5, timeout: int = 10):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
    
    async def test_multiple_accounts(self, accounts: list) -> list:
        """Test multiple VPN accounts using main branch testing logic"""
        # Convert account URLs to account dicts if needed
        account_dicts = []
        for i, account in enumerate(accounts):
            if isinstance(account, str):
                # Try to parse as JSON first
                try:
                    account_dict = json.loads(account)
                except:
                    # If not JSON, treat as URL and create basic dict
                    account_dict = {
                        'tag': f'account-{i}',
                        'type': 'vless',  # Default type
                        'server': self._extract_server_from_url(account),
                        'server_port': 443,
                        '_raw_url': account
                    }
            else:
                account_dict = account
            
            account_dicts.append(account_dict)
        
        # Create semaphore and live_results
        semaphore = asyncio.Semaphore(self.max_concurrent)
        live_results = [{} for _ in account_dicts]
        
        # Use main branch test_account function
        tasks = [
            test_account(acc, semaphore, i, live_results)
            for i, acc in enumerate(account_dicts)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert to VPNTestResult objects
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
                final_results.append(VPNTestResult(account_dicts[i], error_result))
            else:
                final_results.append(VPNTestResult(account_dicts[i], result))
        
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
    'extract_vpn_accounts'
]