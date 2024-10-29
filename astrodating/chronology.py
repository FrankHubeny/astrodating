# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""


import ast

import numpy as np
import pandas as pd

__all__ = [
    'Calendar',
    'Chronology',
]

CONSTANTS = {
    'DATETIME_EPOCH': 1970,
}

CALENDARS = {
    'BEFORE_PRESENT' : {
        'NAME' : 'Before Present',
        'POSLABEL' : '',
        'NEGLABEL' : ' BP',
        'ZEROYEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USEZERO' : False,
    },
    'EXPERIMENT' : {
        'NAME' : 'Experiment',
        'POSLABEL' : '',
        'NEGLABEL' : '',
        'ZEROYEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USEZERO' : False,
    },
    'GREGORIAN' : {
        'NAME' : 'Gregorian',
        'POSLABEL' : ' AD',
        'NEGLABEL' : ' BC',
        'ZEROYEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USEZERO' : False,
    },
    'SECULAR' : {
        'NAME' : 'Secular',
        'POSLABEL' : ' CE',
        'NEGLABEL' : ' BCE',
        'ZEROYEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USEZERO' : False,
    },
}

KEYS = {
    'ACTORS' : 'Actors',
    'AREA' : 'Area',
    'BEGIN' : 'Begin',
    'CALENDAR' : 'Calendar',
    'DESCRIPTION' : 'Description',
    'DISPLAYNAME' : 'Display Name',
    'END' : 'End',
    'EVENTS' : 'Events',
    'FEMALE' : 'Female',
    'FILE' : 'File Name',
    'MALE' : 'Male',
    'NAME' : 'Name',
    'PERIODS' : 'Periods',
    'SUBPERIOD' : 'Subperiod',
    'UNIT' : 'Unit',
}

AREAS = {
    'ASSYRIA' : 'Assyria',
    'BABYLONIA' : 'Babylonia',
    'EGYPT' : 'Egypt',
    'ISRAEL' : 'Israel',
    'ANE' : 'Ancient Near East',
}

# Date and time units from https://numpy.org/doc/stable/reference/arrays.datetime.html
DATETIMES = {
    'ATTOSECOND' : 'as',
    'DAY' : 'D',
    'FEMTOSECOND' : 'fs',
    'HOUR' : 'h',
    'MICROSECOND' : 'us',
    'MILLISECOND' : 'ms',
    'MINUTE' : 'm',
    'MONTH' : 'M',
    'NANOSECOND' : 'ns',
    'PICOSECOND' : 'ps',
    'SECOND' : 's',
    'WEEK' : 'W',
    'YEAR' : 'Y',
}

CHRONOLOGIES = {
    'BYZANTINE' : {KEYS['DESCRIPTION'] : 'LXX', KEYS['FILE'] : 'chronologies/byzantine.txt'},
    'SMITH': {KEYS['DESCRIPTION'] : 'ABR', KEYS['FILE'] : 'chronologies/smith.txt'},
    'PETROVICH' : {KEYS['DESCRIPTION'] : 'ABR', KEYS['FILE'] : 'chronologies/petrovich.txt'},
}


EVENTS = {
    'Creation': {'Area' : AREAS['ISRAEL'], 'Text' : 'Genesis 1'},
    'Flood': {'Area' : AREAS['ISRAEL'], 'Text' : 'Genesis 6-9'},
    'Babel': {'Area' : AREAS['ISRAEL'], 'Text' : 'Genesis 11'},
    'Sojourn': {'Area' : AREAS['ISRAEL'], 'Text' : 'Genesis 49'},
    'Exodus': {'Area' : AREAS['ISRAEL'], 'Text' : 'Exodus'},
}
ACTORS = {}



TEXTS = {}

class Calendar:
    """This class defines the calendar system in which the chronology will be built.
    By default the calendar will be the Gregorian calendar with AD/BC KEYS.
    """

    def __init__(self, calendar: dict = CALENDARS['GREGORIAN']):
        """Parameters to be used for the calendar in which this chronology is constructed

        Parameters
        ----------
        calendar: string (default 'Gregorian')
            The calendar that will be used to display and input dates.  All dates are
            handled through NumPy's datetime64, but the display and put are in the user's
            normal calendar.  The default is the ISO format of the date and time
            with an optional 'AD' or 'BC' label.  There is no `year zero`.

        """
        self.calendar = calendar
        self.calendarname = self.calendar['NAME']
        self.poslabel = self.calendar['POSLABEL']
        self.poslabellen = len(self.poslabel)
        self.neglabel = self.calendar['NEGLABEL']
        self.neglabellen = len(self.neglabel)
        self.zeroyear = self.calendar['ZEROYEAR']
        self.usezero = self.calendar['USEZERO']




    def daysinyear(self, date:str|np.datetime64):
        """A procedure to count number of days in a Gregorian year given the year.
        
        Parameters
        ----------
        date: np.datetime64
            The date to find the number of days in the year
            
        Examples
        --------

        """
        if type(date) == str:
            year = np.datetime64(date,'Y').astype('int') + 1970
        else:
            year = date['Y'].astype('int') + 1970
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 366
        else:
            return 365


    def numericdate(self, date: str, unit: str = DATETIMES['YEAR']):
        """A procedure to convert an ISO string with KEYS to astronomical year numbering.
        This numeric value contains a Year Zero as 0.  Dates labelled as `BC` or `BCE`
        will be converted to a negative value one year larger than the string date with
        the label.
        
        Parameters
        ----------
        date: string
            The date that will be converted to a numeric value.

        Returns
        -------
        np.datetime64
            The numeric value of the date in astronomical time with Year Zero being 0.

        Examples
        --------
        >>> 

        """
        # Look for errors
        if date[0] == '-':
            if date[-self.neglabellen:] == self.neglabel:
                raise ValueError(f'The year is negative but the date contains a negative label "{date[-self.neglabellen:]}"')
            elif date[-self.poslabellen:] == self.poslabel:
                raise ValueError(f'The year is negative but the date contains a positive label "{date[-self.poslabellen:]}"')

        # If no errors, proceed
        if date[-self.neglabellen:] == self.neglabel:
            if self.usezero:
                numericdate = np.datetime64('-'+date[0:-self.neglabellen])
            else:
                days = self.daysinyear(date[0:-self.neglabellen])
                numericdate = np.datetime64('-'+date[0:-self.neglabellen]) + np.timedelta64(days, 'D')
        elif date[-self.poslabellen:] == self.poslabel:
            numericdate = np.datetime64(date[0:-self.poslabellen])
        else:
            numericdate = np.datetime64(date)
        return numericdate

    def stringdate(self, date: np.datetime64, unit: str = DATETIMES['YEAR']):
        """A procedure to convert a numeric date to a date labelled with an epoch label.
        
        Parameters
        ----------
        date: np.datetime64
            The numeric date to be converted to a string

        """
        if date is None:
            return ''
        else:
            return np.datetime_as_string(date, unit='D')

    def load(self, chronologyname: str):
        # for i in CHRONOLOGIES:
        #     if i[0] == chronologyname:
        #         filename = i[2]
        #         break
        chronology = {}
        with open(CHRONOLOGIES[chronologyname][KEYS['FILE']]) as file:
            for i in file:
                line = ast.literal_eval(i.replace('\n',''))
                chronology.update(line)
        return chronology

class Chronology(Calendar):
    """This class constructs the dictionaries used to store a particular chronology.
    It builds actors, events and periods.  It saves the dictionaries.  It provides
    visual adis to viewing the chronology.
    """

    def __init__(self,
                 chronologyname: str = '',
                 description: str = '',
                 calendar: dict = CALENDARS['GREGORIAN']):
        super().__init__(calendar)
        self.chronologyname = chronologyname
        self.description = description
        self.chronology = {
            KEYS['NAME'] : self.chronologyname,
            KEYS['DESCRIPTION'] : self.description,
            KEYS['CALENDAR'] : self.calendar,
            KEYS['EVENTS'] : {},
            KEYS['PERIODS'] : {},
            KEYS['ACTORS'] : {},
        }
        if self.chronologyname not in CHRONOLOGIES.keys():
            CHRONOLOGIES.update({self.chronologyname : {KEYS['DESCRIPTION'] : self.description, KEYS['FILE'] : ''}})

    def __str__(self):
        return str(self.chronology)

    def save(self, filename: str):
        if self.chronologyname != '':
            with open(filename, 'w') as f:
                for key, value in self.chronology.items():
                    f.write('{"%s" : "%s"}\n' % (key, value))
            CHRONOLOGIES[self.chronologyname][KEYS['FILE']] = filename
        else:
            raise ValueError('The chronology name is the empty string.')
        
    # def actors(self) -> pd.DataFrame:
    #     """Display the ACTORS constants."""
    #     return pd.DataFrame.from_dict(ACTORS, orient='index')


    # def areas(self) -> pd.DataFrame:
    #     """Display the AREAS constants."""
    #     return pd.DataFrame.from_dict(AREAS, orient='index', columns=['Value'])


    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(CALENDARS)


    def chronologies(self) -> pd.DataFrame:
        """Display the CHRONOLOGIES constants."""
        return pd.DataFrame.from_dict(CHRONOLOGIES, orient='index')


    def datetimes(self) -> pd.DataFrame:
        """Display the DATETIMES constants."""
        return pd.DataFrame.from_dict(DATETIMES, orient='index', columns=['Value'])


    # def events(self) -> pd.DataFrame:
    #     """Display the EVENTS constants."""
    #     return pd.DataFrame.from_dict(EVENTS, orient='index')


    def keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame.from_dict(KEYS, orient='index', columns=['Value'])


    # def periods(self) -> pd.DataFrame:
    #     """Display the PERIODS constants."""
    #     return pd.DataFrame.from_dict(PERIODS, orient='index')

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology."""
        return pd.DataFrame.from_dict(self.chronology[KEYS['PERIODS']], orient='index')
    
    def add_period(self, name: str, area:str, begin: str, end: str):
        """Add a period to the dictionary."""
        self.chronology[KEYS['PERIODS']].update({name : {
            KEYS['AREA'] : area,
            KEYS['BEGIN'] : begin,
            KEYS['END'] : end,
        }})

    def remove_period(self, name):
        """Remove a period from the dictionary."""
        self.chronology[KEYS['PERIODS']].pop(name)

    
    def actors(self) -> pd.DataFrame:
        """Display the ACTORS constants."""
        return pd.DataFrame.from_dict(self.chronology[KEYS['ACTORS']], orient='index')

    # def areas(self) -> pd.DataFrame:
    #     """Display the AREAS constants."""
    #     return pd.DataFrame.from_dict(self.chronology[KEYS['AREAS']], orient='index', columns=['Value'])

    def events(self) -> pd.DataFrame:
        """Display the EVENTS constants."""
        return pd.DataFrame.from_dict(self.chronology[KEYS['EVENTS']], orient='index')
    
    def add_event(self, event: str, date: str, text: str = ''):
        """Add an event in a chronology and to its event ordering.
        
        Parameters
        ----------
        event: string
            The name of the event to add
        date: string
            The date of the event to add.
            The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
            Otional ' AD', ' BC', ' CE', ' BCE' KEYS may be added.
            The years may be negative if the KEYS are not used.
            The years may be arbitrarily large outside of the range of the current julian period.
        text: string (Optional)
            Reference to the text justifying this event and date

        Returns
        -------
        string
            A message stating that the event at a certain date with a reference text
            was added to the chronology.

        Examples
        --------

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            numericdate = super().numeric(date)
            numericdatetype = type(numericdate)
            self.chronology[event] = [date, super().numeric(date), text]
            self.eventorder.append(event)
            return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.chronologyname}" chronology.')

    def update_event(self, event: str, date: str, text: str = ''):
        """Update an event in a chronology.
        
        Parameters
        ----------
        event: string
            The name of the event to update
        date: string
            The date of the event to update.
            The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
            Otional ' AD', ' BC', ' CE', ' BCE' KEYS may be added.
            The years may be negative if the KEYS are not used.
            The years may be arbitrarily large outside of the range of the current julian period.
        text: string
            Reference to the text justifying this event and date

        Returns
        -------
        string
            A message stating that the event at a certain date with a reference text
            was updated in the chronology

        Examples
        --------

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.chronology.update({event : [date, super().numeric(date), text]})
            return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.chronologyname}" chronology.')

    def remove_event(self, event: str):
        """Remove an event from a chronology and its event ordering.
        
        Parameters
        ----------
        event: string
            The name of the event to remove

        Returns
        -------
        string
            A message stating that the event has been removed from the chronology.

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.chronology.pop(event)
            self.eventorder.remove(event)
            return(f'Event "{event}" has been removed from the "{self.chronologyname}" chronology.')

    def show_event(self, vertical: bool = False):
        """Display the chronology as a table.  The default display will show
        the metadata associated with the chronology.  The vertical display
        will only show the events in their current event ordering.
        
        Parameters
        ----------
        vertical: boolean
            Display the events vertically rather than horizontally

        Examples
        --------

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            return pd.DataFrame(self.chronology)

    def show_eventorder(self):
        """Display a list of events in the order they will be shown.
        
        Returns
        -------
        list
            A list of events in the order they will appear
            
        Examples
        --------

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            return self.eventorder

    def update_eventorder(self, events: list):
        """Update the event ordering of a chronology.
        
        Parameters
        ----------
        events: list
            A list of events in the chronology is the order they should appear.
            
        Returns
        -------
        string
            A message stating that the event order has been updated.

        Examples
        --------

        """
        if self.chronologyname == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.eventorder = events
            return f'The event ordering of the "{self.chronologyname}" has been updated.'
