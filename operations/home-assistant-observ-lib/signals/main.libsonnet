// signals — merge every per-group signal file into one flat signals map.
// Each group file is function(cfg, sig) -> { name: signal }.
local signal = import 'libs/common-lib/signal/main.libsonnet';

function(cfg)
  local sig(name, expr, unit, desc='') =
    signal.new(name, 'prometheus', cfg.datasource, expr, unit)
    .filteringSelector(cfg.selector)
    .withDescription(desc);
  (import './overview.libsonnet')(cfg, sig)
  + (import './batteries.libsonnet')(cfg, sig)
  + (import './esphome.libsonnet')(cfg, sig)
  + (import './zha.libsonnet')(cfg, sig)
