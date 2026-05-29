# Secrets Checklist

Before committing code, verify that no secrets are included.

## Pre-commit Checklist

- [ ] No AWS access keys or secret keys
- [ ] No API tokens or OAuth credentials
- [ ] No database passwords
- [ ] No private TLS certificates or keys
- [ ] No service account credentials (GCP, Azure)
- [ ] No Vault tokens or KMS keys
- [ ] No hardcoded connection strings
- [ ] No PII (personally identifiable information)
- [ ] No `.env` file committed (should be in `.gitignore`)
- [ ] No `secrets.json` or similar config files
- [ ] No SSH private keys

## Verification

Run the secrets scanner before pushing:

```bash
# Install detect-secrets
pip install detect-secrets

# Scan for secrets
detect-secrets scan

# If baseline exists, check against it
detect-secrets scan --baseline .secrets.baseline
```

## If You Accidentally Committed a Secret

1. **Stop**: Do not push the commit
2. **Rotate**: Immediately rotate the secret (change API key, password, etc.)
3. **Rewrite**: Remove the secret from Git history
   ```bash
   git rm --cached path/to/file
   git commit --amend
   ```
4. **Report**: Notify security team
5. **Audit**: Check if secret was used elsewhere

## For CI/CD Secrets

- Use GitHub Repository Secrets (Settings > Secrets and variables > Actions)
- Reference via `{{ secrets.SECRET_NAME }}` in workflows
- Never echo secrets in logs
- Mask sensitive values in action output:
  ```yaml
  - name: Use secret
    env:
      MY_SECRET: ${{ secrets.MY_SECRET }}
    run: |
      echo "::add-mask::$MY_SECRET"
      # Use $MY_SECRET in commands
  ```

## Policy

- All secrets must be rotated every 90 days
- Secrets must have minimal scope (only needed permissions)
- Secrets must be stored in a secrets manager (Vault, AWS Secrets Manager) in production
- Local development should use `.env` (never commit)

## Emergency

If a critical secret is compromised:

1. Notify security team immediately
2. Rotate the secret
3. Audit recent usage
4. File incident report
5. Review Git history for leaks
