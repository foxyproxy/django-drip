"""
This file was taken from Matthew Schinckel's django-timedelta-field project.

https://bitbucket.org/schinckel/django-timedelta-field/src/225c5d61394000ccb8e903ecaf8c092853898ffe/timedelta/helpers.py?at=default

Copyright (c) 2012, Matthew Schinckel.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL MATTHEW SCHINCKEL BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime
import re

from django.utils import six


def parse(string):
    """
    Parse a string into a timedelta object.

    >>> parse("1 day")
    datetime.timedelta(1)
    >>> parse("2 days")
    datetime.timedelta(2)
    >>> parse("1 d")
    datetime.timedelta(1)
    >>> parse("1 hour")
    datetime.timedelta(0, 3600)
    >>> parse("1 hours")
    datetime.timedelta(0, 3600)
    >>> parse("1 hr")
    datetime.timedelta(0, 3600)
    >>> parse("1 hrs")
    datetime.timedelta(0, 3600)
    >>> parse("1h")
    datetime.timedelta(0, 3600)
    >>> parse("1wk")
    datetime.timedelta(7)
    >>> parse("1 week")
    datetime.timedelta(7)
    >>> parse("1 weeks")
    datetime.timedelta(7)
    >>> parse("2 wks")
    datetime.timedelta(14)
    >>> parse("1 sec")
    datetime.timedelta(0, 1)
    >>> parse("1 secs")
    datetime.timedelta(0, 1)
    >>> parse("1 s")
    datetime.timedelta(0, 1)
    >>> parse("1 second")
    datetime.timedelta(0, 1)
    >>> parse("1 seconds")
    datetime.timedelta(0, 1)
    >>> parse("1 minute")
    datetime.timedelta(0, 60)
    >>> parse("1 min")
    datetime.timedelta(0, 60)
    >>> parse("1 m")
    datetime.timedelta(0, 60)
    >>> parse("1 minutes")
    datetime.timedelta(0, 60)
    >>> parse("1 mins")
    datetime.timedelta(0, 60)
    >>> parse("2 ws")
    Traceback (most recent call last):
    ...
    TypeError: '2 ws' is not a valid time interval
    >>> parse("2 ds")
    Traceback (most recent call last):
    ...
    TypeError: '2 ds' is not a valid time interval
    >>> parse("2 hs")
    Traceback (most recent call last):
    ...
    TypeError: '2 hs' is not a valid time interval
    >>> parse("2 ms")
    Traceback (most recent call last):
    ...
    TypeError: '2 ms' is not a valid time interval
    >>> parse("2 ss")
    Traceback (most recent call last):
    ...
    TypeError: '2 ss' is not a valid time interval
    >>> parse("")
    Traceback (most recent call last):
    ...
    TypeError: '' is not a valid time interval
    >>> parse("1.5 days")
    datetime.timedelta(1, 43200)
    >>> parse("3 weeks")
    datetime.timedelta(21)
    >>> parse("4.2 hours")
    datetime.timedelta(0, 15120)
    >>> parse(".5 hours")
    datetime.timedelta(0, 1800)
    >>> parse(" hours")
    Traceback (most recent call last):
        ...
    TypeError: ' hours' is not a valid time interval
    >>> parse("1 hour, 5 mins")
    datetime.timedelta(0, 3900)

    >>> parse("-2 days")
    datetime.timedelta(-2)
    >>> parse("-1 day 0:00:01")
    datetime.timedelta(-1, 1)
    >>> parse("-1 day, -1:01:01")
    datetime.timedelta(-2, 82739)
    >>> parse("-1 weeks, 2 days, -3 hours, 4 minutes, -5 seconds")
    datetime.timedelta(-5, 11045)
    """
    if string == "":
        raise TypeError("'%s' is not a valid time interval" % string)
    # This is the format we get from sometimes Postgres, sqlite,
    # and from serialization
    d = re.match(r'^((?P<days>[-+]?\d+) days?,? )?(?P<sign>[-+]?)(?P<hours>\d+):'
                 r'(?P<minutes>\d+)(:(?P<seconds>\d+(\.\d+)?))?$',
                 six.text_type(string))
    if d:
        d = d.groupdict(0)
        if d['sign'] == '-':
            for k in 'hours', 'minutes', 'seconds':
                d[k] = '-' + d[k]
        d.pop('sign', None)
    else:
        # This is the more flexible format
        d = re.match(
                     r'^((?P<weeks>-?((\d*\.\d+)|\d+))\W*w((ee)?(k(s)?)?)(,)?\W*)?'
                     r'((?P<days>-?((\d*\.\d+)|\d+))\W*d(ay(s)?)?(,)?\W*)?'
                     r'((?P<hours>-?((\d*\.\d+)|\d+))\W*h(ou)?(r(s)?)?(,)?\W*)?'
                     r'((?P<minutes>-?((\d*\.\d+)|\d+))\W*m(in(ute)?(s)?)?(,)?\W*)?'
                     r'((?P<seconds>-?((\d*\.\d+)|\d+))\W*s(ec(ond)?(s)?)?)?\W*$',
                     six.text_type(string))
        if not d:
            raise TypeError("'%s' is not a valid time interval" % string)
        d = d.groupdict(0)

    return datetime.timedelta(**dict(( (k, float(v)) for k,v in d.items())))


