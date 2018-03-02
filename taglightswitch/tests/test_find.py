import pytest
import taglightswitch
import datetime

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    light = taglightswitch.TagLightSwitch()

    assert light.tgt_tag_name != None
    inst_list = light.find_tagged_instances(light.tgt_tag_name)

    assert len(inst_list.keys())> 0
