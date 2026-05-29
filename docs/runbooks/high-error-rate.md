# High Error Rate Incident Runbook

**Alert**: Error rate > 1% (sustained for 5+ minutes)

## Severity Levels

- 🔴 **CRITICAL**: Error rate > 5% — Immediate response required
- 🟠 **HIGH**: Error rate > 1% — Investigate within 15 minutes
- 🟡 **MEDIUM**: Error rate > 0.5% — Monitor closely

## Initial Triage (First 2 minutes)

1. **Acknowledge Alert**
   - [ ] Page on-call engineer (PagerDuty)
   - [ ] Post to #incidents Slack channel
   - [ ] Check if this is a known issue (JIRA)

2. **Assess Scope**
   - [ ] Is error rate increasing or stable?
   - [ ] Which endpoints are affected?
   - [ ] How many users impacted?
   - Command: `curl http://localhost:9090/api/query?query=rate(schema_architect_requests_total{status=~"5.."}"`

3. **Check Recent Deployments**
   - [ ] Was there a recent release (last 30 mins)?
   - [ ] Check: `git log --oneline -5`
   - [ ] If yes: Consider immediate rollback (see below)

## Investigation (2-10 minutes)

### Decision Tree

```
┌─ Recent deployment? ──→ YES ──→ [ROLLBACK]
│                   └─→ NO
├─ Database errors in logs?
│  ├─ YES ──→ [DATABASE TROUBLESHOOTING]
│  └─ NO
├─ Schema validation failures?
│  ├─ YES ──→ Check schema registry health
│  └─ NO
├─ Timeout errors?
│  ├─ YES ──→ Check CPU/Memory usage
│  └─ NO
└─ Unknown/5xx errors ──→ [ESCALATE]
```

### Log Investigation

```bash
# Query recent errors
curl 'http://localhost:5601/api/console/proxy' \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "index": "schema-architect-*",
    "query": {
      "match": {"level": "ERROR"}
    },
    "size": 100
  }'

# Filter by endpoint
kibana_query='level:ERROR AND endpoint:/schemas'

# Count errors by type
grepkibana 'exception' schema-architect-* | sort | uniq -c | sort -rn
```

### Metrics to Check

```
Grafana: Service Health Dashboard
- Error Rate (graph): Expected < 0.1%
- P95 Latency: Expected < 500ms
- CPU Usage: Expected < 70%
- Memory Usage: Expected < 80%
- Active Requests: Should not spike
```

## Root Cause Analysis

| Symptom | Likely Cause | Investigation |
|---------|--------------|----------------|
| Sudden spike after deployment | Code regression | Roll back; check PR diffs |
| Gradual increase over time | Memory leak / resource exhaustion | Check memory trend; restart if needed |
| Timeout errors | Slow database / overloaded | Check DB query time; scale up |
| Validation errors | Schema changed | Check schema registry for recent updates |
| Intermittent errors | Race condition / deadlock | Check logs for patterns; increase thread pool |

## Remediation

### Option 1: Immediate Rollback

**When**: Recent deployment is the cause

```bash
# Get current version
kubectl get deployment schema-architect -o jsonpath='{.spec.template.spec.containers[0].image}'

# Rollback to previous
kubectl rollout undo deployment/schema-architect

# Verify
kubectl rollout status deployment/schema-architect
```

**SLA**: Complete within 5 minutes

### Option 2: Restart Service

**When**: Memory leak suspected, no recent deployment

```bash
kubectl rollout restart deployment/schema-architect

# Monitor recovery
kubectl logs -f deployment/schema-architect --tail=50
```

### Option 3: Scale Up

**When**: Resource exhaustion (CPU/Memory high)

```bash
# Increase replicas
kubectl scale deployment schema-architect --replicas=5

# Monitor error rate recovery
watch -n 5 'kubectl top pods -l app=schema-architect'
```

## Escalation Path

1. **15 min**: No progress → Notify Tech Lead
2. **30 min**: Still ongoing → Page on-call Manager
3. **1 hour**: Unresolved → Critical incident (CEO notification)

## Post-Incident

1. **Document**
   - [ ] Root cause confirmed
   - [ ] Timeline of events
   - [ ] Resolution steps

2. **Postmortem** (within 24 hours)
   - [ ] What happened?
   - [ ] Why did it happen?
   - [ ] How to prevent?
   - [ ] Action items

3. **Follow-up**
   - [ ] Implement preventive monitoring
   - [ ] Add circuit breaker / fallback
   - [ ] Update runbook

## References

- Dashboard: http://grafana:3000/d/service-health
- Logs: http://kibana:5601
- Metrics: http://prometheus:9090
- ADR 0003: CI/CD Platform Choice
