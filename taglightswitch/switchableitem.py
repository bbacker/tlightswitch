import logging

import boto3
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

    # make separate class methods so easier to unit test without real EC2 data
    @classmethod
    def mode_is_toggle(cls, mode):
        return mode.lower() == "on_off"

    @classmethod
    def mode_is_off_only(cls, mode):
        return mode.lower() == "leaveoff"

    @classmethod
    def _compute_recommended_power_state(cls, current_state, off_range, current_time, lightswitchmode):

        # possible states are  (pending | running | shutting-down | terminated | stopping | stopped ).
        # rule 1: we will only consider instances in the 'running' or 'stopped'
        # states, leave instances in any other states unchanged
        if not (current_state.lower() == 'stopped' or
                current_state.lower() == 'running'):
            return current_state

        offhours = controltags.ControlTags.time_is_within_range(off_range[0], off_range[1], current_time)

        # rule 2: offhours powered on so turn off
        if offhours and current_state == "running":
            return "stopped"

        # rule 3: onhours, powered off, turn back on if mode is correct
        if (not offhours) and (current_state == "stopped") and SwitchableItem.mode_is_toggle(lightswitchmode):
            return "running"

        return current_state

    def _to_hash(self):
        h={}
        h['instance_id']=self.instance.id
        h['name']=self.name
        h['offhours']=self.off_range[0].strftime("%H:%M") + ' - ' + self.off_range[1].strftime("%H:%M")
        return h

    def advise_power_state(self, current_time):
        presentstate = self.get_power_state()
        nextstate = SwitchableItem._compute_recommended_power_state(presentstate, self.off_range, current_time, self.mode)
        advice = '  {}  current={}  desired={}'.format(self, presentstate, nextstate)
        advice = {}
        advice['switchable_item'] = self._to_hash()
        advice['current_state'] = presentstate
        advice['desired_state'] = nextstate
        return advice

    def correct_power_state(self, current_time):
        presentstate = self.get_power_state()
        nextstate = SwitchableItem._compute_recommended_power_state(presentstate, self.off_range, current_time, self.mode)

        # TODO: new boto3 client each time, optimization = reuse parent's
        toprint = "NO OP"
        if presentstate == "stopped" and nextstate == "running":
            response = boto3.client('ec2').start_instances(InstanceIds=[self.instance.id])
            toprint = "ACTION=POWERON (result={})".format(response)

        if presentstate == "running" and nextstate == "stopped":
            # note Force is default which is false
            response = boto3.client('ec2').stop_instances(InstanceIds=[self.instance.id])
            toprint = "ACTION=POWEROFF (result={})".format(response)

        correction = '  {}  current={}  desired={}\n       {}'.format(self, presentstate, nextstate, toprint)
        return correction

    def __init__(self, instance):
        self.ec2 = None
        self.name = ''
        self.tgt_tag_name = 'lightswitch:offhours'
        self.logger = logging.getLogger(__name__)
        self.mode = "ON_OFF" # TODO: add override

        if instance:
            self.instance = instance

            self.tags = {}
            if instance.tags:
                for this_tag in instance.tags:
                    k = this_tag["Key"]
                    v = this_tag["Value"]
                    self.tags[k] = v
                    if k == self.tgt_tag_name:
                        self.off_range_tag = v
                        self.off_range = controltags.ControlTags.parse_offhours(v)
                    if k.lower() == 'name':
                        self.name = v

    def __str__(self):
        return "switchable({}/{}, offrange={}-{})".format(self.instance.id, self.name, self.off_range[0].strftime("%H:%M"), self.off_range[1].strftime("%H:%M"))
