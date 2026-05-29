# Threat Models

This document contains threat models for critical modules and data flows.

## agent_a (Schema Registry)

### Assets
- Schema definitions (source of truth)
- Validation logic (business rules)
- Publish hooks (external integrations)

### Threats

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Unauthorized schema modification | MEDIUM | HIGH | CODEOWNERS review, Git audit trail |
| Malformed schema causing DoS | MEDIUM | MEDIUM | Input validation, rate limiting |
| Schema information leakage | LOW | MEDIUM | Access control, encryption at rest |
| Publish hook compromise | LOW | HIGH | Hook validation, timeout, retry logic |
| Version conflict (race condition) | LOW | MEDIUM | Optimistic locking, version stamps |

### Controls
1. All schema changes require PR review (CODEOWNERS)
2. Schema validation against JSON Schema standard
3. Publish hooks have retry and timeout logic
4. Audit trail via Git (immutable)
5. Rate limiting on API endpoints

---

## feature_engineering (Featurizers)

### Assets
- Feature definitions
- Feast feature store integration
- Training data pipeline

### Threats

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Feature data leakage | MEDIUM | HIGH | Encryption, access control |
| Malicious feature injection | LOW | HIGH | Feature validation, schema contracts |
| Training data poisoning | LOW | MEDIUM | Data quality checks, anomaly detection |

### Controls
1. Feature schema validation (contract tests)
2. Data lineage tracking
3. Access control via Feast RBAC
4. Anomaly detection for feature values

---

## CI/CD Pipeline

### Assets
- Build artifacts
- Deployment secrets
- Release process

### Threats

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Compromised dependency | MEDIUM | HIGH | SCA, SBOM, vendor verification |
| Unauthorized artifact push | LOW | HIGH | Artifact signing, OIDC keyless |
| Secrets in workflow files | MEDIUM | HIGH | Secrets scanning in CI, code review |
| Build server compromise | LOW | CRITICAL | Isolated runners, minimal permissions |

### Controls
1. All dependencies pinned and scanned (SCA)
2. SBOM generated and reviewed per release
3. Artifacts signed with cosign + keyless OIDC
4. Secrets in GitHub Actions Secrets, never in code
5. detect-secrets scanning on every commit

---

## Next Steps
1. Review and sign-off on threat models (Phase 1)
2. Implement controls in code and CI (Phase 2)
3. Conduct security audit (Phase 3)
4. Implement runtime monitoring (Phase 3+)
