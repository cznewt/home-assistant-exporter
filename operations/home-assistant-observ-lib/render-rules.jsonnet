// Prometheus recording rules from the mixin. Rendered by the observ-lib image:
// `render render-rules.jsonnet > prometheus_rules.yaml` (JSON is valid YAML).
(import './mixin.libsonnet').prometheusRules
