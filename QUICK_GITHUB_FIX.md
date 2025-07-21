# 🚀 Quick GitHub Fix

## ❌ Problem: "Invalid GitHub token or insufficient permissions"

### The token in your `github_config.json` is **expired or invalid**.

## ✅ **Solution (5 minutes):**

### 1. Create New GitHub Token:
🔗 **Go to:** https://github.com/settings/tokens/new

### 2. Configure Token:
- **Name:** `VortexVPN Manager`
- **Expiration:** `90 days` (recommended)
- **Scopes:** Check these boxes:
  ```
  ✅ repo
    ✅ repo:status  
    ✅ repo_deployment
    ✅ public_repo
    ✅ repo:invite
    ✅ security_events
  ```

### 3. Copy Token:
- Click "Generate token"
- **Copy the token immediately** (starts with `ghp_`)
- You won't be able to see it again!

### 4. Update VortexVPN Manager:
- Open VortexVPN Manager
- Go to GitHub Configuration section
- Paste the new token in "GitHub Token" field
- Click "💾 Save GitHub Config"
- ✅ If successful, dropdown will appear with your .json files

## 🔄 **Alternative: Use Local Template**

If you don't want to setup GitHub right now:

1. Select **"Local Template"** (default option)
2. Skip GitHub setup entirely  
3. Go directly to "Add VPN Links & Test"
4. Works offline with local template.json

## 🆘 **Still Not Working?**

### Test with Public Repository:
Use these settings to verify GitHub integration works:
- **Owner:** `microsoft`
- **Repo:** `vscode` 
- **Token:** Your new valid token

This will show you how the dropdown works.

### Debug Tools:
1. Fill GitHub fields in VortexVPN Manager
2. Click "🔍 Debug GitHub Connection"
3. Check the detailed error message

## ✅ **After Fix:**

You should see:
1. ✅ Green "Configured" badge
2. 📁 Dropdown with .json files from your repository
3. 🚀 Ready to select file and start testing

---
**Next:** Select a .json file from dropdown → Add VPN links → Start testing!