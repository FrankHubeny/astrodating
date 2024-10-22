# Licensed under a 3-clause BSD style license - see LICENSE.md
"""
:mod:`format` allows an AD/BC or CE/BCE or BP time format with an ability to convert
to another AstroPy format if the values are within the range of those
other formats.  

These formats implement 
[astronomical year numbering](https://en.wikipedia.org/wiki/Astronomical_year_numbering) 
where 1 BC is the Year Zero as required by NumPy's datetime64 which is used
to implement the functionality with a wider range of dates than those offered
in AstroPy.
."""

import time
import warnings
import erfa

import numpy as np
import astropy.units as u
from astropy import constants as const
from astropy.time import Time
from astropy.time.formats import TimeUnique

__all__ = [
    "TimeBCAD",
]

class TimeBCAD(TimeUnique):
    """
    Time based on NumPy's datetime64 values with AD/BC labels.
    """

    name = "bcad"
    subfmts = (
        (
            "date_hms",
            "%Y-%m-%d %H:%M:%S AD",
            "{year:d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d}:{sec:02d} AD",
        ),
        (
            "date_hm",
            "%Y-%m-%dT%H:%M AD",
            "{year:d}-{mon:02d}-{day:02d}T{hour:02d}:{min:02d} AD",
        ),
        ("date", "%Y-%m-%d AD", "{year:d}-{mon:02d}-{day:02d} AD"),
    )