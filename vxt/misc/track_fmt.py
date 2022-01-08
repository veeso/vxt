# VXT
# Developed by Christian Visintin
#
# MIT License
# Copyright (c) 2021 Christian Visintin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from datetime import datetime
import re
from typing import List, Callable, Any, Optional
from vxt.audio.track import Track

# FmtFn: wrkstr, prepend, track
FmtFn = Callable[[Track], str]
Callchain = List[FmtFn]
# Regex
FMT_REGEX: str = r"%(?:([%,d,H,M,m,S,s,t,y,Y]))(\.(?:(\d+)))?"


class TrackFmt(object):
    """Track filename fmt.
    The syntax use parameters which must be preceeded by `%`, everything in between will be kept the same.
    The following parameters are supported.

    - %%: print percentage symbol
    - %d: current day
    - %H: current hours
    - %I: current timestamp ISO8601 syntax
    - %M: current minutes
    - %m: current month
    - %S: current seconds
    - %s: track speech
    - %s.NUMBER track speech cut at length (e.g. `%s.24`)
    - %t: track number in track list (from 1 to n)
    - %y: current year with 2 digits
    - %Y: current year with 4 digits
    """

    def __init__(self, fmt: str, regex: Optional[Any] = None) -> None:
        super().__init__()
        self.__fmt = fmt
        if not regex:
            regex = re.compile(FMT_REGEX)
        self.__build(fmt, regex)

    def fmt(self, wrkstr: str, track: Track) -> str:
        """Fmt incoming str according to callchain"""
        arg = self.__func(track)
        if self.__len:
            arg = arg[: self.__len]
        wrkstr = "%s%s%s" % (wrkstr, self.__prepend, arg)
        # Call next block
        if self.__next:
            return self.__next.fmt(wrkstr, track)
        else:
            return wrkstr

    # callchain constructor
    def __build(self, wrkstr: str, regex: Any) -> None:
        # Find first
        result = regex.search(wrkstr)
        if result:
            # Prepend
            self.__prepend = wrkstr[: result.start()]
            # Parse
            keyword = result.group(1)
            if result.group(3):
                self.__len = int(result.group(3))
            else:
                self.__len = None
            # Get new working string
            wrkstr = wrkstr[result.end() :]
            # Get func
            self.__func = TrackFmt.__get_fmt_func(keyword)
            # Process remainign string
            self.__next = TrackFmt(wrkstr, regex)
        else:
            # Return dummy
            self.__func = TrackFmt.__fmt_none
            self.__prepend = wrkstr
            self.__len = None
            self.__next = None

    @staticmethod
    def __get_fmt_func(keyword: str) -> FmtFn:
        if keyword == "%":
            return TrackFmt.__fmt_percentage
        elif keyword == "d":
            return TrackFmt.__fmt_day
        elif keyword == "H":
            return TrackFmt.__fmt_hours
        elif keyword == "I":
            return TrackFmt.__fmt_iso8601
        elif keyword == "M":
            return TrackFmt.__fmt_minutes
        elif keyword == "m":
            return TrackFmt.__fmt_month
        elif keyword == "S":
            return TrackFmt.__fmt_second
        elif keyword == "s":
            return TrackFmt.__fmt_speech
        elif keyword == "t":
            return TrackFmt.__fmt_track_number
        elif keyword == "y":
            return TrackFmt.__fmt_year
        elif keyword == "Y":
            return TrackFmt.__fmt_fullyear
        else:
            raise NotImplementedError

    # Fmt functions
    @staticmethod
    def __fmt_none(t: Track) -> str:
        return ""

    @staticmethod
    def __fmt_percentage(t: Track) -> str:
        return "%%"

    @staticmethod
    def __fmt_day(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%d")

    @staticmethod
    def __fmt_hours(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%H")

    @staticmethod
    def __fmt_iso8601(t: Track) -> str:
        now = datetime.now()
        return now.astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

    @staticmethod
    def __fmt_minutes(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%M")

    @staticmethod
    def __fmt_month(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%m")

    @staticmethod
    def __fmt_second(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%S")

    @staticmethod
    def __fmt_speech(t: Track) -> str:
        return t.speech.replace(" ", "_")

    @staticmethod
    def __fmt_track_number(t: Track) -> str:
        return t.index + 1

    @staticmethod
    def __fmt_year(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%y")

    @staticmethod
    def __fmt_fullyear(t: Track) -> str:
        now = datetime.now()
        return now.strftime("%Y")

    def __repr__(self) -> str:
        return repr(self.__fmt)

    def __str__(self) -> str:
        return self.__fmt
