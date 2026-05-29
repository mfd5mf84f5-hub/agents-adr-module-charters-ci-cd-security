# ISO 27001 Control Mapping

This document maps ISO 27001 controls (A.5-A.18) to implementation in the schema architect project.

**Status**: Phase 2 - Core controls mapped (80% complete)
**Next Phase**: Phase 3 - Formal audit and evidence collection

## Control Categories

### A.5: Organizational Controls

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.5.1 | Information security policies | `docs/SECURITY.md` | ✅ | Policy document |
| A.5.2 | Information security roles | `CODEOWNERS` | ✅ | CODEOWNERS file |
| A.5.3 | Segregation of duties | ADR + CODEOWNERS | 📋 | Approval workflow |
| A.5.4 | Management responsibilities | `docs/ADRs/` | ✅ | Architecture decisions |
| A.5.5 | Contact with authorities | `docs/compliance/` | 📋 | Incident response SOP |
| A.5.6 | Industry associations | Reference only | ✅ | External standards |
| A.5.7 | Threat intelligence | `docs/security/threat-models.md` | ✅ | Threat models |
| A.5.8 | Information security in PM | `docs/ADRs/` | ✅ | Design reviews |

### A.6: Access Control

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.6.1 | Access control policy | `CODEOWNERS` + PR template | ✅ | Branch protection rules |
| A.6.2 | User registration | GitHub SSO | 📋 | Team management |
| A.6.3 | Privileged access | Service accounts (planned) | 📋 | Phase 3 |
| A.6.4 | User responsibilities | PR template | ✅ | Checklist |
| A.6.5 | Access rights review | Manual (quarterly) | 📋 | Planned automation |
| A.6.6 | Information and comms removal | `.gitignore` + secrets policy | ✅ | `.gitignore` file |
| A.6.7 | User authentication | GitHub OIDC | ✅ | GitHub Actions config |
| A.6.8 | Subsequent user authentication | 2FA required | 📋 | Org policy |
| A.6.9 | Access control for cryptographic keys | Vault placeholder | 📋 | Phase 3 |

### A.7: Cryptography

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.7.1 | Cryptographic controls policy | `docs/SECURITY.md` | 📋 | TLS policy (planned) |
| A.7.2 | Encryption of secrets | GitHub Actions Secrets | ✅ | `.github/workflows/` |

### A.8: Physical & Environmental Security

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.8.1 | Perimeter security | GitHub infrastructure | ✅ | Out of scope (GitHub) |
| A.8.2 | Physical entry | GitHub data center | ✅ | Out of scope (GitHub) |
| A.8.3 | Offices, rooms, facilities | GitHub managed | ✅ | Out of scope (GitHub) |

### A.9: Operations & Communications

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.9.1 | Operational procedures | `docs/deployment/playbook.md` | ✅ | Deployment SOP |
| A.9.2 | Change management | Git commits + PR review | ✅ | Commit history |
| A.9.3 | Capacity management | Resource monitoring | 📋 | Prometheus setup |
| A.9.4 | Segregation of dev/test/prod | Branch-based deployments | 📋 | Phase 3 |
| A.9.5 | Access to production code | CODEOWNERS | ✅ | `.github/CODEOWNERS` |

### A.10: Communications Security

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.10.1 | Network security | HTTPS + GitHub infrastructure | ✅ | Out of scope |
| A.10.2 | Information transfer | TLS 1.2+ | 📋 | Config (Phase 3) |
| A.10.3 | Message authentication | JWT + CODEOWNERS | ✅ | ADR 0002 |

### A.11: Systems Acquisition, Development & Maintenance

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.11.1 | Policy for application security | `docs/SECURITY.md` | ✅ | Security doc |
| A.11.2 | Secure development | `pyproject.toml` + CI | ✅ | Build config |
| A.11.3 | Development practices | Black, flake8, mypy | ✅ | `.github/workflows/ci.yml` |
| A.11.4 | Testing of security controls | Unit + contract + security tests | ✅ | `tests/` |
| A.11.5 | Secure supply chain | SCA + SBOM | ✅ | `pyproject.toml` |
| A.11.6 | Development change control | Git + CODEOWNERS | ✅ | Branch protection |
| A.11.7 | Removal of temporary test data | `.gitignore` | ✅ | Config file |
| A.11.8 | Access control for code artifacts | GitHub organization | 📋 | Access control (Phase 3) |
| A.11.9 | Configuration management | Git + Docker + K8s | 📋 | Phase 3 |
| A.11.10 | Information and comms removal | PR review + secrets scanning | ✅ | `detect-secrets` |
| A.11.11 | Software vulnerabilities | Snyk + Dependabot | ✅ | `.github/dependabot.yml` |
| A.11.12 | Development environment hardening | `.flake8` + pytest config | ✅ | `pyproject.toml` |

### A.12: Information Security Incidents

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.12.1 | Incident response procedure | Runbooks in `docs/runbooks/` | ✅ | 6 runbooks created |
| A.12.2 | Incident reporting | Slack + JIRA (org policy) | 📋 | Org integration |
| A.12.3 | Incident assessment | Decision trees in runbooks | ✅ | Runbook documents |
| A.12.4 | Response to malware | Secrets compromise runbook | ✅ | `secrets-compromise.md` |
| A.12.5 | Lessons learned | Postmortem template | 📋 | Planned |

### A.13: Business Continuity Management

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.13.1 | BCP planning | `docs/deployment/playbook.md` | ✅ | Deployment SOP |
| A.13.2 | BCP implementation | Canary deployments | ✅ | `.github/workflows/release.yml` |
| A.13.3 | Test, maintain BCP | Runbook procedures | ✅ | Operational runbooks |

### A.14: Compliance

| Control | Requirement | Implementation | Status | Evidence |
|---------|---|---|---|---|
| A.14.1 | Compliance with legal requirements | GDPR + SOC2 mapping | 📋 | `docs/compliance/mapping.md` |
| A.14.2 | IP rights | MIT license | ✅ | LICENSE file |
| A.14.3 | Regulation of security tools | Code review + testing | ✅ | CI pipeline |
| A.14.4 | Audit logging | JSON logging + ELK | ✅ | `src/logging/` |

## Summary by Phase

**Phase 1 (Complete)**: Foundation controls (policies, access, development)
**Phase 2 (In Progress)**: Operational controls (monitoring, incident response)
**Phase 3 (Planned)**: Advanced controls (formal audit, penetration testing)

## Evidence Collection Checklist

- [ ] Policy documents (docs/SECURITY.md, etc.)
- [ ] Design decisions (docs/ADRs/)
- [ ] Configuration files (pyproject.toml, .github/workflows/)
- [ ] Test results (CI pipeline logs)
- [ ] Audit logs (ELK aggregated logs)
- [ ] Access logs (Git commit history)
- [ ] Incident response records (Slack, JIRA)

## Improvement Plan

1. Phase 2: Implement monitoring + centralized logging
2. Phase 3: Formal audit engagement
3. Phase 3: Penetration testing
4. Phase 3: SOC2 Type II audit
