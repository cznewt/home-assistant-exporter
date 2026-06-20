# Integrations

The exporter exposes every series on a single `/metrics` endpoint, so any
Prometheus-compatible collector can scrape it — one static target, no
multi-target relabeling.

## Prometheus

```yaml
scrape_configs:
  - job_name: home-assistant-exporter
    static_configs:
      - targets: ["home-assistant-exporter:9878"]
```

## Grafana Alloy

Scrape the exporter and forward the samples to your metrics backend:

```alloy
prometheus.scrape "home_assistant" {
  targets    = [{ __address__ = "home-assistant-exporter:9878" }]
  forward_to = [prometheus.remote_write.default.receiver]
  job_name   = "home-assistant-exporter"
}

prometheus.remote_write "default" {
  endpoint {
    url = "http://prometheus:9090/api/v1/write"
  }
}
```

For Grafana Cloud, point `prometheus.remote_write` at the stack's Prometheus
push URL with `basic_auth` (credentials from the environment):

```alloy
prometheus.remote_write "default" {
  endpoint {
    url = sys.env("METRICS_PRIMARY_URL")
    basic_auth {
      username = sys.env("METRICS_PRIMARY_USER")
      password = sys.env("METRICS_PRIMARY_PASSWORD")
    }
  }
}
```

!!! tip "Ready-made Alloy scenarios"
    [`cznewt/alloy-resources`](https://github.com/cznewt/alloy-resources) ships
    drop-in Alloy [scenarios](https://github.com/cznewt/alloy-resources/tree/main/scenarios)
    (Grafana Cloud, HassOS, Docker, …) with the `prometheus.remote_write` plumbing
    already wired up — add a `prometheus.scrape` for this exporter to the one that
    matches your environment (e.g. the
    [HassOS scenario](https://github.com/cznewt/alloy-resources/tree/main/scenarios/hassos)).

## Alerting

The metrics are ordinary gauges, so you can alert on them directly:

```yaml
groups:
  - name: home-assistant
    rules:
      - alert: HassDeviceBatteryLow
        expr: hass_device_battery_remaining < 15
        for: 1h
        labels: { severity: warning }
        annotations:
          summary: "{{ $labels.device_name }} battery at {{ $value }}%"

      - alert: HassDeviceUnavailable
        expr: hass_device_available == 0
        for: 15m
        labels: { severity: warning }
        annotations:
          summary: "{{ $labels.device_name }} is unavailable"
```

See [Metrics](metrics.md) for the full list of series and labels.
