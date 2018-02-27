import datetime
import re

class BadTagError(ValueError):
    """Wrap value exception in project custom error"""
    pass

class TagLightSwitch:

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

