// panels — merge every per-group panel file into one flat elements map.
// Each group file is function(signals) -> { name: PanelKind }.
function(signals)
  (import './overview.libsonnet')(signals)
  + (import './batteries.libsonnet')(signals)
  + (import './esphome.libsonnet')(signals)
  + (import './zha.libsonnet')(signals)
