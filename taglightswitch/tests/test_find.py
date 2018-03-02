import pytest
import taglightswitch
import datetime
from pprint import pprint

def test_find():
    light = taglightswitch.TagLightSwitch()

    assert light.tgt_tag_name != None
    inst_list = light.find_tagged_instances(light.tgt_tag_name)

    assert len(inst_list.keys())> 0

    pprint(inst_list)
