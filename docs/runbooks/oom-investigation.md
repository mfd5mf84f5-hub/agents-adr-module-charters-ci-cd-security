# Out of Memory (OOM) Incident Runbook

**Alert**: Memory usage > 95% OR Container killed due to OOM

## Severity Levels

- 🔴 **CRITICAL**: OOM Kill (pod restarting) — Immediate response
- 🟠 **HIGH**: Memory > 95% — Investigate now
- 🟡 **MEDIUM**: Memory > 80% — Monitor closely

## Initial Triage (First 2 minutes)

1. **Check Pod Status**
   ```bash
   kubectl describe pod <pod-name>
   # Look for: "OOMKilled", "CrashLoopBackOff"
   
   kubectl logs <pod-name> --tail=50
   ```

2. **Memory Usage Trend**
   ```bash
   # Current
   kubectl top pod <pod-name>
   
   # Over time (Grafana)
   # Query: schema_architect_memory_usage_percent
   ```

3. **Check if Transient or Persistent**
   - Transient spike: Temporary load (queue processing)
   - Persistent growth: Memory leak (requires restart)

## Investigation (2-10 minutes)

### Memory Leak Detection

```python
# Enable memory profiling
pip install memory-profiler

# Run with profiling
mprof run -M <script.py>
mprof plot mprofile_*.dat

# Trace memory allocations
from tracemalloc import start, take_snapshot
start()
# ... application code ...
snapshot = take_snapshot()
for stat in snapshot.statistics('lineno'):
    print(stat)
```

### Check for Common Leaks

```python
# 1. Unbounded caches
import sys
print(sys.getsizeof(cache_dict))  # Check cache size

# 2. Growing lists
print(f"Active schemas: {len(schema_cache)}")

# 3. Open connections
import gc
gc.get_objects()  # Find unreleased objects
```

### Heap Dump Analysis

```bash
# Generate heap dump
jmap -dump:live,format=b,file=heap.bin <PID>

# Analyze with Eclipse Memory Analyzer
# Or use Python's pympler
pip install pympler
from pympler import asizeof
print(f"Schema cache size: {asizeof.asizeof(cache)} bytes")
```

## Root Cause Analysis

| Symptom | Likely Cause | Investigation |
|---------|--------------|----------------|
| Gradual growth (weeks) | Memory leak in cache | Check cache eviction policy |
| Sudden spike | Large batch operation | Check recent schema uploads |
| OOM on restart | Insufficient limits | Check pod resource requests |
| All pods OOM | System-wide issue | Check node memory; scale nodes |

## Remediation

### Option 1: Immediate Restart

**When**: OOMKilled, investigate later

```bash
kubectl rollout restart deployment/schema-architect

# Monitor logs
kubectl logs -f deployment/schema-architect
```

**Side effects**: Brief service disruption (< 1 min)

### Option 2: Increase Memory Limits

**When**: Legitimate need for more memory

```yaml
kubectl set resources deployment schema-architect \
  --limits=memory=2Gi \
  --requests=memory=1Gi
```

**Cost**: More expensive infrastructure

### Option 3: Fix Memory Leak

**When**: Leak identified (requires code fix)

```python
# Example: Add cache size limits
from functools import lru_cache

@lru_cache(maxsize=1000)  # Bounded cache
def get_schema(schema_id):
    # ... fetch logic
    pass

# Or use weakref for auto-cleanup
import weakref
schema_cache = weakref.WeakValueDictionary()
```

**Deploy**: Create PR, merge, deploy fix

### Option 4: Scale Horizontally

**When**: Load requires more instances

```bash
kubectl scale deployment schema-architect --replicas=5
```

## Escalation Path

1. **Immediate**: OOMKilled → Restart pod + investigate
2. **5 min**: Memory > 90% → Increase limits temporarily
3. **30 min**: Confirmed leak → Page Platform team
4. **1 hour**: Leak unresolved → Escalate to CTO

## Post-Incident

1. **Profile memory** (generate heap dump)
2. **Identify leak source** (lines of code)
3. **Fix code** (add limits, fix algorithm)
4. **Add monitoring** (alert at 80% usage)
5. **Postmortem** (document findings)

## Prevention

- Set memory requests/limits appropriately
- Use bounded caches (LRU, WeakValueDictionary)
- Profile regularly (monthly)
- Monitor memory trends (catch growth early)

## References

- Dashboard: http://grafana:3000/d/resources
- Memory profiling: `memory-profiler`, `pympler`, `tracemalloc`
- Heap analysis: `jmap`, `Eclipse MAT`
