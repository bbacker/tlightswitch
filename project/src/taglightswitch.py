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

    # take AWS tag name (key) and body (value), parse into start, end times
    @classmethod
    def _parse_timerange(cls,body):
        range_dict = cls._parse_csvbody(body)
        return range_dict['start'], range_dict['end']

