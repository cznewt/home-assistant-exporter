# home-assistant-exporter

- get diagnostic properties of connected devices

## Configuration

```
integrations:
  - zha
  - esphome
```

## Supported metrics

| Metric name| Metric type | Description | Unit (where applicable) | Labels/tags | Status |
| ---------- | ----------- | ----------- | ----------------------- | ----------- | ------ |
| hass_device_info | Gauge | Information about the device | | `manufacturer`=&lt;manufacturer&gt; <br> `model`=&lt;model-version&gt; <br> `sw_version`=&lt;sw-version&gt; <br> `hw_version`=&lt;hw-version&gt; <br> `id`=&lt;unique-id&gt; | STABLE |
| hass_device_name | Gauge | Human name of the device | | `name`=&lt;human-name&gt; <br> `id`=&lt;unique-id&gt; | STABLE |
| hass_device_esp_signal_strength | Gauge | Signal of the ESP device | | `ap_name`=&lt;ap-name&gt; <br> `ap_essid`=&lt;ap-essid&gt; <br> `id`=&lt;unique-id&gt; | STABLE |