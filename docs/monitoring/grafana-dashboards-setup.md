# Grafana Dashboard Provisioning

Create `grafana/provisioning/dashboards/` directory and place dashboard JSON files there.
Create `grafana/provisioning/datasources/prometheus.yml` with:

```yaml
apiVersion: 1

providers:
  - name: 'Prometheus'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /etc/grafana/provisioning/datasources

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

## Dashboard Definitions

See grafana-dashboards.json for complete Grafana dashboard definitions covering:
1. Service Health
2. Performance
3. Resources
4. Business Metrics
5. Deployment
