import boto3
import datetime
import json
import re
import logging
import switchableitem

class BadTagError(ValueError):
    """Wrap value exception in project custom error"""
    pass

class TagLightSwitch:
    """find and power off EC2 instances with lightswitch: tags"""

    def __init__(self):
        self.tgt_tag_name = 'lightswitch:timerange'

        self.ec2=None
        self.logger = logging.getLogger(__name__)

    # fetch or initialize boto3 client
    def _get_ec2(self):
        if not self.ec2:
            region = 'us-west-2'
            session = boto3.session.Session()
            self.ec2 = session.resource('ec2')
        self.logger.debug('boto: %s', self.ec2)
        return self.ec2

    def find_tagged_instances(self, tag_pattern):
        """return flattened keys and instance IDs for instances with lightswitch tags"""
        ec2 = self._get_ec2()

        instances = ec2.instances.all()
        found_instances = {}

        for instance in instances:
            found=False
            # if tags is NoneType, no tags and iterate will die so just add all to found lists
            if instance.tags:
                for thisTag in instance.tags:
                    if thisTag["Key"].startswith(tag_pattern):
                        found_instances[instance] = switchableitem.SwitchableItem(instance)
                        break

        return found_instances
