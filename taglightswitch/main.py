#!/usr/bin/env python

import taglightswitch
import datetime
from pprint import pprint
import switchableitem

# TODO: add mode OffOnly, OnOff

#now = datetime.datetime.now().time()
#lightswitcher = taglightswitch.TagLightSwitch(now)

#lightswitcher = taglightswitch.TagLightSwitch()

fake_time = datetime.time(11 + 12, 0) # 11PM

lightswitcher = taglightswitch.TagLightSwitch(fake_time)
switchable_list = lightswitcher.find_tagged_instances()

lightswitcher.advise()

#lightswitcher.correct()
