import requests
import base64
import json

class GitHubClient:
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {
            "Authorization": f"Bearer {self.token}",  # Updated to Bearer token format
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "VortexVPN-Manager/1.0"
        }

    def test_connection(self) -> dict:
        """Test GitHub repository connection dengan detailed error info"""
        try:
            # Test basic repo access first
            repo_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
            
            print(f"🔍 Testing GitHub connection to: {repo_url}")
            print(f"🔍 Using token: {self.token[:10]}...{self.token[-4:] if len(self.token) > 14 else '****'}")
            
            response = requests.get(repo_url, headers=self.headers, timeout=15)
            
            print(f"🔍 Response status: {response.status_code}")
            print(f"🔍 Response headers: {dict(response.headers)}")
            
            if response.status_code == 401:
                return {
                    'success': False,
                    'error': 'Invalid GitHub token or insufficient permissions',
                    'details': 'Please check your token has repo access'
                }
            elif response.status_code == 404:
                return {
                    'success': False,
                    'error': f'Repository {self.owner}/{self.repo} not found',
                    'details': 'Please check repository owner and name'
                }
            elif response.status_code == 403:
                return {
                    'success': False,
                    'error': 'GitHub API rate limit or access forbidden',
                    'details': 'Please wait a moment or check token permissions'
                }
            
            response.raise_for_status()
            repo_data = response.json()
            
            return {
                'success': True,
                'repo_name': repo_data.get('name'),
                'private': repo_data.get('private', False),
                'default_branch': repo_data.get('default_branch', 'main')
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Connection timeout to GitHub',
                'details': 'GitHub API took too long to respond'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Cannot connect to GitHub',
                'details': 'Please check your internet connection'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'GitHub API error: {str(e)}',
                'details': 'Unexpected error connecting to GitHub'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'details': 'Please try again'
            }

    def list_files_in_repo(self, path: str = "") -> list:
        url = f"{self.api_url}/{path}"
        try:
            print(f"🔍 Listing files from: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 404:
                print(f"❌ Path not found: {path}")
                return []
            
            response.raise_for_status()
            files = response.json()
            print(f"✅ Found {len(files)} items in repository")
            return files
        except requests.exceptions.RequestException as e:
            print(f"❌ Gagal mengambil daftar file dari GitHub: {e}")
            return []

    def get_file(self, file_path: str) -> tuple[str, str]:
        url = f"{self.api_url}/{file_path}"
        try:
            print(f"🔍 Getting file: {file_path}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            return content, data['sha']
        except requests.exceptions.RequestException as e:
            print(f"❌ Gagal mengambil file '{file_path}': {e}")
            return None, None

    def update_or_create_file(self, file_path: str, content: str, commit_message: str, sha: str = None):
        url = f"{self.api_url}/{file_path}"
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        payload = {"message": commit_message, "content": encoded_content}
        if sha:
            payload['sha'] = sha
        try:
            response = requests.put(url, headers=self.headers, data=json.dumps(payload), timeout=15)
            response.raise_for_status()
            print(f"✔️ Berhasil menyimpan file '{file_path}' ke GitHub.")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Gagal menyimpan ke GitHub: {e}")
            return None