# 🔧 GitHub Troubleshooting Guide

## ❌ "GitHub validation failed: Cannot connect to GitHub repository"

### Common Causes & Solutions:

### 1. 🔑 **Invalid or Expired GitHub Token**
**Error:** `Invalid GitHub token or insufficient permissions`

**Solution:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Create a new token or check existing token
3. **Required permissions:**
   - ✅ `repo` (Full repository access)
   - ✅ `read:org` (Read organization info)
4. Copy the new token and paste in VortexVPN Manager

**Token Format:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. 📁 **Repository Not Found**
**Error:** `Repository F4txhr/sing not found`

**Solution:**
1. Check repository owner name (case-sensitive)
2. Check repository name (case-sensitive)
3. Ensure repository exists and is accessible
4. For private repos, token must have access

### 3. 🚫 **Permission Issues**
**Error:** `GitHub API rate limit or access forbidden`

**Solutions:**
1. **Rate limit:** Wait 1 hour and try again
2. **Private repo:** Ensure token has repository access
3. **Organization repo:** Ensure token has organization access

### 4. 🌐 **Network Issues**
**Error:** `Connection timeout to GitHub` or `Cannot connect to GitHub`

**Solutions:**
1. Check internet connection
2. Try again in a few minutes
3. Check if GitHub is down: https://status.github.com

### 5. 📄 **No JSON Files Found**
**Error:** `No JSON configuration files found in repository`

**Solution:**
1. Add at least one `.json` file to your repository
2. Common names: `config.json`, `template.json`, `vpn-config.json`
3. Ensure files are in the root directory or specify path

## 🛠️ **How to Create a Valid GitHub Token**

### Step-by-Step:
1. **Go to GitHub Settings**
   - Click your profile → Settings
   - Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Give it a descriptive name: "VortexVPN Manager"

3. **Select Required Scopes**
   ```
   ✅ repo
     ✅ repo:status
     ✅ repo_deployment
     ✅ public_repo
     ✅ repo:invite
     ✅ security_events
   
   ✅ read:org
   ```

4. **Set Expiration**
   - Recommended: 90 days or longer
   - For security: Don't set "No expiration"

5. **Generate and Copy**
   - Click "Generate token"
   - **Important:** Copy token immediately (you won't see it again)

6. **Test in VortexVPN Manager**
   - Paste token in GitHub Token field
   - Click "Save GitHub Config"
   - If successful, dropdown will appear

## 🔍 **Debug Tools**

### In VortexVPN Manager:
1. Fill GitHub fields (token, owner, repo)
2. Click "🔍 Debug GitHub Connection"
3. Check console for detailed error messages

### Manual Testing:
```bash
# Run manual test
python3 test_github.py
```

## ✅ **Verification Checklist**

Before reporting issues, verify:

- [ ] Token is valid and not expired
- [ ] Token has `repo` permissions
- [ ] Repository owner/name are correct (case-sensitive)
- [ ] Repository exists and is accessible
- [ ] Repository contains at least one `.json` file
- [ ] Internet connection is working
- [ ] GitHub is not experiencing outages

## 🆘 **Still Having Issues?**

### Common Working Examples:

**Public Repository:**
- Owner: `microsoft`
- Repo: `vscode`
- Token: Any valid token with `public_repo` access

**Private Repository:**
- Owner: `yourusername`
- Repo: `your-private-repo`
- Token: Valid token with full `repo` access

### Test with This Public Repo:
If you want to test the functionality quickly:
- Owner: `microsoft`
- Repo: `vscode`
- Token: Any valid GitHub token

This will show how the dropdown works with a real repository.

## 🔄 **Alternative: Use Local Template**

If GitHub continues to have issues:
1. Select "Local Template" option (default)
2. Click directly to "Add VPN Links & Test"
3. No GitHub setup needed

This uses the local `template.json` file and works offline.

## 📞 **Support**

If none of these solutions work:
1. Use the "🔍 Debug GitHub Connection" button
2. Copy the debug output
3. Check console logs (F12 → Console)
4. Include error details when asking for help