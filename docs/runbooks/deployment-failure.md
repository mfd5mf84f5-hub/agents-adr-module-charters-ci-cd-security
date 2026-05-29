# Deployment Failure Runbook

**Alert**: Deployment failed OR Pods stuck in CrashLoopBackOff

## Pre-Deployment Checklist

Before each deployment, verify:

- [ ] All tests passing (unit, integration, contract)
- [ ] Security scans clean
- [ ] SBOM reviewed
- [ ] Database migrations tested
- [ ] Configuration secrets available
- [ ] Rollback procedure tested
- [ ] Monitoring dashboards ready
- [ ] On-call engineer notified

## Deployment Failure Investigation

### Check Pod Events

```bash
# View recent events
kubectl describe deployment schema-architect

# Check pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # If restarting
```

### Common Failures

| Error | Cause | Solution |
|-------|-------|----------|
| `ImagePullBackOff` | Image not found / wrong tag | Check image registry; verify tag exists |
| `CrashLoopBackOff` | App startup failure | Check logs; verify config |
| `Pending` | Insufficient resources | Scale nodes; reduce resource requests |
| `OOMKilled` | Out of memory | Increase memory limit; check for leaks |
| `Liveness probe failed` | Health check failing | Check endpoint; increase timeout |

### Image Pull Failure

```bash
# Verify image exists
grep "image:" kubernetes/deployment.yaml

# Check registry credentials
kubectl get secret ghcr-secret -o yaml

# Test docker pull
docker pull ghcr.io/<image>:tag
```

### Application Startup Failure

```bash
# Check logs for errors
kubectl logs <pod> | tail -100

# Common startup issues:
# - Missing environment variables
# - Database migration failure
# - Invalid configuration
# - Schema registry unreachable

# Debug startup
kubectl run debug --image=<image> -it -- /bin/bash
```

### Configuration Issues

```bash
# Check secrets mounted
kubectl exec <pod> -- env | grep -i database

# Verify secrets exist
kubectl get secrets
kubectl describe secret <secret-name>

# If missing, create secret
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL=$DATABASE_URL
```

## Remediation

### Option 1: Rollback Immediately

**When**: Deployment is broken, known previous version was stable

```bash
# List deployment history
kubectl rollout history deployment/schema-architect

# Rollback to previous version
kubectl rollout undo deployment/schema-architect

# Verify
kubectl rollout status deployment/schema-architect
kubectl get pods
```

### Option 2: Fix and Redeploy

**When**: Fix is simple (config change, small bug)

```bash
# Fix issue in code
# Commit and push
# CI will auto-build and deploy

# Or manual redeployment
kubectl rollout restart deployment/schema-architect
```

### Option 3: Scale to Previous Version

**When**: Rolling update is failing

```bash
# Scale new version to 0
kubectl scale deployment schema-architect-new --replicas=0

# Verify old version is running
kubectl scale deployment schema-architect-old --replicas=3
```

## Post-Deployment Validation

```bash
# Wait for pods ready
kubectl rollout status deployment/schema-architect --timeout=5m

# Run smoke tests
curl http://localhost:8000/health

# Check metrics
curl http://localhost:8000/metrics | grep schema_architect_requests_total

# Verify no error spike
# Check Grafana Error Rate dashboard
```

## Escalation Path

1. **2 min**: Deployment stuck → Rollback immediately
2. **5 min**: Rollback failed → Page SRE
3. **15 min**: Production down → Page on-call Manager
4. **30 min**: Still down → Critical incident

## Post-Incident

1. Document failure scenario
2. Add pre-deployment check to prevent recurrence
3. Improve monitoring (catch issues earlier)
4. Update runbook

## Prevention

- Canary deployments (10% → 50% → 100%)
- Automated smoke tests post-deploy
- Blue-green deployments for zero downtime
- Feature flags for gradual rollout

## References

- Deployment guide: `docs/deployment/playbook.md`
- Release SOP: `docs/release/signing-sop.md`
