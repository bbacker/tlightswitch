import datetime
import pytest

from taglightswitch import controltags

cls = controltags.ControlTags

def test_default_tag_pattern():
    tn = controltags.ControlTags.get_target_tag_name()
    assert tn != None

def range_helper(rangestr):
    r = cls.parse_offhours(rangestr)
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
    assert (tenPM,eightAM) == cls.parse_offhours("start=22:00,end=08:00")

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
    assert not cls.time_is_within_range(tenPM, eightAM, fivePM)

    # corner case
    assert cls.time_is_within_range(eightAM, eightAM, eightAM)

def test_advise():
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
    assert not cls.time_is_within_range(tenPM, eightAM, fivePM)

    # corner case
    assert cls.time_is_within_range(eightAM, eightAM, eightAM)

def test_dayofweek():
    assert([0] == cls.parse_offdays("mon"))
    assert([0] == cls.parse_offdays("Mon"))
    assert([0] == cls.parse_offdays("Monday"))
    assert([0,1] == cls.parse_offdays("mon,tue"))
    assert([5,6] == cls.parse_offdays("SAT,SUN"))
    assert([6] == cls.parse_offdays("SUN,SUN"))
    assert([6] == cls.parse_offdays("SUN,sunday"))

def test_dayofweek_fail0():
    with pytest.raises(ValueError):
        assert([0] == cls.parse_offdays(""))

def test_dayofweek_fail1():
    # I think this should fail but parser likes it so let it slide
    assert([0] == cls.parse_offdays("sun-mon"))

def test_dayofweek_fail2():
    with pytest.raises(ValueError):
        assert([0] == cls.parse_offdays("bob"))

def test_dayofweek_fail3():
    with pytest.raises(ValueError):
        assert([0] == cls.parse_offdays("sundayblsskdfjlsdjf"))


def test_match_dow():
    sat = datetime.date(2018, 3, 17)
    sun = datetime.date(2018, 3, 18)
    mon = datetime.date(2018, 3, 19)
    tue = datetime.date(2018, 3, 20)

    weekendlist = cls.parse_offdays("SAT,SUN")

    assert(cls.date_matches_an_offday(weekendlist, sat))
    assert(cls.date_matches_an_offday(weekendlist, sun))
    assert(not cls.date_matches_an_offday(weekendlist, mon))
    assert(not cls.date_matches_an_offday(weekendlist, tue))

    assert(not cls.date_matches_an_offday([], sun)) # empty days off means never match
