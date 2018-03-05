#!/usr/bin/env python

import taglightswitch
import datetime
from pprint import pprint
import switchableitem

#now = datetime.datetime.now().time()
#lightswitcher = taglightswitch.TagLightSwitch(now)

# TODO: add mode OffOnly, OnOff

lightswitcher = taglightswitch.TagLightSwitch()
switchable_list = lightswitcher.find_tagged_instances()

lightswitcher.advise()

lightswitcher.correct()
