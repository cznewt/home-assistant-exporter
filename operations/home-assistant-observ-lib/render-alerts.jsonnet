// Prometheus alert rules from the mixin. Rendered by the observ-lib image:
// `render render-alerts.jsonnet > prometheus_alerts.yaml` (JSON is valid YAML).
(import './mixin.libsonnet').prometheusAlerts
