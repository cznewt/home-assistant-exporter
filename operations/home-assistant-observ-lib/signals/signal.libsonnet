// Signal factory bound to the lib config: returns sig(name, expr, unit, desc).
local signal = import 'libs/common-lib/signal/main.libsonnet';

function(this)
  function(name, expr, unit, desc='')
    signal.new(name, 'prometheus', this.datasource, expr, unit)
    .filteringSelector(this.selector)
    .withDescription(desc)
