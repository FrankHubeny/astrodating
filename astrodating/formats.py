# Licensed under a 3-clause BSD style license - see LICENSE.md
"""
:mod:`time` allows an AD/BC or CE/BCE or BP time format with an ability to convert
to another AstroPy format if the values are within the range of those
other formats.  

It uses a Year Zero.

NumPy's datetime64 supports the functionality and range of the times.
."""

import numpy as np

from astropy.time.formats import TimeString

class TimeADBC(TimeString):
    """
    Time based on NumPy's datetime64 values with AD/BC labels.
    """

    name = "adbc"
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