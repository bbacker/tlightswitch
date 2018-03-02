import pytest
import taglightswitch
import datetime
import controltags

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    light = taglightswitch.TagLightSwitch()

    tn = controltags.ControlTags.get_target_tag_name()
    assert tn != None
    inst_list = light.find_tagged_instances(tn)

    assert len(inst_list.keys()) > 0
