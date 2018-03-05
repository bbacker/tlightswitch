import pytest
import taglightswitch
import datetime
import controltags
import switchableitem

ec2inst=None # find better way to mock an instance
cls = switchableitem.SwitchableItem(ec2inst)

# TODO: this uses 'live' boto3 - need to mock that so test passes if not in
# contact with AWS
def test_find():
    light = taglightswitch.TagLightSwitch()
    inst_list = light.find_tagged_instances()

    assert len(inst_list.keys()) > 0

def test_advise():
    light = taglightswitch.TagLightSwitch()
    light.advise()

def test_advise():
    elevenPM = datetime.time(11 + 12, 0)
    fivePM = datetime.time(5 + 12, 0)
    tenPM = datetime.time(10 + 12, 0)
    eightAM = datetime.time(8,0)
    sixAM = datetime.time(6,0)

    # confirm that states other than running and stopped return unchanged
    assert "terminated" == cls._compute_recommended_power_state("terminated",
            [fivePM, sixAM], eightAM, "ON_OFF")

    # outside range, should be unchanged
    assert "running" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], eightAM, "ON_OFF")

    # inside range, should stop
    assert "stopped" == cls._compute_recommended_power_state("running",
            [fivePM, sixAM], tenPM, "ON_OFF")

    # inside range stoped, mode says leave off
    assert "stopped" == cls._compute_recommended_power_state("stopped",
            [fivePM, sixAM], tenPM, "leaveOFF")

    # offhours and stopped, leave off
    assert "stopped" == cls._compute_recommended_power_state("stopped",
            [fivePM, sixAM], tenPM, "ON_OFF")

    # not offhours (not inside range) and stopped, mode says power back up
    assert "running" == cls._compute_recommended_power_state("stopped",
            [tenPM, sixAM], fivePM, "ON_OFF")
