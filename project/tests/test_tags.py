import pytest
import taglightswitch

# class TestTags(object):
#    def test_one(self):
#
#    def test_two(self):
#        x = "hello"
#        assert hasattr(x, 'check')


def test1():
    t = TagLightSwitch.tag_to_dict("mytagname","start=10pm,end=8am")
    assert "2200" == t.start 
