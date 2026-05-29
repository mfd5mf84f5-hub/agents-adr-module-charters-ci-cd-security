# Release Management SOP

This document defines the standard operating procedure for releasing Agent A schema architect.

## Overview

- **Release Cycle**: 2-week sprints with releases on Fridays
- **Version Scheme**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Artifacts**: Docker image, GitHub Release, SBOM, signed checksums
- **Sign-off**: Release Manager approval required

## Release Types

### Major Release (e.g., v2.0.0)
- **Breaking changes**: API changes, schema incompatibilities
- **Migration guide**: Required in release notes
- **Announcement**: Email to all users, 2-week notice
- **Support**: v1.x gets 6 months of security patches
- **Deployment**: Staged rollout (canary → 10% → 50% → 100%)

### Minor Release (e.g., v1.1.0)
- **New features**: Backward-compatible additions
- **Deprecations**: Warning in release notes, 2 releases before removal
- **Deployment**: Standard canary rollout

### Patch Release (e.g., v1.0.1)
- **Bug fixes**: No API changes
- **Security fixes**: Expedited SLA
- **Deployment**: Fast-track (1-hour SLA for approval)

## Release Workflow

### Phase 1: Preparation (Monday-Wednesday)

1. **Planning**
   - Identify features/fixes to include
   - Review PRs for quality and testing
   - Update CHANGELOG.md

2. **Testing**
   - Full regression test suite
   - Performance benchmarks
   - Security scans (SCA, SAST)
   - Integration tests across modules

3. **Documentation**
   - Release notes (features, bug fixes, breaking changes)
   - Migration guide (if major version)
   - Known issues / limitations

### Phase 2: Build & Sign (Thursday)

1. **Artifact Generation**
   ```bash
   # Tag release
   git tag -a v1.x.x -m "Release v1.x.x"
   git push origin v1.x.x
   
   # Trigger release workflow
   # - Build Docker image
   # - Run tests
   # - Generate SBOM
   # - Sign artifacts with cosign
   ```

2. **Artifact Signing**
   - Use keyless cosign + GitHub OIDC
   - Sign Docker image: `cosign sign ghcr.io/.../image:v1.x.x`
   - Sign checksums: `cosign sign-blob --key cosign.key checksums.txt`
   - Upload to GitHub Release

3. **SBOM Review**
   - Review CycloneDX SBOM for issues
   - Check for new dependencies
   - Verify no unexpected transitive deps

### Phase 3: Deployment (Friday)

1. **Dev Environment** (Automatic)
   - Deploy immediately after build
   - Smoke tests (15 min)
   - Approval: Automatic

2. **Staging Environment**
   - Manual approval: Release Manager
   - Full integration tests (1 hour)
   - Performance benchmarks
   - Soak testing (24-48 hours for minor/major)
   - Final approval

3. **Production**
   - Canary deployment (10% → 50% → 100%)
   - Monitoring (4-8 hours)
   - Final sign-off
   - Publish release notes

### Phase 4: Post-Release

1. **Announcement**
   - GitHub Release published
   - Email notification to users
   - Slack announcement in #releases
   - Twitter/blog (if major feature)

2. **Monitoring**
   - 24-hour post-release monitoring
   - Error tracking
   - User feedback channel

3. **Documentation**
   - Update README with latest version
   - Archive release notes
   - Update migration guides

## Signing Procedure

### Keyless Signing (Recommended)

```bash
# Prerequisites:
# - GitHub Actions OIDC token (automatic in GitHub)
# - cosign installed locally

# In CI/CD (automatic via GitHub Actions):
export COSIGN_EXPERIMENTAL=1
cosign sign ghcr.io/mfd5mf84f5-hub/agent-a:v1.x.x

# Verification:
cosign verify --certificate-identity https://github.com/mfd5mf84f5-hub/agents-adr-module-charters-ci-cd-security/.github/workflows/release.yml@refs/tags/v1.x.x ghcr.io/mfd5mf84f5-hub/agent-a:v1.x.x
```

### Manual Signing (If Local)

```bash
# Generate keys (one-time)
cosign generate-key-pair
# Prompts for password, creates cosign.key and cosign.pub

# Sign artifact
cosign sign --key cosign.key ghcr.io/mfd5mf84f5-hub/agent-a:v1.x.x

# Verify
cosign verify --key cosign.pub ghcr.io/mfd5mf84f5-hub/agent-a:v1.x.x
```

## Release Checklist

### Pre-Release
- [ ] CHANGELOG.md updated
- [ ] Version bumped (setup.py, __version__.py, pyproject.toml)
- [ ] Release notes written
- [ ] All tests passing
- [ ] Security scans clean
- [ ] SBOM reviewed
- [ ] Migration guide (if breaking)

### Build
- [ ] Docker image built
- [ ] Artifacts signed
- [ ] SBOM generated
- [ ] GitHub Release created
- [ ] Checksums calculated and signed

### Deployment
- [ ] Dev deployment successful
- [ ] Staging deployment successful
- [ ] Canary 10% successful
- [ ] Canary 50% successful
- [ ] Full production deployment
- [ ] Monitoring alerts configured
- [ ] User announcement sent

### Post-Release
- [ ] Documentation updated
- [ ] Known issues documented
- [ ] Runbook prepared
- [ ] Support team notified

## Rollback Procedure

See `docs/deployment/playbook.md` for detailed rollback steps.

## Version Support Matrix

| Version | Release Date | Support Until | Status |
|---|---|---|---|
| v2.0.0 | TBD | TBD | Future |
| v1.1.0 | 2026-06-30 | 2026-12-30 | Current |
| v1.0.0 | 2026-05-30 | 2026-11-30 | LTS |

## Emergency Release

For critical security fixes:

1. **Assess**: Determine if emergency release needed
2. **Fix**: Apply patch, test thoroughly
3. **Expedite**: Skip normal staging SLA (but not security checks)
4. **Release**: Tag and deploy immediately
5. **Notify**: Email all users of security fix
6. **Postmortem**: Review how vulnerability was introduced

Emergency release SLA: 4 hours from fix to production

## References

- `docs/deployment/playbook.md`: Deployment procedure
- `docs/SECURITY.md`: Security requirements
- `.github/workflows/release.yml`: Release automation
- `ADR 0003`: CI/CD Platform Choice
