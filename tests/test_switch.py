import pytest
import taglightswitch
import datetime

from taglightswitch import switchableitem

ec2inst=None # find better way to mock an instance
cls = switchableitem.SwitchableItem(ec2inst)

def test_advise_times():
    elevenPM = datetime.time(11 + 12, 0)
    fivePM = datetime.time(5 + 12, 0)
    tenPM = datetime.time(10 + 12, 0)
    eightAM = datetime.time(8,0)
    sixAM = datetime.time(6,0)

    # confirm that states other than running and stopped return unchanged
    assert "terminated" == cls._compute_recommended_power_state("terminated",
            [fivePM, sixAM], eightAM, "toggle")

    # outside range, should be unchanged
    assert "running" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], eightAM, "toggle")

    # inside range, should stop
    assert "stopped" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], tenPM, "toggle")

    # inside range stopped, mode says leave off
    assert "stopped" == cls._compute_recommended_power_state("stopped",
            [fivePM, sixAM], tenPM, "leaveOFF")

    # offhours and stopped, leave off
    assert "stopped" == cls._compute_recommended_power_state("stopped",
            [fivePM, sixAM], tenPM, "toggle")

    # not offhours (not inside range) and stopped, mode says power back up
    assert "running" == cls._compute_recommended_power_state("stopped",
            [tenPM, sixAM], fivePM, "toggle")

    # not offhours (not inside range) and stopped, mode says leave off
    assert "stopped" == cls._compute_recommended_power_state("stopped",
            [tenPM, sixAM], fivePM, "leaveoff")

def test_advise_days():
    elevenPM = datetime.time(11 + 12, 0)
    fivePM = datetime.time(5 + 12, 0)
    tenPM = datetime.time(10 + 12, 0)
    eightAM = datetime.time(8,0)
    sixAM = datetime.time(6,0)

    sat = datetime.date(2018, 3, 17)
    sun = datetime.date(2018, 3, 18)
    mon = datetime.date(2018, 3, 19)
    tue = datetime.date(2018, 3, 20)

    weekendlist = [5,6] # sat, sun

    # confirm that states other than running and stopped return unchanged
    assert "terminated" == cls._compute_recommended_power_state("terminated",
            [fivePM, sixAM], eightAM, "toggle", weekendlist, sun)

    # empty offdays, remain unchanged
    assert "running" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], eightAM, "toggle", [], sun)

    # empty offdays, remain unchanged
    assert "running" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], eightAM, "toggle", [], sun)

    # not offhours but is offdays
    assert "stopped" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], eightAM, "toggle", weekendlist, sun)

    # offhours and offdays
    assert "stopped" == cls._compute_recommended_power_state("running",
            [fivePM, eightAM], sixAM, "toggle", weekendlist, sun)
