# Compliance Mapping

This document maps organizational controls to code, tests, and monitoring.

**Status**: Framework defined; detailed mapping in Phase 2

## Control Categories

### Access Control

| Control | Requirement | Implementation | Status |
|---|---|---|---|
| AC-1 | CODEOWNERS enforcement | .github/CODEOWNERS + branch protection | ✅ Done |
| AC-2 | Secrets management | GitHub Actions Secrets | ✅ Done |
| AC-3 | Role-based access | GitHub organization teams | 📋 Planned |

### Change Management

| Control | Requirement | Implementation | Status |
|---|---|---|---|
| CM-1 | PR review required | CODEOWNERS + branch protection | ✅ Done |
| CM-2 | Change log | CHANGELOG.md + git history | ✅ Done |
| CM-3 | Audit trail | Git commits with signatures | 📋 Planned |
| CM-4 | Rollback capability | Blue-green deployment | 📋 Planned |

### Security Testing

| Control | Requirement | Implementation | Status |
|---|---|---|---|
| ST-1 | SAST scanning | Bandit in CI | ✅ Done |
| ST-2 | DAST scanning | Integration tests | 📋 Planned |
| ST-3 | Dependency scanning | SCA + CycloneDX | ✅ Done |
| ST-4 | Secret scanning | detect-secrets | ✅ Done |

### Data Protection

| Control | Requirement | Implementation | Status |
|---|---|---|---|
| DP-1 | Data classification | docs/compliance/classification.md | 📋 Planned |
| DP-2 | Encryption at rest | TBD (Phase 3) | 🔲 Future |
| DP-3 | Encryption in transit | TLS 1.2+ | 🔲 Future |
| DP-4 | Data retention | Defined per data type | 📋 Planned |

### Monitoring & Logging

| Control | Requirement | Implementation | Status |
|---|---|---|---|
| ML-1 | Centralized logging | ELK stack | 📋 Planned |
| ML-2 | Event logging | Structured JSON logs | ✅ Done |
| ML-3 | Log retention | 30/90/365 days | 📋 Planned |
| ML-4 | Alerting | PagerDuty integration | 📋 Planned |

## Compliance Frameworks

### GDPR
- **Data Processing**: Documented in data classification
- **Right to be Forgotten**: Data retention policy defined
- **Audit Trail**: All schema changes logged
- **DPA**: Vendor agreements (Phase 3)

### SOC2
- **Security**: Access control, vulnerability management ✅
- **Availability**: Uptime monitoring, incident response 📋
- **Processing Integrity**: Data validation, schema contracts ✅
- **Confidentiality**: Secrets management, encryption (planned)
- **Privacy**: Data handling policy 📋

### ISO 27001
- **A.5-A.18**: Information security controls
- **Mapping**: To be completed in Phase 2

## Artifact Traceability

All code artifacts map to:
1. Requirement → Code → Test → Control
2. Example:
   - Requirement: "All schemas must be version controlled"
   - Code: `src/agent_a/schema_registry.py` (versioning logic)
   - Test: `tests/contract_tests/test_schema_versioning.py`
   - Control: CM-1 (Change Management)

## Next Steps

1. **Phase 2**: Complete detailed control mapping
2. **Phase 2**: Map requirements to test cases
3. **Phase 3**: Audit trail implementation
4. **Phase 3**: Formal compliance audit

## References

- `docs/security/threat-models.md`: Risk assessment
- `docs/SECURITY.md`: Security baseline
- `.github/PULL_REQUEST_TEMPLATE.md`: Process enforcement
