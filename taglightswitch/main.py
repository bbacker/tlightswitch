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

print ('{} {} {} {} {}'.format( "instance", "current state", "range", "now",
    "recommended state"))

for (inst, si) in inst_list.items():
    print ('{} {} {} {} {}'.format( inst, si.get_power_state(),
            si.get_off_range(), now, si.get_recommended_power_state(now)))
    #pprint (si)
    #pprint (si.get_power_state())
    #pprint (si.get_off_range())
    #pprint (now)
    #pprint (si.get_recommended_power_state(now))
