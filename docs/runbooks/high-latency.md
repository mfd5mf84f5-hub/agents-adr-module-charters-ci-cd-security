# High Latency Incident Runbook

**Alert**: P95 latency > 1000ms (or > 2x baseline)

## Severity Levels

- 🔴 **CRITICAL**: P95 latency > 2000ms OR > 5x baseline
- 🟠 **HIGH**: P95 latency > 1000ms OR > 3x baseline
- 🟡 **MEDIUM**: P95 latency > 500ms OR > 2x baseline

## Baseline Targets (SLA)

| Endpoint | Target | Alert |
|----------|--------|-------|
| `/schemas` | 50ms | > 250ms |
| `/schemas/{id}` | 100ms | > 500ms |
| `/validate` | 200ms | > 1000ms |
| `/features/extract` | 500ms | > 2500ms |
| Feast query | 100ms | > 250ms |

## Initial Triage (First 2 minutes)

1. **Verify Alert**
   - [ ] Is latency still elevated?
   - [ ] Is error rate normal (< 0.5%)?
   - [ ] Affected endpoints: ??
   - Query: `histogram_quantile(0.95, schema_architect_request_duration_seconds)`

2. **Check Resource Utilization**
   ```bash
   # CPU
   kubectl top nodes
   kubectl top pods -l app=schema-architect
   
   # Memory
   kubectl describe node <node-name>
   
   # Disk I/O
   iostat -x 1 10
   ```

3. **Is Database Slow?**
   ```sql
   -- Check slow queries
   SELECT query, calls, mean_exec_time
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC LIMIT 10;
   
   -- Check connections
   SELECT count(*) FROM pg_stat_activity;
   ```

## Investigation (2-15 minutes)

### Decision Tree

```
┌─ CPU > 80%? ──→ YES ──→ [SCALE UP / OPTIMIZE]
│           └─→ NO
├─ Memory > 85%? ──→ YES ──→ [MEMORY INVESTIGATION]
│             └─→ NO
├─ Disk I/O > 70%? ──→ YES ──→ [DISK INVESTIGATION]
│               └─→ NO
├─ Database latency > 100ms? ──→ YES ──→ [DATABASE TUNING]
│                        └─→ NO
├─ Network latency? ──→ YES ──→ [NETWORK INVESTIGATION]
│              └─→ NO
└─ Code/Application ──→ [PROFILING]
```

### Profiling Commands

```bash
# Profile current requests (Python)
py-spy record -o profile.svg -d 60 --pid <PID>

# Flamegraph
perf record -F 99 -p <PID> -g -- sleep 60
perf report

# Trace slow requests
kubectl logs <pod> | grep 'duration_ms' | sort -t: -k2 -rn | head -20
```

### Performance Metrics

```
Grafana: Performance Dashboard
- Request Duration (graph): P50, P95, P99
- Database Query Time: < 100ms
- Feature Extraction: < 500ms
- Cache Hit Rate: > 80%
- Queue Depth: Should be stable
```

## Root Cause Analysis

| Symptom | Likely Cause | Investigation |
|---------|--------------|----------------|
| All endpoints slow | CPU/Memory exhausted | Check resource dashboard |
| Only validation slow | Schema change / regression | Check schema size; profile validator |
| Intermittent slowness | GC pauses / context switching | Check GC logs; increase heap |
| Progressive slowness | Memory leak / cache growth | Check memory trend; restart |
| Database queries slow | Missing index / table scan | Run EXPLAIN ANALYZE; add index |
| Network latency | Network congestion / DNS | Check latency distribution; trace network |

## Remediation

### Option 1: Increase Resources

```yaml
kubectl set resources deployment schema-architect \
  --limits=cpu=2,memory=2Gi \
  --requests=cpu=1,memory=1Gi
```

### Option 2: Enable Caching

```python
# Add result caching
from functools import lru_cache
import time

@lru_cache(maxsize=1000)
def validate_schema(schema_id, ttl=3600):
    # Check TTL
    current_time = time.time()
    if hasattr(validate_schema, '_cache_time'):
        if current_time - validate_schema._cache_time > ttl:
            validate_schema.cache_clear()
    validate_schema._cache_time = current_time
    # ... validation logic
```

### Option 3: Database Optimization

```sql
-- Add missing indexes
CREATE INDEX idx_schemas_type ON schemas(type);
CREATE INDEX idx_schemas_status ON schemas(status, created_at);

-- Analyze table
ANALYZE schemas;
```

### Option 4: Code Optimization

```python
# Profile and optimize hot path
profile_data = cProfile.run('validate_schema(...)')
pstats.Stats(profile_data).sort_stats('cumulative').print_stats(10)
```

## Escalation Path

1. **5 min**: > 5x baseline → Page SRE team
2. **15 min**: No improvement → Notify Tech Lead
3. **30 min**: Still critical → Consider rollback

## Post-Incident

1. **Identify bottleneck** (profiling data)
2. **Fix root cause** (code optimization / infrastructure)
3. **Add monitoring** (low-latency alert at 2x baseline)
4. **Document** (update SLA / runbook)

## References

- Dashboard: http://grafana:3000/d/performance
- Logs: http://kibana:5601
- Metrics: http://prometheus:9090
- Profiling: `py-spy`, `perf`, `cProfile`
