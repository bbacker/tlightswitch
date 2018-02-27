import pytest
import taglightswitch
import datetime

cls = taglightswitch.TagLightSwitch

def range_helper(rangestr):
    r = cls._parse_timerange(rangestr)
    assert r
    assert r.start
    assert r.end
    return r.start, r.end

def test_csv():
    x = cls._parse_csvbody("key=val")
    assert x['key'] == "val"
    x = cls._parse_csvbody("key=val, key2=val2")
    assert "val2" == x["key2"]
    x = cls._parse_csvbody("key=, key2=")
    assert "" == x["key"]
    assert "" == x["key2"]

def test_ranges():
    tenPM = datetime.time(10 + 12, 0)
    eightAM = datetime.time(8,0)
    assert (tenPM,eightAM) == cls._parse_timerange("start=22:00,end=08:00")
    #assert ("2200", "0800") == cls._parse_timerange("start=10pm,end=8am")
