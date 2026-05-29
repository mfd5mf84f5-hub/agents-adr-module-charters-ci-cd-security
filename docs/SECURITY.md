# Security Documentation

This document outlines the security baseline, expectations, and compliance controls for this repository.

## Overview

- **Classification**: Internal
- **Compliance**: GDPR, SOC2, ISO 27001 (planned Phase 3)
- **Owner**: Security Team
- **Last Updated**: 2026-05-29

## Security Principles

1. **Defense in Depth**: Multiple layers of security (code, build, deploy)
2. **Zero Trust**: Assume breach; verify all inputs
3. **Audit Everything**: Maintain immutable logs for all changes
4. **Principle of Least Privilege**: Minimize permissions and access
5. **Transparency**: Document all security decisions (ADRs)

## Secrets Management

### Policy
- ❌ **Never commit secrets** to the repository (keys, tokens, passwords, certs)
- ✅ Use `.env` files locally (excluded via `.gitignore`)
- ✅ Store secrets in GitHub Repository Secrets (CI/CD)
- ✅ Rotate secrets every 90 days
- ✅ Use managed services (Vault, AWS Secrets Manager) in production

### Secrets Checklist
- [ ] No AWS keys, API tokens, or database passwords in code
- [ ] No service account credentials in repository
- [ ] No TLS certificates or private keys in code
- [ ] All `.env*` files are `.gitignore`-d
- [ ] CI secrets stored in GitHub Actions Secrets, not in workflow files
- [ ] `detect-secrets` scan passes with no findings

## Dependency Security

### Requirements
- All dependencies must be pinned in `pyproject.toml` (no floating versions)
- Dependencies locked in `requirements-lock.txt` for reproducibility
- Regular updates for security patches (at least monthly)
- SBOM (Software Bill of Materials) generated and reviewed on each release

### SCA (Software Composition Analysis)
- Tool: Snyk (planned) or OSS Index
- Frequency: On every commit (PR gate)
- Threshold: Block on CRITICAL vulnerabilities, warn on HIGH
- SBOM Format: CycloneDX 1.4 JSON
- Artifact Signing: cosign (via GitHub Actions OIDC)

## Threat Modeling

Each module must maintain a threat model documenting:
- Attack surface
- High-risk components
- Mitigation strategies
- Compliance controls

Template: `docs/security/threat-models.md`

## Vulnerability Response SLA

| Severity | Response Time | Action |
|---|---|---|
| CRITICAL | 24 hours | Immediate fix or workaround |
| HIGH | 72 hours | Schedule fix in next sprint |
| MEDIUM | 1 week | Fix in planned maintenance |
| LOW | 2 weeks | Fix during routine updates |

## Code Review & Approval

- **CODEOWNERS**: Required approval on all code changes
- **PR Checklist**: Must be 100% complete before merge
- **Security Review**: Any changes to auth, encryption, or secrets handling
- **Audit Trail**: All approvals logged in Git commit history

## Testing Requirements

- **Unit Tests**: 75% code coverage minimum (enforced in CI)
- **Security Tests**: Input validation, output encoding, secrets handling
- **Contract Tests**: Schema validation, API compatibility
- **Integration Tests**: End-to-end flows with real dependencies

## Build & CI Security

- Linting: `flake8`, `black` (code quality)
- SAST: `bandit` (static analysis)
- Secrets Scanning: `detect-secrets` (committed secrets)
- Dependency Scan: CycloneDX SBOM generation
- Artifact Signing: All releases signed with cosign + keyless OIDC
- No credentials in environment (use GitHub Secrets)

## Data Classification

| Level | Examples | Protection |
|---|---|---|
| Public | Documentation, schemas | No special handling |
| Internal | Configuration, module charters | Access control; audit logging |
| Confidential | API keys, credentials | Encryption; minimal access; rotation |

## Access Control

- **Repository**: Private (Phase 1); consider public for open source (Phase 2)
- **Workflows**: Protected via GitHub Actions permissions
- **Secrets**: Restricted to required workflows only
- **CODEOWNERS**: Enforce required approvals by role

## Incident Response

If a security issue is discovered:

1. **Assess**: Determine severity and impact
2. **Contain**: Disable or isolate the affected component
3. **Fix**: Apply patch and test thoroughly
4. **Release**: Push hotfix with priority tag
5. **Audit**: Document root cause and lessons learned (blameless postmortem)
6. **Communicate**: Notify affected parties within SLA

## Future Work (Phase 3+)

- [ ] Implement external SCA tool (Snyk API integration)
- [ ] Add runtime security monitoring
- [ ] Complete ISO 27001 compliance mapping
- [ ] Implement penetration testing
- [ ] Add FIPS 140-2 crypto enforcement
- [ ] Formal threat modeling review process

## References

- **ADR 0003**: CI/CD Platform Choice (security gates in GitHub Actions)
- **ADR 0002**: Schema Governance Approach (audit trail for schema changes)
- `.github/PULL_REQUEST_TEMPLATE.md`: PR security checklist
- `docs/security/threat-models.md`: Module threat models
- `docs/security/secrets-checklist.md`: Secrets validation guide
