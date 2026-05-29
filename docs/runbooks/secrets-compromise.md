# Secrets Compromise Response Runbook

**Alert**: Secret found in repo OR unauthorized access suspected

## Severity Levels

- 🔴 **CRITICAL**: Database password leaked
- 🟠 **HIGH**: API token / service account key exposed
- 🟡 **MEDIUM**: SSH key in commit (no active use)

## Immediate Actions (First 5 minutes)

1. **Acknowledge**
   - [ ] Post to #security-incidents Slack
   - [ ] Page security team
   - [ ] Create incident ticket

2. **Contain**
   - [ ] Rotate the exposed secret immediately
   - [ ] Revoke tokens / regenerate keys
   - [ ] Disable service account (if applicable)
   - [ ] Backup exposed secret value (for forensics)

3. **Assess Exposure**
   - [ ] When was it exposed? (git history)
   - [ ] Who has access? (git logs)
   - [ ] Was it used anywhere? (access logs)
   - [ ] How was it exposed? (branch / PR / direct commit)

## Investigation (5-30 minutes)

### How to Find the Secret

```bash
# Search git history
git log --all --full-history --oneline | grep -i "secret\|password\|token"

# Find commit with secret
git log --all -S '<secret-value>' --oneline

# Get commit details
git show <commit-hash>

# Check who committed it
git log --oneline -p <commit-hash> | grep Author
```

### Check Access Logs

```bash
# Did anyone use the exposed credentials?
grep -r "<secret-value>" /var/log/auth.log
grep -r "<secret-value>" /var/log/apache2/access.log

# Check cloud provider logs (AWS, GCP, Azure)
aws logs filter-log-events --log-group-name <group> --filter-pattern '<secret>'
```

### Check Repository Access

```bash
# Who has access to the repo?
gh repo list --json name,primaryLanguage,visibility

# Recent collaborators
gh repo view --json collaborators

# Clone activity
git log --all --oneline | head -20
```

## Remediation Steps

### Step 1: Rotate the Secret

**Database Password**:
```sql
ALTER USER schema_architect WITH PASSWORD '<new-password>';
```

**API Token** (GitHub):
```bash
gh auth logout
gh auth login  # Use new token
```

**AWS/Cloud Credentials**:
```bash
# Revoke old key
aws iam delete-access-key --access-key-id <key-id>

# Create new key
aws iam create-access-key --user-name <user>
```

### Step 2: Remove Secret from Git History

**Option A: BFG Repo Cleaner (Recommended)**

```bash
# Install BFG
brew install bfg

# Remove secret from history
echo "<secret-value>" > secrets.txt
bfg --replace-all --no-blob-protection --textblob secrets.txt

# Force push
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push origin --force --all
```

**Option B: Git Filter**

```bash
# Find and remove
git filter-branch --tree-filter 'grep -r "<secret>" . && git rm' -- --all

# Force push
git push origin --force --all --tags
```

### Step 3: Notify Stakeholders

**Message Template**:
```
A secret was inadvertently committed to the repository.
We have:
1. Rotated all affected credentials
2. Removed the secret from git history
3. Revoked unauthorized access

No unauthorized access was detected.
No customer data was affected.
```

### Step 4: Audit Access

```bash
# Check who pulled the repo after secret was committed
git log --all --format='%h %ae %ad' --date=short

# See if anyone used the credential
grep '<secret-value>' logs/access.log
```

## Prevention

### Enable Secret Scanning

**GitHub Secret Scanning**:
1. Go to Settings → Security & analysis
2. Enable "Secret scanning"
3. GitHub will alert on detected secrets

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Scanning for secrets..."
detect-secrets scan --baseline .secrets.baseline

if [ $? -ne 0 ]; then
    echo "ERROR: Secrets detected. Aborting commit."
    exit 1
fi
```

### Environment Variables

```bash
# Use .env files (in .gitignore)
export DATABASE_PASSWORD=$(cat ~/.config/app/db_password)

# Or use a secrets manager
export DATABASE_PASSWORD=$(vault kv get -field=password secret/db)
```

## Escalation Path

1. **Immediate**: Rotate secret
2. **5 min**: Check for unauthorized access
3. **15 min**: Remove from git history
4. **30 min**: Notify stakeholders
5. **1 hour**: Post-incident review

## Post-Incident

1. **Root cause**: How did secret get committed?
2. **Timeline**: When was it first exposed?
3. **Impact**: Any unauthorized access?
4. **Prevention**: What tooling can prevent this?
5. **Follow-up**: Add pre-commit hook, enable secret scanning

## References

- Secret scanning: GitHub Security tab
- BFG Repo Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
- detect-secrets: https://github.com/Yelp/detect-secrets
- Vault: https://www.vaultproject.io/
