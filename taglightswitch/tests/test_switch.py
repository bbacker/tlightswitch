import pytest
import taglightswitch
import datetime
import controltags

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    light = taglightswitch.TagLightSwitch()
    inst_list = light.find_tagged_instances()

    assert len(inst_list.keys()) > 0

def test_advise():
    light = taglightswitch.TagLightSwitch()
    light.advise()
