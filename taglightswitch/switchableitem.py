import boto3
import datetime
import json
import re
import logging
import controltags

class SwitchableItem:
    """tagged EC2 info and state"""

    def get_tags(self):
        return self.tags

    def get_off_range(self):
        return self.off_range

    def get_power_state(self):
        """ what is the current power state of the item?"""
        return self.instance.state["Name"]

    def get_recommended_power_state(self, current_time):
        """given the current time and the power range in tags, should instance be on or off?"""
        if controltags.ControlTags.time_is_within_range(self.off_range, current_time):
            return "within time range, power off"
        else:
            return "outside time range, no change"

    def set_power_state(self, state):
        """set the power to the given state"""
        # TODO start_instances()
        # TODO stop_instances()
        return self.instance.state["Name"]

    def __init__(self, instance):
        self.ec2=None
        self.tgt_tag_name = 'lightswitch:timerange'
        self.logger = logging.getLogger(__name__)

        self.instance = instance

        self.tags={}
        if instance.tags:
            for thisTag in instance.tags:
                k = thisTag["Key"]
                v = thisTag["Value"]
                self.tags[k]=v
                if k == self.tgt_tag_name:
                    self.off_range_tag = v
                    self.off_range = controltags.ControlTags.parse_timerange(v)
