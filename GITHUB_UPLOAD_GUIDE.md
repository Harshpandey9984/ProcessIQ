# GitHub Upload Guide

## Repository Information
- **Repository URL**: https://github.com/Harshpandey9984/ProcessIQ.git
- **Project**: ProcessIQ Digital Twin Platform

## Authentication Methods

### Method 1: Personal Access Token (PAT)
1. Generate a PAT from GitHub:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with `repo` scope
   - Copy the token when shown (it won't be displayed again)

2. Push using HTTPS with your PAT:
   ```bash
   git push -u origin master
   ```
   - When prompted for password, use your PAT instead

### Method 2: GitHub CLI
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```
3. Push using GitHub CLI:
   ```bash
   gh repo create Harshpandey9984/ProcessIQ --public --source=. --remote=origin --push
   ```

### Method 3: SSH Authentication
1. Generate SSH key if you don't have one:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Add SSH key to GitHub:
   - Go to GitHub → Settings → SSH and GPG keys → New SSH key
   - Copy your public key (usually in `~/.ssh/id_ed25519.pub`) and paste it

3. Update remote URL to use SSH:
   ```bash
   git remote set-url origin git@github.com:Harshpandey9984/ProcessIQ.git
   ```
4. Push to GitHub:
   ```bash
   git push -u origin master
   ```

## Troubleshooting
- If you get a "403 Forbidden" error, your token may not have the right permissions
- If you get a "remote already exists" error, use `git remote remove origin` first
- For credential issues, check Windows Credential Manager and clear any old GitHub credentials

## After Successful Push
After pushing successfully, verify your code on GitHub by visiting:
https://github.com/Harshpandey9984/ProcessIQ
