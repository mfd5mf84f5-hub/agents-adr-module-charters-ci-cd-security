# ADR 0003: CI/CD Platform Choice

## Status
**Accepted**

## Context
The project requires a CI/CD platform to:
- Run automated tests and linters on every PR
- Enforce code quality gates and security scans
- Generate SBOMs and manage artifacts
- Support deployment automation and canary releases

**Problem:**
- Need reliable, scalable CI/CD without heavy operational burden
- Must integrate with GitHub for PR feedback
- Should support future multi-environment deployments (dev, staging, prod)

## Decision
Use **GitHub Actions** as the primary CI/CD platform:

1. **PR Gate Checks**
   - Linting (flake8, black)
   - Unit tests (pytest with 75% coverage minimum)
   - Contract tests (schema validation)
   - SCA scanning (Snyk, OSS Index)
   - SBOM generation (CycloneDX)

2. **Build & Release Pipeline**
   - Docker image build on release tag
   - Artifact signing (cosign)
   - Push to artifact registry (GitHub Packages or DockerHub)
   - Automatic deployment to canary environment

3. **Observability & Notifications**
   - Workflow status to PR comments
   - Slack notifications on failure
   - Build time tracking for performance trends

4. **Configuration**
   - All workflows in `.github/workflows/`
   - Reusable workflow components for DRY principle
   - Secrets managed via GitHub Repository Secrets

## Consequences

**Positive:**
- ✅ No separate infrastructure to manage (fully hosted)
- ✅ Tight integration with GitHub (native PR feedback)
- ✅ Good free tier for public repos
- ✅ Rich ecosystem of pre-built actions
- ✅ OIDC support for keyless signing

**Negative:**
- ❌ Vendor lock-in to GitHub
- ❌ Limited customization compared to self-hosted (Jenkins, GitLab CI)
- ❌ Costs scale with minutes on private repos

**Mitigation:**
- Parameterize workflows for portability
- Use widely-supported tools (pytest, flake8) as abstraction
- Monitor costs and switch if needed (Phase 2 evaluation)

## Alternatives Rejected
1. **GitLab CI**: Requires separate infrastructure; more complex
2. **Jenkins**: Requires self-hosted runner; operational burden
3. **Cloud Native (AWS CodePipeline, GCP Cloud Build)**: Tighter coupling; vendor specific

## Implementation
- Main workflow: `.github/workflows/ci.yml` (PR gate)
- Release workflow: `.github/workflows/release.yml` (manual trigger)
- Canary workflow: `.github/workflows/canary.yml` (scheduled)
- Template workflows in `.github/workflows/templates/` for reuse

## CI Gate Checks (in order)
1. **Lint & Format** (fail fast)
2. **Unit Tests + Coverage**
3. **Contract Tests** (schema validation)
4. **Security Scans** (SCA, secret detection)
5. **SBOM Generation**
6. **Artifact Signing** (release only)

## Future Enhancements (Phase 3+)
- Multi-environment deployments with approval gates
- Performance benchmarking with regression detection
- Automated dependency updates (Dependabot)
- Integration with external SCA tools (Snyk API)
- Custom branch protection rules

## Related ADRs
- ADR 0002: Schema Governance Approach (contract tests in CI)
- ADR 0001: Agent Model Selection (no impact on CI/CD)

---

**Approved by:** DevOps & Security Team  
**Date:** 2026-05-27  
**Authors:** @mfd5mf84f5-hub