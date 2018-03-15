import pytest
import taglightswitch
import datetime

enable_live_account_tests=False
enable_live_account_tests=True

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    if enable_live_account_tests:
        light = TagLightSwitch()
        inst_list = light.find_tagged_instances()
        assert len(inst_list.keys()) > 0

def test_advise():
    if enable_live_account_tests:
        light = TagLightSwitch()
        light.advise()
