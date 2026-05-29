# SCA (Software Composition Analysis) Compliance

This document defines SCA requirements and integration points.

## Overview

- **Tool**: Snyk (planned), OSS Index (current)
- **Frequency**: On every PR and release
- **Coverage**: All dependencies in `pyproject.toml` and transitive dependencies
- **SBOM Format**: CycloneDX 1.4 JSON
- **Threshold**: Block on CRITICAL, warn on HIGH

## Dependency Requirements

### Pinning Strategy
- All dependencies must use **semantic versioning** (e.g., `>=1.0.0,<2.0.0`)
- No floating versions (e.g., ❌ `fastapi` or `fastapi>=1.0`)
- Security patches should be included (e.g., ✅ `>=1.0.5,<2.0.0`)
- Lock file (`requirements-lock.txt`) for production reproducibility

### Dependency Review Checklist
- [ ] Dependency has active maintenance (issues/PRs resolved)
- [ ] No known critical vulnerabilities (check OSS Index)
- [ ] License compatible with project (MIT/Apache 2.0 preferred)
- [ ] Dependency size reasonable (no bloat)
- [ ] Alternative considered (if popular replacement exists)

## SBOM Generation

### Tools
- **Python**: `cyclonedx-bom` (generates CycloneDX format)
- **Docker**: `syft` (if containerized)

### Generation

```bash
# Install
pip install cyclonedx-bom

# Generate SBOM
cyclonedx-bom -r -o sbom.json

# Validate format
jq . sbom.json > /dev/null && echo "Valid JSON"
```

### Contents
- Package name, version, license
- Component relationships and dependencies
- Vulnerability metadata (if available)
- Hashes (SHA256) for verification

## CI Integration

The CI pipeline generates SBOM on every PR:

```yaml
- name: Generate SBOM (CycloneDX)
  run: cyclonedx-bom -r -o sbom.json

- name: Upload SBOM
  uses: actions/upload-artifact@v3
  with:
    name: sbom
    path: sbom.json
```

Reviewers should download and verify the SBOM.

## Scanning Process

1. **Automated**: SCA tool scans dependencies on PR
2. **Review**: Maintainer reviews findings
3. **Action**:
   - CRITICAL: Require fix before merge
   - HIGH: Create issue for next sprint
   - MEDIUM/LOW: Document in release notes

## Vulnerability Response

If a vulnerability is discovered in a dependency:

1. **Assess**: Determine if project is affected
2. **Update**: Bump dependency to patched version
3. **Test**: Verify no breaking changes
4. **Release**: Push security patch (increment PATCH version)
5. **Communicate**: Notify users of security fix

See `docs/SECURITY.md` for SLA.

## Future Enhancements (Phase 3+)

- [ ] Integrate Snyk API for real-time scanning
- [ ] Automated dependency updates via Dependabot
- [ ] License compliance scanning
- [ ] Transitive dependency tracking
- [ ] Software composition dashboard
