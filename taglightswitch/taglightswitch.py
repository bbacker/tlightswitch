import datetime
import logging

import boto3
import controltags
import switchableitem

class BadTagError(ValueError):
    """Wrap value exception in project custom error"""
    pass

class TagLightSwitch:
    """find and power off EC2 instances with lightswitch: tags"""

    def __init__(self, target_time=None):
        self.tag_pattern = controltags.ControlTags.get_target_tag_name()

        self.target_time = target_time
        if not self.target_time:
            self.target_time = datetime.datetime.now().time()
        self.ec2 = None
        self.logger = logging.getLogger(__name__)

        self.switchable_list = {}
        self.session = None
        self.ec2 = None
        self.caller_identity = None
        self.account = None

    # fetch or initialize boto3 client
    def _get_ec2(self):
        if not self.ec2:
            self.session = boto3.session.Session()
            self.ec2 = self.session.resource('ec2')
            caller_identity = boto3.client('sts').get_caller_identity()
            self.aws_info = {}
            self.aws_info['account']= caller_identity['Account']
            self.aws_info['profile_name']= self.session.profile_name
            self.aws_info['access_key']= self.session.get_credentials().access_key
        self.logger.debug('boto: %s', self.ec2)

        return self.ec2

    def find_tagged_instances(self):
        """return flattened keys and instance IDs for instances with lightswitch tags"""
        ec2 = self._get_ec2()

        instances = ec2.instances.all() # TODO: make smarter match with filter
        found_instances = {}

        for instance in instances:
            # if tags is NoneType, no tags and iterate will die so just add all to found lists
            if instance.tags:
                for this_tag in instance.tags:
                    if this_tag["Key"].startswith(self.tag_pattern):
                        found_instances[instance] = switchableitem.SwitchableItem(instance)
                        break

        self.switchable_list = found_instances
        return found_instances

    def dump_aws_info(self):
        return "AWSaccount={} AWSprofile={} access_key={}".format(self.account, self.session.profile_name, self.session.get_credentials().access_key)

    def advise(self):
        if not self.switchable_list.keys():
            self.find_tagged_instances()

        advice = {}

        sw_dict = self.switchable_list.items()
        advice['aws_info'] = self.aws_info
        advice['target_time'] = self.target_time.isoformat()

        advice['advice_per_item'] = {}
        for (inst, switchable_item) in sw_dict:
            this_advice = switchable_item.advise_power_state(self.target_time)
            advice['advice_per_item'][inst.id]=this_advice

        return advice

    def correct(self):
        if not self.switchable_list.keys():
            self.find_tagged_instances()

        sw_dict = self.switchable_list.items()
        print(self.dump_aws_info())
        print("correct power states for {} switchable items for target time {}".format(len(sw_dict), self.target_time.isoformat()))
        for (inst, switchable_item) in sw_dict:
            correction_text = switchable_item.correct_power_state(self.target_time)
            print(correction_text)
