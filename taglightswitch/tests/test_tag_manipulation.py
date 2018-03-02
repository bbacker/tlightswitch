import pytest
import controltags
import datetime
from pprint import pprint

cls = controltags.ControlTags

def range_helper(rangestr):
    r = cls.parse_timerange(rangestr)
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
    assert (tenPM,eightAM) == cls.parse_timerange("start=22:00,end=08:00")

def test_within_range():
    elevenPM = datetime.time(11 + 12, 0)
    fivePM = datetime.time(5 + 12, 0)
    tenPM = datetime.time(10 + 12, 0)
    eightAM = datetime.time(8,0)
    sixAM = datetime.time(6,0)
    # daytime off
    assert cls.time_is_within_range(eightAM, tenPM, fivePM)
    assert not cls.time_is_within_range(eightAM, fivePM, tenPM)

    # nighttime off
    assert cls.time_is_within_range(tenPM, eightAM, tenPM)
    assert cls.time_is_within_range(tenPM, eightAM, sixAM)
    assert cls.time_is_within_range(tenPM, eightAM, fivePM)

    # corner case
    assert cls.time_is_within_range(eightAM, eightAM, eightAM)
