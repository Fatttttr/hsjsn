#!/usr/bin/env python3
"""
Test GitHub connection manually untuk debugging
"""

import json
from github_client import GitHubClient

def test_github_connection():
    """Test GitHub connection dengan konfigurasi yang ada"""
    
    # Load config
    try:
        with open('github_config.json', 'r') as f:
            config = json.load(f)
        
        token = config.get('token')
        owner = config.get('owner')
        repo = config.get('repo')
        
        print(f"🔍 Testing GitHub connection:")
        print(f"   Owner: {owner}")
        print(f"   Repo: {repo}")
        print(f"   Token: {token[:10]}...{token[-4:] if len(token) > 14 else '****'}")
        print()
        
        # Create client
        client = GitHubClient(token, owner, repo)
        
        # Test connection
        print("🔗 Testing basic connection...")
        result = client.test_connection()
        
        print(f"Connection result: {result}")
        print()
        
        if result['success']:
            print("✅ Connection successful!")
            print(f"   Repository: {result.get('repo_name')}")
            print(f"   Private: {result.get('private')}")
            print(f"   Branch: {result.get('default_branch')}")
            print()
            
            # Test file listing
            print("📁 Testing file listing...")
            files = client.list_files_in_repo()
            
            if files:
                print(f"✅ Found {len(files)} files:")
                json_files = [f for f in files if f.get('name', '').endswith('.json')]
                print(f"   JSON files: {len(json_files)}")
                
                for f in json_files[:5]:  # Show first 5
                    print(f"     - {f.get('name')}")
                    
                if len(json_files) > 5:
                    print(f"     ... and {len(json_files) - 5} more")
            else:
                print("❌ No files found or error listing files")
                
        else:
            print("❌ Connection failed!")
            print(f"   Error: {result.get('error')}")
            print(f"   Details: {result.get('details')}")
            
    except FileNotFoundError:
        print("❌ github_config.json not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_github_connection()