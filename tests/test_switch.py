import pytest
import taglightswitch
import datetime

from taglightswitch import switchableitem

ec2inst=None # find better way to mock an instance
cls = switchableitem.SwitchableItem(ec2inst)

def test_advise():
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
