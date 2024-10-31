# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides procedures to create generic chronologies.
It also provides examples of chronologies of actual chronologies
from historical events around the world to processes either
hypothesized or observed in laboratory conditions.

The module also provides means of testing conflicting chronologies
using constraints that could lead one to falsify the
chronology unless the constraints are answered.
"""

import numpy as np
import pandas as pd
import ast
import copy


__all__ = [
    'Chronology',
    'Compare',
]

CONSTANTS = {
    'DATETIME_EPOCH': 1970,
    'COMMENT' : '#',
    'NEGATIVE' : '-',
}


KEYS = {
    'ACTORS' : 'ACTORS',
    'BEGIN' : 'BEGIN',
    'CALENDAR' : 'CALENDAR',
    'CHALLENGES' : 'CHALLENGES',
    'END' : 'END',
    'EVENTS' : 'EVENTS',
    'FEMALE' : 'FEMALE',
    'FILE' : 'FILENAME',
    'GREGORIAN' : 'Gregorian',
    'MALE' : 'MALE',
    'MARKERS' : 'MARKERS',
    'NAME' : 'NAME',
    'NEGLABEL' : 'NEG LABEL',
    'PERIODS' : 'PERIODS',
    'POSLABEL' : 'POS LABEL',
    'TEXTS' : 'TEXT',
    'USEZERO' : 'USE ZERO',
    'ZEROYEAR' : 'ZERO YEAR',
}

CALENDARS = {
    'Before Present' : {
        'NAME' : 'Before Present',
        'POS LABEL' : '',
        'NEG LABEL' : ' BP',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Experiment' : {
        'NAME' : 'Experiment',
        'POS LABEL' : '',
        'NEG LABEL' : '',
        'Zero Year' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Gregorian' : {
        'NAME' : 'Gregorian',
        'POS LABEL' : ' AD',
        'NEG LABEL' : ' BC',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
    'Secular' : {
        'NAME' : 'Secular',
        'POS LABEL' : ' CE',
        'NEG LABEL' : ' BCE',
        'ZERO YEAR' : -CONSTANTS['DATETIME_EPOCH'],
        'USE ZERO' : False,
    },
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


class Compare():
    """Compare two or more chronologies for the same events.

    Routines
    --------

    See Also
    --------
    `Chronology`: The compared chronologies being were created or read
        from files using this class.  

    References
    ----------

    Examples
    --------
    The following example compares James Ussher's history of the world
    with a modern version of the older Byzantine church chronology.
    The challenges by each of these chronologies are used
    """

    def __init__(self, chronologies: list):
        self.chronologies = chronologies

    

class Chronology():
    """Construct a dictionary to represent a chronology.

    The tools provide for storing dates associated with periods and events.
    - One can name an actor with an event.  
    - One can add a defense for each date to answer a challenge.  
    - One can add a challenge to argue against a competing chronology.
    - One can save the chronology to a human readable file.
    - The file may be modified with a text editor.
    - One can retrieve the dictionary from a file to continue building it.

    Routines
    --------

    See Also
    --------
    `Compare`: After two competing Chronologies have been constructed
        with defenses and challenges they may be compared with the
        visualization tools in this class.

    References
    ----------
    - Introduction to Calendars: https://aa.usno.navy.mil/faq/calendars Accessed on Oct 30, 2024

    Examples
    --------
    The first two examples show two competing chronologies for biblical history.

    The following would construct a brief chronology based on James Ussher's history.
    It also provides a defense against and a challenge for the older Byzantine chronology.

    The following constructs a brief chronology based on the Byzantine chronology.
    It contains a defense against and a challenge for the Ussher's history.

    The next two examples show to competing chronologies based on periods
    for the Ancient Near East.

    The following would construct a brief chronology as the basis of a genealogy.


    The following would construct a brief chronology of the decay of uranian-238.

    The following chronology provides a brief history of China using the
    Chinese calendar.

    The following example converts the above chronology of China to a
    Gregorian calendar.

    The following chronology provides a brief history of Islam using the
    Islamic calendar.

    The following example converts the above chronology of Islam to a
    secular calendar using 'CE' rather than 'AD' labels.




    """

    def __init__(self,
                 chronologyname: str = '',
                 filename: str = '',
                 cal: str = 'Gregorian'):
        if chronologyname == '' and filename == '':
            raise ValueError('The chronology has neither a name nor a file to load.')
        if chronologyname != '' and filename != '':
            raise ValueError(f'Both a chronology name "{chronologyname}" and a filename "{filename}" have been specified, but only one can be used.')
        self.comments = []
        self.filename = filename
        self.name = chronologyname
        self.calendar = cal
        self.dictionaries = [
            KEYS['EVENTS'], 
            KEYS['PERIODS'], 
            KEYS['ACTORS'], 
            KEYS['TEXTS'], 
            KEYS['CHALLENGES'], 
            KEYS['MARKERS']
        ]
        if chronologyname != '':
            self.chronology = {
                KEYS['NAME'] : chronologyname,
                KEYS['CALENDAR'] : cal,
                KEYS['POSLABEL'] : CALENDARS[cal][KEYS['POSLABEL']],
                KEYS['NEGLABEL'] : CALENDARS[cal][KEYS['NEGLABEL']],
                KEYS['ZEROYEAR'] : CALENDARS[cal][KEYS['ZEROYEAR']],
                KEYS['USEZERO'] : CALENDARS[cal][KEYS['USEZERO']],
                KEYS['EVENTS'] : {},
                KEYS['PERIODS'] : {},
                KEYS['ACTORS'] : {},
                KEYS['TEXTS'] : {},
                KEYS['CHALLENGES'] : {},
                KEYS['MARKERS'] : {},
            }
            self.poslabel = CALENDARS[cal][KEYS['POSLABEL']]
            self.poslabellen = len(self.poslabel)
            self.neglabel = CALENDARS[cal][KEYS['NEGLABEL']]
            self.neglabellen = len(self.neglabel)
        else:
            self.chronology = {}
            with open(filename) as file:
                for line in file:
                    if line[0] == CONSTANTS['COMMENT']:
                        self.comments.append(line)
                    else:  
                        self.chronology.update(ast.literal_eval(line))
                

    def __str__(self):
        return str(self.chronology)
    
    # def load(self, chronologyname: str):
    #     chronology = {}
    #     with open(CHRONOLOGIES[chronologyname][KEYS['FILE']]) as file:
    #         for i in file:
    #             line = ast.literal_eval(i.replace('\n','').replace('"{','{').replace('}"','}'))
    #             if line[0] == CONSTANTS['COMMENT']:
    #                 self.comments.append(line)
    #             else:
    #                 chronology.update(line)
    #         chronology.update({KEYS['PERIODS'] : ast.literal_eval(chronology[KEYS['PERIODS']])})
    #     return chronology

    def save(self, filename: str = ''):
        if filename == '':
            if self.filename == '':
                raise ValueError(f'No file name has been provided.')
            else:
                file = self.filename
        else:
            file=filename
        with open(file, 'w') as f:
            for i in self.comments:
                f.write('%s\n' % i)
            for key, value in self.chronology.items():
                if isinstance(value, dict):
                    f.write("{'%s' : %s}\n" % (key, value))
                else:
                    f.write("{'%s' : '%s'}\n" % (key, value))

        
    def comment(self, line: str):
        self.comments.append(''.join([CONSTANTS['COMMENT'], ' ', line]))
        
    def show_comments(self):
        for i in self.comments:
            print(i[2:])

    def daysinyear(self, date:str|np.datetime64):
        """A procedure to count number of days in a Gregorian year given the year.
        
        Parameters
        ----------
        date: np.datetime64
            The date to find the number of days in the year
            
        Examples
        --------

        """
        if isinstance(date, str):
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
        if date[0] == CONSTANTS['NEGATIVE']:
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
            
    

    # def name(self):
    #     """Display the name of the chronology.
        
    #     Returns
    #     -------
    #     string
    #         The name of the chrono0logy.
    #     """
    #     return str(self.chronology[KEYS['NAME']])
    
    
    # def calendar(self):
    #     """Display the name of the calendar used in the chronology."""
    #     return self.chronology[KEYS['CALENDAR']]


    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(CALENDARS)


    def datetimes(self) -> pd.DataFrame:
        """Display the DATETIMES constants."""
        return pd.DataFrame.from_dict(DATETIMES, orient='index', columns=['Value'])


    def keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame.from_dict(KEYS, orient='index', columns=['Value'])


    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any."""
        if self.chronology[KEYS['PERIODS']] is not None:
            return pd.DataFrame.from_dict(self.chronology[KEYS['PERIODS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no periods.')

    def periods_pop(self, pops: list) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        dictionary = copy.deepcopy(dict(self.chronology[KEYS['PERIODS']]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient='index')

    
    def add_period(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a period to the dictionary."""
        for i in keyvalues.keys():
            if i in KEYS.keys():
                raise ValueError(f'The key "{i}" is a reserved key.')
        else:
            self.chronology[KEYS['PERIODS']].update({name : {
                KEYS['BEGIN'] : begin,
                KEYS['END'] : end,
            }})
            if len(keyvalues) > 0:
                self.chronology[KEYS['PERIODS']][name].update(keyvalues)

    def remove_period(self, name):
        """Remove a period from the dictionary."""
        self.chronology[KEYS['PERIODS']].pop(name)

    
    def actors(self) -> pd.DataFrame:
        """Display the ACTORS constants."""
        if len(self.chronology[KEYS['ACTORS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['ACTORS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no actors.')


    def events(self) -> pd.DataFrame:
        """Display the EVENTS constants."""
        if len(self.chronology[KEYS['EVENTS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['EVENTS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no events.')
    
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
        if self.name == '':
            raise ValueError('The chronology name is empty.')
        else:
            numericdate = super().numeric(date)
            numericdatetype = type(numericdate)
            self.chronology[event] = [date, super().numeric(date), text]
            self.eventorder.append(event)
            return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.name}" chronology.')

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
        if self.name == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.chronology.update({event : [date, super().numeric(date), text]})
            return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.name}" chronology.')

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
        if self.name == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.chronology.pop(event)
            self.eventorder.remove(event)
            print(f'Event "{event}" has been removed from the "{self.name}" chronology.')


    def show_eventorder(self):
        """Display a list of events in the order they will be shown.
        
        Returns
        -------
        list
            A list of events in the order they will appear
            
        Examples
        --------

        """
        if self.chronology[KEYS['NAME']] == '':
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
        if self.chronology[KEYS['NAME']] == '':
            raise ValueError('The chronology name is empty.')
        else:
            self.eventorder = events
            return f'The event ordering of the "{self.name}" has been updated.'
        
    def show(self):
        """Show the entire chronology."""
        pass
    
    def remove_key(self, dictname: str, key: str):
        """Revove a key from a dictionary of the chronology.  
        
        Reserved keys cannot be removed, but they can be hiddened when displaying
        the dictionary or entire chronology.

        Parameters
        ----------
        dictname: str
            The name of the dictionary within the chronology where the key will be removed
        key: str
            The name of the key to be removed from the dictionary
        
        """
        if key in KEYS.keys():
            raise ValueError(f'The key "{key}" is a reserved key and cannot be removed.')
        elif key not in self.chronology[dictname].keys():
            raise ValueError(f'The key "{key}" is not in the chronology dictionary "{dictname}".')
        else:
            self.chronology[dictname].pop(key)


    def to(self, calendar: str):
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        pass

    def combine(self, chronologyname: str, chronology: dict, comments: list):
        """Combine the current chronology with another one.
        
        Parameters
        ----------
        chronology: dict
            The chronology to combine with the present one.
        """

        newchron = Chronology(chronologyname=chronologyname, cal=self.calendar)
        if self.calendar == chronology[KEYS['CALENDAR']]:
            newchron.comments.extend(self.comments)
            newchron.comments.extend(comments)
            for key in self.dictionaries:
                newchron.chronology[key].update(self.chronology[key])
                newchron.chronology[key].update(chronology[key])
            return newchron
        else:
            raise ValueError(f'The calendars dont match')
            
        
        # firstcalendar = chronologies[0][KEYS['CALENDAR'][KEYS['NAME']]]
        # for i in chronologies:
        #     if i[KEYS['CALENDAR']][KEYS['NAME']] != firstcalendar:
        #          raise ValueError(f'More than one calendar are in use: "{firstcalendar}" and "{i[KEYS['CALENDAR']][KEYS['NAME']]}"')
        # combined = Chronology(chronologyname)
        # for i in chronologies:
        #     combined.chronology.update(i)
        # combined.save(filename)