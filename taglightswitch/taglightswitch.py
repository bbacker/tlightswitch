import boto3
import datetime
import json
import re
import logging

class BadTagError(ValueError):
    """Wrap value exception in project custom error"""
    pass

class TagLightSwitch:
    """find and power off EC2 instances with lightswitch: tags"""

    # take AWS tag body as CSV string, parse into dict
    @classmethod
    def _parse_csvbody(cls,bodystr):
        body = {}
        items = bodystr.split(',')
        rx = re.compile(r'\s*(?P<key>\w+)\s*=\s*(?P<value>.*)')
        for i in items:
            match = rx.match(i)
            if match and match.group('key'):
                body[match.group('key').lower()] = match.group('value')
            else:
                raise BadTagError("bad CSV string: " + i)
        return body

    @classmethod
    def _parse_time(cls, timestr):
        from dateutil import parser
        t = parser.parse(timestr)
        return t.time()

    # take AWS tag name (key) and body (value), parse into start, end times
    @classmethod
    def _parse_timerange(cls,body):
        range_dict = cls._parse_csvbody(body)
        s = cls._parse_time(range_dict['start'])
        e = cls._parse_time(range_dict['end'])
        return s, e



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
            k={}
            # if tags is NoneType, no tags and iterate will die so just add all to found lists
            if instance.tags:
                for thisTag in instance.tags:
                    k[thisTag["Key"]]=thisTag["Value"]
                    if thisTag["Key"].startswith(tag_pattern):
                        found=True
                if found:
                    found_instances[instance]=k

        return found_instances
