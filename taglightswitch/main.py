#!/usr/bin/env python

import pytest
import taglightswitch
import datetime
from pprint import pprint
import switchableitem

light = taglightswitch.TagLightSwitch()

inst_list = light.find_tagged_instances(light.tgt_tag_name)

pprint(inst_list)

tgt='lightswitch:timerange'

now = datetime.datetime.now().time()

for (inst, si) in inst_list.items():
    # print inst, current power state, time range, tod, recommended state
    pprint (inst)
    pprint (si)
    pprint (si.get_power_state())
    pprint (si.get_off_range())
    pprint (now)
    pprint (si.get_recommended_power_state(now))
