import boto3
import datetime
import json
import re
import logging

class BadTagError(ValueError):
    """Wrap value exception in project custom error"""
    pass

class ControlTags:
    """tagged EC2 info and state"""

    @classmethod
    def get_target_tag_name(cls):
        return 'lightswitch:timerange'

    # take AWS tag body as CSV string, parse into dict
    @classmethod
    def parse_csvbody(cls,bodystr):
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

    @classmethod
    def _parse_timerange(cls,body):
        """ take AWS tag body, parse into start, end times""
        range_dict = cls._parse_csvbody(body)
        s = cls._parse_time(range_dict['start'])
        e = cls._parse_time(range_dict['end'])
        return s, e

    @classmethod
    def time_is_within_range(cls, range, time):
        """ does the given time fall within the timerange? """
        return True
