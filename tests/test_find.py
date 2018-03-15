import pytest
import datetime

from taglightswitch import lightswitch

#enable_live_account_tests=True
enable_live_account_tests=False

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    if enable_live_account_tests:
        ls = lightswitch.LightSwitch()
        inst_list = ls.find_tagged_instances()
        assert len(inst_list.keys()) > 0

def test_advise():
    if enable_live_account_tests:
        ls = lightswitch.LightSwitch()
        ls.advise()
