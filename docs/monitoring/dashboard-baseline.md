# Monitoring Baseline

This document defines the baseline monitoring infrastructure and dashboards for Agent A schema architect.

## Overview

- **Monitoring Stack**: Prometheus (metrics) + ELK (logs) + Grafana (dashboards)
- **Alerting**: PagerDuty for critical issues
- **SLA**: 99.5% uptime target
- **Dashboard Access**: Team members via Grafana

## Key Metrics

### Application Metrics

```
schema_registry_requests_total (counter)
  - labels: method, endpoint, status
  - example: schema_registry_requests_total{method="POST", endpoint="/schemas", status="201"}

schema_registry_request_duration_seconds (histogram)
  - labels: method, endpoint
  - buckets: 0.1, 0.5, 1.0, 5.0 seconds

schema_validations_total (counter)
  - labels: status (valid, invalid)

feature_extraction_duration_seconds (histogram)
  - labels: featurizer_type
  - Track performance of each featurizer

publish_hooks_total (counter)
  - labels: status (success, failure, timeout)
```

### Infrastructure Metrics

```
cpu_usage_percent (gauge)
  - target: < 70% during normal operation
  - alert: > 85%

memory_usage_percent (gauge)
  - target: < 80% during normal operation
  - alert: > 95%

disk_usage_percent (gauge)
  - alert: > 90%

network_bytes_in/out (counter)
  - Track bandwidth usage
  - Alert on anomalies
```

## Dashboards

### 1. Service Health Dashboard

**Purpose**: Real-time health of Agent A service

**Panels**:
- Uptime (SLA tracker)
- Error rate (% requests with 5xx)
- P95 latency
- Requests per second
- Top errors (by type)
- Service dependencies health

### 2. Performance Dashboard

**Purpose**: Performance trends and optimization

**Panels**:
- Request latency (p50, p95, p99)
- Throughput (requests/sec)
- Error rate (by endpoint)
- Feature extraction duration (by type)
- Feast feature store latency
- Schema validation performance

### 3. Resource Dashboard

**Purpose**: Infrastructure utilization

**Panels**:
- CPU usage
- Memory usage
- Disk I/O
- Network bandwidth
- Container restart count
- Pod status

### 4. Business Metrics Dashboard

**Purpose**: Feature adoption and usage

**Panels**:
- Total schemas registered
- Schemas by type (Product, Service, Platform, Tool)
- Feature extraction requests
- Publish hook invocations
- Active users / integrations
- Validation accuracy

### 5. Deployment Dashboard

**Purpose**: Deployment metrics and SLA

**Panels**:
- Deployment frequency
- Lead time for changes
- Deployment duration
- Deployment success rate
- Rollback count
- Canary phase durations

## Alerting Rules

### Critical (PagerDuty Immediate)

```
- Error rate > 5% (5-min average)
- Service unavailable (health check failures)
- Response time > 2 seconds (p95)
- Memory usage > 95%
- Disk usage > 95%
- Database connection pool exhausted
```

### High (PagerDuty with delay)

```
- Error rate > 1% (10-min average)
- Response time > 1 second (p95)
- CPU usage > 85%
- Feature extraction timeout
- Publish hook failure rate > 10%
```

### Medium (Slack notification)

```
- Response time > 500ms (p95)
- CPU usage > 70%
- Dependency (Feast) latency > 100ms
- Low cache hit rate (< 70%)
```

### Low (Metrics only)

```
- Deployment frequency < 1/week
- Test coverage < 75%
- SBOM not generated
```

## Logging Strategy

### Log Levels
- **ERROR**: Critical issues requiring action
- **WARN**: Unexpected conditions (handled gracefully)
- **INFO**: Important events (deployments, schema changes)
- **DEBUG**: Detailed troubleshooting (log to local file only)

### Structured Logging

All logs should include:
```json
{
  "timestamp": "2026-05-29T00:00:00Z",
  "level": "INFO",
  "service": "agent_a",
  "request_id": "abc123",
  "user_id": "user_123",
  "action": "schema_registered",
  "schema_id": "schema_1",
  "status": "success",
  "duration_ms": 45
}
```

### Log Retention
- **Application logs**: 30 days (hot)
- **Audit logs**: 1 year (cold)
- **Error logs**: 90 days (indexed)

## SLA & Error Budget

```
Target SLA: 99.5% uptime
Error budget: (1 - 0.995) * hours_in_month = ~3.6 hours/month of downtime

Monthly reporting:
- Actual uptime %
- Error budget remaining
- Top incidents and root causes
- Remediation items
```

## Runbooks

Runbooks linked from alerts for each critical scenario:

- High error rate: `runbooks/high-error-rate.md`
- High latency: `runbooks/high-latency.md`
- Out of memory: `runbooks/oom-investigation.md`
- Deployment failure: `runbooks/deployment-failure.md`
- Database connection issues: `runbooks/db-connection-issues.md`

## Implementation Phase

**Phase 1 (Now)**:
- [ ] Prometheus metrics instrumentation
- [ ] Grafana dashboards (basic)
- [ ] Alert rules (critical only)
- [ ] ELK logging setup

**Phase 2 (Sprint 2)**:
- [ ] Business metrics dashboards
- [ ] Deployment metrics
- [ ] Advanced alerting (anomaly detection)
- [ ] Slack/PagerDuty integration

**Phase 3 (Sprint 3+)**:
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Performance profiling
- [ ] Chaos engineering / failure injection
- [ ] Predictive alerting (ML-based)

## References

- `docs/deployment/playbook.md`: Deployment monitoring
- `docs/SECURITY.md`: Security monitoring
- `ADR 0003`: CI/CD Platform Choice
