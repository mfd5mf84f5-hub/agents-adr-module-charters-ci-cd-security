# Deployment Playbook

This playbook defines the process for deploying the Agent A schema architect to production environments.

## Overview

- **Environments**: Dev, Staging, Production
- **Deployment Tool**: GitHub Actions (automated via CI/CD)
- **Deployment Strategy**: Blue-green with canary rollout
- **Rollback Strategy**: Automatic on health check failure
- **Communication**: Slack notifications on deployment events

## Pre-deployment Checklist

- [ ] All tests passing (unit, integration, contract)
- [ ] Security scans passing (SCA, SAST, secrets)
- [ ] Code review approved (CODEOWNERS)
- [ ] SBOM generated and reviewed
- [ ] Release notes prepared
- [ ] Runbook updated
- [ ] Monitoring dashboards verified
- [ ] Rollback procedure tested

## Deployment Process

### Stage 1: Build & Artifact Preparation

```bash
# Triggered on: Release tag (e.g., v1.0.0)
# Steps:
# 1. Checkout code
# 2. Run full test suite
# 3. Build Docker image
# 4. Sign image with cosign (keyless OIDC)
# 5. Push to artifact registry (GitHub Container Registry)
# 6. Generate SBOM
# 7. Create GitHub Release with artifacts
```

### Stage 2: Dev Environment

**Trigger**: Automatic on main branch commits

```bash
# Deploy to Dev
# - Pull latest image
# - Run smoke tests (schema registry endpoints)
# - Monitor logs for errors (5 min window)
# - Notify team on success/failure
```

### Stage 3: Staging Environment

**Trigger**: Manual approval after Dev success

```bash
# Deploy to Staging
# - Blue-green deployment (parallel old + new)
# - Run integration tests
# - Run E2E tests
# - Performance benchmarks
# - Soak testing (24-48 hours)
# - Manual smoke tests
# - Approval from Release Manager
```

### Stage 4: Production - Canary Rollout

**Trigger**: Manual approval after Staging success

```bash
# Canary Phase 1: 10% of traffic
# - Deploy new version alongside stable
# - Monitor error rate, latency, resource usage
# - Health checks every 1 min
# - Alert if error rate > 1% or latency > 500ms
# - If failed: automatic rollback

# Canary Phase 2: 50% of traffic (after 30 min at 10%)
# - Increase traffic to 50%
# - Continue monitoring
# - If stable for 30 min, proceed

# Canary Phase 3: 100% of traffic (after 30 min at 50%)
# - Route all traffic to new version
# - Stable version becomes "previous"
# - Keep old version running for 1 hour for quick rollback
```

### Stage 5: Monitoring & Validation

```
Duration: 4-8 hours post-deployment

Metrics to monitor:
- Error rate (target: < 0.1%)
- P95 latency (target: < 500ms)
- CPU usage (target: < 70%)
- Memory usage (target: < 80%)
- Schema validation success rate (target: > 99%)

Alerts:
- Slack notification on any anomaly
- PagerDuty for critical issues
- Auto-rollback if error rate > 5%
```

## Rollback Procedure

### Automatic Rollback Triggers
- Error rate > 5%
- Health checks fail (3 consecutive)
- Memory/CPU usage > 95%
- Database connection failure

### Manual Rollback

```bash
# If automatic rollback doesn't work:
gh workflow run rollback.yml --ref main

# Or manually:
git tag -d v1.x.x.rollback
git push -d origin v1.x.x.rollback
gh workflow run deploy.yml -f target_version=v1.(x-1).x
```

### Post-Rollback
- Notify stakeholders
- Investigate root cause
- Document in incident report
- Schedule postmortem

## Monitoring & Observability

### Key Dashboards
- **Deployment Dashboard**: Deployment frequency, duration, success rate
- **Performance Dashboard**: Request latency, error rate, throughput
- **Resource Dashboard**: CPU, memory, disk usage
- **Business Metrics**: Schema registrations, validations, publish hooks

### Logging
- All logs streamed to centralized system (ELK, Datadog)
- Log retention: 30 days
- Critical events indexed for alerting

### Alerting
- On-call rotation: Email + PagerDuty
- Alert escalation: 15 min, then manager
- Runbook linked in every alert

## Incident Response

If deployment causes production issue:

1. **Immediately**: Initiate automatic rollback
2. **Within 5 min**: Notify stakeholders (Slack #incidents)
3. **Within 15 min**: PagerDuty alert to on-call
4. **Within 1 hour**: Post-incident review started

## Deployment Windows

- **Standard**: Tuesday-Thursday 10am-2pm UTC
- **Emergency**: 24/7 for critical security fixes
- **Maintenance windows**: Friday after 5pm (no new deployments)

## Approval Matrix

| Stage | Required Approver | SLA |
|---|---|---|
| Dev | Automatic | N/A |
| Staging | Release Manager | 4 hours |
| Canary (10%) | Release Manager | 4 hours |
| Production (100%) | Tech Lead + Release Manager | 2 hours |
| Rollback | On-Call Engineer | Immediate |

## References

- `docs/release/signing-sop.md`: Artifact signing procedure
- `docs/monitoring/dashboard-baseline.md`: Monitoring setup
- `.github/workflows/deploy.yml`: Deployment automation
- `ADR 0003`: CI/CD platform choice (GitHub Actions)
