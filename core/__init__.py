"""
Core VPN testing modules for Bot VPN Checker
"""

from .github_client import GitHubClient
from .extractor import extract_vpn_accounts
from .converter import convert_v2ray_url_to_json

# Simple VPN test result class
class VPNTestResult:
    def __init__(self, account: str, is_working: bool, latency: float = 0.0, error: str = None):
        self.account = account
        self.is_working = is_working
        self.latency = latency
        self.error = error

# Simple VPN tester class  
class VPNTester:
    def __init__(self, max_concurrent: int = 5, timeout: int = 10):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
    
    async def test_multiple_accounts(self, accounts: list) -> list:
        """Test multiple VPN accounts using socket connectivity"""
        import asyncio
        import socket
        import re
        
        async def test_single_account(account: str) -> VPNTestResult:
            """Test single VPN account connectivity"""
            try:
                # Parse account URL to extract host and port
                host, port = self._parse_account_url(account)
                if not host or not port:
                    return VPNTestResult(account, False, error="Cannot parse host/port")
                
                # Test socket connectivity
                future = asyncio.open_connection(host, port)
                try:
                    reader, writer = await asyncio.wait_for(future, timeout=self.timeout)
                    writer.close()
                    await writer.wait_closed()
                    return VPNTestResult(account, True, latency=1.0)
                except asyncio.TimeoutError:
                    return VPNTestResult(account, False, error="Connection timeout")
                except Exception as e:
                    return VPNTestResult(account, False, error=str(e))
                    
            except Exception as e:
                return VPNTestResult(account, False, error=f"Parse error: {str(e)}")
        
        # Create semaphore for concurrent limit
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def test_with_semaphore(account):
            async with semaphore:
                return await test_single_account(account)
        
        # Run tests concurrently
        tasks = [test_with_semaphore(account) for account in accounts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(VPNTestResult(accounts[i], False, error=str(result)))
            else:
                final_results.append(result)
        
        return final_results
    
    def _parse_account_url(self, account_url: str) -> tuple:
        """Parse VPN account URL to extract host and port"""
        try:
            # Simple regex patterns for common VPN URLs
            patterns = [
                r'://([^:/@]+):(\d+)',  # protocol://host:port
                r'://([^/@]+)',         # protocol://host (default ports)
                r'server["\']?\s*:\s*["\']?([^"\',:]+)',  # server field in JSON
                r'host["\']?\s*:\s*["\']?([^"\',:]+)',    # host field
            ]
            
            for pattern in patterns:
                match = re.search(pattern, account_url)
                if match:
                    host = match.group(1)
                    port = int(match.group(2)) if len(match.groups()) > 1 else 443
                    return host, port
            
            return None, None
            
        except Exception:
            return None, None

__all__ = [
    'GitHubClient',
    'VPNTester', 
    'VPNTestResult',
    'extract_vpn_accounts',
    'convert_v2ray_url_to_json'
]