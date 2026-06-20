# Prometheus

The exporter exposes all series on a single `/metrics` endpoint, so scrape it
like any other exporter — one static target, no multi-target relabeling.

```yaml
scrape_configs:
  - job_name: home-assistant-exporter
    static_configs:
      - targets: ["home-assistant-exporter:9878"]
```

## Alerting

The metrics are ordinary gauges, so you can alert on them directly. A couple of
examples:

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
