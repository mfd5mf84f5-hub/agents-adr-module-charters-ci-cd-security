# Database Connection Failure Runbook

**Alert**: Database connection errors > 10% OR "No available connections" error

## Severity Levels

- 🔴 **CRITICAL**: All connections exhausted
- 🟠 **HIGH**: > 50% connections in use
- 🟡 **MEDIUM**: Connection errors appearing

## Initial Triage (First 2 minutes)

1. **Verify Database is Reachable**
   ```bash
   # Check connectivity
   nc -zv <db-host> 5432
   
   # Test credentials
   psql -h <host> -U <user> -d schema_architect -c "SELECT 1"
   ```

2. **Check Connection Pool Status**
   ```bash
   # From app logs
   kubectl logs <pod> | grep -i "pool\|connection"
   
   # Database side
   psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='schema_architect';"
   ```

3. **Is Database Slow?**
   ```bash
   # Query latency
   kubectl exec <pod> -- curl -s http://localhost:8000/health | jq '.database_latency_ms'
   ```

## Investigation (2-10 minutes)

### Decision Tree

```
┌─ Cannot ping database? ──→ YES ──→ [NETWORK ISSUE]
│                    └─→ NO
├─ Credentials wrong? ──→ YES ──→ [CREDENTIALS ISSUE]
│              └─→ NO
├─ Too many connections? ──→ YES ──→ [CONNECTION POOL]
│                  └─→ NO
├─ Database is slow? ──→ YES ──→ [DATABASE PERFORMANCE]
│             └─→ NO
└─ Intermittent ──→ [TIMEOUT / NETWORK ISSUE]
```

### Network Troubleshooting

```bash
# Ping database
ping <db-host>

# DNS resolution
nslookup <db-host>

# Trace route
traceroute <db-host>

# Check firewall
telnet <db-host> 5432
```

### Connection Pool Analysis

```sql
-- Current connections
SELECT datname, usename, application_name, state, count(*)
FROM pg_stat_activity
GROUP BY datname, usename, application_name, state;

-- Idle connections (potential leak)
SELECT pid, usename, application_name, state_change
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '1 minute';

-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '5 minutes';
```

### Credentials Check

```bash
# Verify environment variables
kubectl get secret <db-secret> -o yaml | grep -i password

# Test credentials
DATABASE_URL="postgresql://user:pass@host:5432/db"
psql "$DATABASE_URL" -c "SELECT 1"
```

## Root Cause Analysis

| Symptom | Likely Cause | Investigation |
|---------|--------------|----------------|
| All connections in use | Connection leak / high load | Check query time; profile app |
| Intermittent failures | Network timeout / DNS | Check traceroute; increase timeout |
| Credentials rejected | Wrong password / user | Verify in secrets manager |
| Cannot reach database | Network down / firewall | Check network status; DNS |
| Slow queries | Missing index / table lock | Run EXPLAIN ANALYZE; check locks |
| Connection refused | Database not running | Check database pod status |

## Remediation

### Option 1: Kill Idle Connections

```sql
-- Terminate long-idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < now() - interval '10 minutes'
AND pid <> pg_backend_pid();
```

### Option 2: Increase Connection Pool

```yaml
# Kubernetes secret / app config
env:
  - name: DATABASE_POOL_SIZE
    value: "20"  # Increase from 10
  - name: DATABASE_MAX_OVERFLOW
    value: "10"
```

### Option 3: Restart Database Connection

```bash
# Restart database pod
kubectl delete pod <db-pod>

# Kubernetes will auto-recreate
kubectl wait --for=condition=ready pod/<db-pod> --timeout=300s
```

### Option 4: Scale Application

```bash
# More instances = less connections per pod
kubectl scale deployment schema-architect --replicas=5
```

## Escalation Path

1. **2 min**: Database unreachable → Page Database team
2. **5 min**: Credentials issue → Check secrets; rotate if needed
3. **15 min**: Persistent problem → Page SRE
4. **30 min**: Database down → Initiate failover

## Post-Incident

1. **Root cause** (network / database / app)
2. **Permanent fix** (update pool size / add monitoring)
3. **Prevention** (connection limit alerts)
4. **Documentation** (update runbook)

## Prevention

- Connection pool monitoring
- Alert at 50%, 80%, 95% utilization
- Automated killing of idle connections (>10 min)
- Regular backups + failover testing

## References

- PostgreSQL docs: https://www.postgresql.org/docs/current/runtime-config-connection.html
- SQLAlchemy pooling: https://docs.sqlalchemy.org/en/20/core/pooling.html
