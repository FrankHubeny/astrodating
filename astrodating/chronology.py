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
    'LEFTBRACE' : '{',
    'NEGATIVE' : '-',
    'NEWLINE' : '\n',
    'SPACE' : ' ',
}


KEYS = {
    'ACTORS' : 'ACTORS',
    'BEFOREPRESENT' : 'Before Present',
    'BEGIN' : 'BEGIN',
    'CALENDAR' : 'CALENDAR',
    'CHALLENGES' : 'CHALLENGES',
    'END' : 'END',
    'EVENTS' : 'EVENTS',
    'EXPERIMENT' : 'Experiment',
    'FEMALE' : 'FEMALE',
    'FILE' : 'FILENAME',
    'GREGORIAN' : 'Gregorian',
    'MALE' : 'MALE',
    'MARKERS' : 'MARKERS',
    'NAME' : 'NAME',
    'NEGLABEL' : 'NEG LABEL',
    'PERIODS' : 'PERIODS',
    'POSLABEL' : 'POS LABEL',
    'SECULAR' : 'Secular',
    'TEXTS' : 'TEXTS',
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
                 calendar: str = 'Gregorian'):
        if chronologyname == '' and filename == '':
            raise ValueError('The chronology has neither a name nor a file to load.')
        if chronologyname != '' and filename != '':
            raise ValueError(f'Both a chronology name "{chronologyname}" and a filename "{filename}" have been specified, but only one can be used.')
        self.commentlist = []
        self.filename = filename
        self.maindictionaries = [
            KEYS['ACTORS'], 
            KEYS['CHALLENGES'], 
            KEYS['EVENTS'], 
            KEYS['MARKERS'],
            KEYS['PERIODS'], 
            KEYS['TEXTS'], 
        ]
        if chronologyname != '':
            self.chronology = {
                KEYS['NAME'] : chronologyname,
                KEYS['ACTORS'] : {},
                KEYS['CALENDAR'] : {},
                KEYS['CHALLENGES'] : {},
                KEYS['EVENTS'] : {},
                KEYS['MARKERS'] : {},
                KEYS['PERIODS'] : {},
                KEYS['TEXTS'] : {},
            }
            
            self.chronology[KEYS['CALENDAR']].update(CALENDARS[calendar])
            self.name = self.chronology[KEYS['NAME']]
            self.calendar = self.chronology[KEYS['CALENDAR']][KEYS['NAME']]
            self.poslabel = CALENDARS[self.calendar][KEYS['POSLABEL']]
            self.poslabellen = len(CALENDARS[self.calendar][KEYS['POSLABEL']])
            self.neglabel = CALENDARS[self.calendar][KEYS['NEGLABEL']]
            self.neglabellen = len(CALENDARS[self.calendar][KEYS['NEGLABEL']])
        else:
            self.chronology = {}
            with open(filename) as file:
                for line in file:
                    if line[0] == CONSTANTS['LEFTBRACE']:
                        self.chronology.update(ast.literal_eval(line))
                    else:  
                        self.commentlist.append(line.replace(CONSTANTS['NEWLINE'], ''))
                        

    def __str__(self):
        return str(self.chronology)
    
    def show(self):
        """Show the entire chronology."""
        self.comments()
        self.dictionaries()
    
    def rename(self, newname: str):
        """Rename the chronology."""
        self.chronology.update({KEYS['NAME'] : newname})
        self.name = self.chronology[KEYS['NAME']]



            






    ###### ACTORS 

    def actors(self) -> pd.DataFrame:
        """Display the actors in a chronology."""
        if len(self.chronology[KEYS['ACTORS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['ACTORS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no actors.')

    def actors_pop(self, pops: list):
        """Display the actors defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the actors.
            
        """
        self.dictionary_pop(self, pops, KEYS['ACTORS'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['ACTORS']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')

    def add_actor(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add an actor to the dictionary."""
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

    def remove_actor(self, name):
        """Remove an actor from the dictionary."""
        self.chronology[KEYS['ACTORS']].pop(name)


    ###### CALENDARS 

    def datetimes(self) -> pd.DataFrame:
        """Display the DATETIMES constants."""
        return pd.DataFrame.from_dict(DATETIMES, orient='index', columns=['Value'])
    
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

    def calendars(self) -> pd.DataFrame:
        """Display the CALENDARS constants."""
        return pd.DataFrame.from_dict(CALENDARS)
    
    def add_calendar(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a calendar to the dictionary."""
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

    def to(self, calendar: str):
        """Convert the calendar of the chronology to anther calendar.
        
        Parameter
        ---------
        calendar: str
            The key of the calendar to convert the current calendar to.
        """
        labelcalendars = [KEYS['GREGORIAN'], KEYS['SECULAR']]
        formercalendar = CALENDARS[self.calendar]
        poslabel = formercalendar[KEYS['POSLABEL']]
        poslabellen = -len(poslabel)
        newcalendar = CALENDARS[calendar]
        if CALENDARS[calendar][KEYS['NAME']] == self.calendar:
            print(f'The chronology already has the "{self.calendar}" calendar.')
        else:
            if calendar in labelcalendars and self.calendar in labelcalendars:
                self.chronology[KEYS['CALENDAR']].update(newcalendar)
                for i in self.chronology[KEYS['PERIODS']]:
                    for k in [KEYS['BEGIN'], KEYS['END']]:
                        if self.chronology[KEYS['PERIODS']][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[KEYS['PERIODS']][i][k].replace(
                                formercalendar[KEYS['POSLABEL']], 
                                newcalendar[KEYS['POSLABEL']]
                            )
                        else:
                            newvalue = self.chronology[KEYS['PERIODS']][i][k].replace(
                                formercalendar[KEYS['NEGLABEL']], 
                                newcalendar[KEYS['NEGLABEL']]
                            )
                        self.chronology[KEYS['PERIODS']][i].update({k : newvalue})
                for i in self.chronology[KEYS['EVENTS']]:
                    for k in [KEYS['DATE']]:
                        if self.chronology[KEYS['EVENTS']][i][k][poslabellen:] == poslabel:
                            newvalue = self.chronology[KEYS['EVENTS']][i][k].replace(
                                formercalendar[KEYS['POSLABEL']], 
                                newcalendar[KEYS['POSLABEL']]
                            )
                        else:
                            newvalue = self.chronology[KEYS['EVENTS']][i][k].replace(
                                formercalendar[KEYS['NEGLABEL']], 
                                newcalendar[KEYS['NEGLABEL']]
                            )
                        self.chronology[KEYS['EVENTS']][i].update({k : newvalue})
            self.calendar = self.chronology[KEYS['CALENDAR']][KEYS['NAME']]
            self.poslabel = CALENDARS[self.calendar][KEYS['POSLABEL']]
            self.poslabellen = len(CALENDARS[self.calendar][KEYS['POSLABEL']])
            self.neglabel = CALENDARS[self.calendar][KEYS['NEGLABEL']]
            self.neglabellen = len(CALENDARS[self.calendar][KEYS['NEGLABEL']])
            print(f'The chronology has been changed to the "{self.calendar}" calendar.')

    ###### CHALLENGES 

    def challenges(self) -> pd.DataFrame:
        """Display the challenges in a chronology."""
        if len(self.chronology[KEYS['CHALLENGES']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['CHALLENGES']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no challenges.')

    def challenges_pop(self, pops: list) -> pd.DataFrame:
        """Display the challenges defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        self.dictionary_pop(self, pops, KEYS['CHALLENGES'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['CHALLENGES']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')

    def add_challenge(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a challenge to the dictionary."""
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

    def remove_challenge(self, name):
        """Remove a challenge from the dictionary."""
        self.chronology[KEYS['CHALLENGES']].pop(name)


    ###### COMMENTS 

    def add_comment(self, text: str = ''):
        """Add a comment to a chronology.
        
        To create a comment with more than one line use `\n` to separate the lines.

        Parameter
        ---------
        text: str (Default '', Optional)


        See Also
        --------
        `comments`
            Display all comments in the chronology.
        `remove_comment`
            Remove a line from the comment list.
        `remove_all_comments`
            Remove all comments from the chronology.

        Notes
        -----
        Once one saves the file, one may add comments using an editor.
        It may be helpful to use this method for each sentence rather
        than using the `\n`.  

        To add a blank line enter one or more spaces as the `text` of this method
        or accept the default which is an empty string.

        All comments are placed at the top of the file when it is written.
        The dictionaries representing the chronology follow the comments.
        
        Parameters
        ----------
        text: str
            A comment one or more lines long. Each line ended with `\n`.
        """
        
        if text == '':
            self.commentlist.append(CONSTANTS['SPACE'])
        else:
            texts = text.split(CONSTANTS['NEWLINE'])
            for i in texts:
                self.commentlist.append(i.replace(CONSTANTS['NEWLINE'], ''))

        
    def comments(self):
        """Display a numbered list of comments."""
        for i in range(0, len(self.commentlist)):
            print('{:>3} : {}'.format(str(i),self.commentlist[i]))

    def remove_comment(self, index: int):
        """Remove a comment from the chronology by specifying its number in the comments list."""
        if index >= len(self.commentlist):
            print(f'There are only {len(self.commentlist)} comments in the list. The index starts at 0.')
        else:
            self.commentlist.pop(index)

    def remove_all_comments(self):
        """Remove all comments from the chronology."""
        self.commentlist = []

    ###### DICTIONARIES

    def keys(self) -> pd.DataFrame:
        """Display the KEYS constants."""
        return pd.DataFrame.from_dict(KEYS, orient='index', columns=['Value'])
    
    def dictionaries(self):
        for key in self.chronology.keys():
            if isinstance(self.chronology[key], dict):
                if len(self.chronology[key]) > 0:
                    print('{} : {}'.format(key, '{'))
                    for subkey in self.chronology[key]:
                        print('    {} : {}'.format(subkey, self.chronology[key][subkey]))
                    print('}')
                else:
                    print('{} : {}'.format(key, self.chronology[key]))
            else:
                print('{} : {}'.format(key, self.chronology[key]))

    def dictionary_pop(self, pops: list, dictname: str):
        """Display the dictionary except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the dictionary.
        dictname: str
            The name of the dictionary to display.
            
        """
        dictionary = copy.deepcopy(dict(self.chronology[dictname]))
        for i in pops:
            for j in dictionary:
                try:
                    dictionary[j].pop(i)
                except KeyError:
                    break
        return pd.DataFrame.from_dict(dictionary, orient='index')
    
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


    ###### EVENTS 

    def events(self) -> pd.DataFrame:
        """Display the EVENTS constants."""
        if len(self.chronology[KEYS['EVENTS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['EVENTS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no events.')


    def events_pop(self, pops: list) -> pd.DataFrame:
        """Display the events defined for the chronology without some of the keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the events.
            
        """
        self.dictionary_pop(self, pops, KEYS['EVENTS'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['EVENTS']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')
    
    
    # def add_event(self, event: str, date: str, text: str = ''):
    #     """Add an event in a chronology and to its event ordering.
        
    #     Parameters
    #     ----------
    #     event: string
    #         The name of the event to add
    #     date: string
    #         The date of the event to add.
    #         The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
    #         Otional ' AD', ' BC', ' CE', ' BCE' KEYS may be added.
    #         The years may be negative if the KEYS are not used.
    #         The years may be arbitrarily large outside of the range of the current julian period.
    #     text: string (Optional)
    #         Reference to the text justifying this event and date

    #     Returns
    #     -------
    #     string
    #         A message stating that the event at a certain date with a reference text
    #         was added to the chronology.

    #     Examples
    #     --------

    #     """
    #     pass
        # if self.name == '':
        #     raise ValueError('The chronology name is empty.')
        # else:
        #     numericdate = super().numeric(date)
        #     numericdatetype = type(numericdate)
        #     self.chronology[event] = [date, super().numeric(date), text]
        #     self.eventorder.append(event)
        #     return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.name}" chronology.')
    
    def add_event(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add an event to the dictionary."""
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

    def remove_event(self, name):
        """Remove an event from the dictionary."""
        self.chronology[KEYS['EVENTS']].pop(name)


    # def update_event(self, event: str, date: str, text: str = ''):
    #     """Update an event in a chronology.
        
    #     Parameters
    #     ----------
    #     event: string
    #         The name of the event to update
    #     date: string
    #         The date of the event to update.
    #         The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
    #         Otional ' AD', ' BC', ' CE', ' BCE' KEYS may be added.
    #         The years may be negative if the KEYS are not used.
    #         The years may be arbitrarily large outside of the range of the current julian period.
    #     text: string
    #         Reference to the text justifying this event and date

    #     Returns
    #     -------
    #     string
    #         A message stating that the event at a certain date with a reference text
    #         was updated in the chronology

    #     Examples
    #     --------

    #     """
    #     if self.name == '':
    #         raise ValueError('The chronology name is empty.')
    #     else:
    #         self.chronology.update({event : [date, super().numeric(date), text]})
    #         return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.name}" chronology.')

    # def remove_event(self, event: str):
    #     """Remove an event from a chronology and its event ordering.
        
    #     Parameters
    #     ----------
    #     event: string
    #         The name of the event to remove

    #     Returns
    #     -------
    #     string
    #         A message stating that the event has been removed from the chronology.

    #     """
    #     if self.name == '':
    #         raise ValueError('The chronology name is empty.')
    #     else:
    #         self.chronology.pop(event)
    #         self.eventorder.remove(event)
    #         print(f'Event "{event}" has been removed from the "{self.name}" chronology.')


    # def show_eventorder(self):
    #     """Display a list of events in the order they will be shown.
        
    #     Returns
    #     -------
    #     list
    #         A list of events in the order they will appear
            
    #     Examples
    #     --------

    #     """
    #     if self.chronology[KEYS['NAME']] == '':
    #         raise ValueError('The chronology name is empty.')
    #     else:
    #         return self.eventorder

    # def update_eventorder(self, events: list):
    #     """Update the event ordering of a chronology.
        
    #     Parameters
    #     ----------
    #     events: list
    #         A list of events in the chronology is the order they should appear.
            
    #     Returns
    #     -------
    #     string
    #         A message stating that the event order has been updated.

    #     Examples
    #     --------

    #     """
    #     if self.chronology[KEYS['NAME']] == '':
    #         raise ValueError('The chronology name is empty.')
    #     else:
    #         self.eventorder = events
    #         return f'The event ordering of the "{self.name}" has been updated.'
        
    ###### MARKERS 

    def markers(self) -> pd.DataFrame:
        """Display the markers in a chronology."""
        if len(self.chronology[KEYS['MARKERS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['MARKERS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no markers.')

    def markers_pop(self, pops: list) -> pd.DataFrame:
        """Display the markers defined for the chronology if there are any.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the markers.
            
        """
        self.dictionary_pop(self, pops, KEYS['MARKERS'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['MARKERS']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')

    ###### PERIODS 

    def periods(self) -> pd.DataFrame:
        """Display the periods defined for the chronology if there are any."""
        if self.chronology[KEYS['PERIODS']] is not None:
            return pd.DataFrame.from_dict(self.chronology[KEYS['PERIODS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no periods.')

    def periods_pop(self, pops: list) -> pd.DataFrame:
        """Display the periods defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the periods.
            
        """
        self.dictionary_pop(self, pops, KEYS['PERIODS'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['PERIODS']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')

    
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

    ###### SAVE 

    def save(self, filename: str = ''):
        if filename == '':
            if self.filename == '':
                raise ValueError(f'No file name has been provided.')
            else:
                file = self.filename
        else:
            file=filename
        with open(file, 'w') as f:
            for i in self.commentlist:
                f.write('%s\n' % i)
            for key, value in self.chronology.items():
                if isinstance(value, dict):
                    f.write("{'%s' : %s}\n" % (key, value))
                else:
                    f.write("{'%s' : '%s'}\n" % (key, value))

    def save_as_json(self):
        pass

    def save_as_html(self):
        pass

    def save_as_pdf(self):
        pass

    
    ###### TEXTS 

    def texts(self) -> pd.DataFrame:
        """Display the texts referenced to justify a chronology."""
        if len(self.chronology[KEYS['TEXTS']]) > 0:
            return pd.DataFrame.from_dict(self.chronology[KEYS['TEXTS']], orient='index')
        else:
            print(f'The chronology "{self.name}" has no texts referenced to justify the chronology.')

    def texts_pop(self, pops: list) -> pd.DataFrame:
        """Display the texts defined for the chronology except for specified keys.
        
        Parameter
        ---------
        pops: list
            A list of keys to be temporarily removed before displaying the texts.
            
        """
        self.dictionary_pop(self, pops, KEYS['TEXTS'])
        # dictionary = copy.deepcopy(dict(self.chronology[KEYS['TEXTS']]))
        # for i in pops:
        #     for j in dictionary:
        #         try:
        #             dictionary[j].pop(i)
        #         except KeyError:
        #             break
        # return pd.DataFrame.from_dict(dictionary, orient='index')

    def add_text(self, name: str, begin: str, end: str, keyvalues: dict = {}):
        """Add a text to the dictionary."""
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

    def remove_text(self, name):
        """Remove a text from the dictionary."""
        self.chronology[KEYS['TEXTS']].pop(name)


    def combine(self, chronologyname: str, chronology: dict, comments: list = [], keepcomments: bool = True):
        """Return a new chronology containing a combination of the current one and another chronology.

        The two source chronologies are not changed.  A new chronology containing both 
        of them is returned.  The two chronologies must have the same calendar. Use
        the `to` method to convert one of the chronologies to the other if their
        calendars do not agree.

        See Also
        --------
        to
        
        Parameters
        ----------
        chronologyname: str
            The name of the new chronology
        chronology: dict
            The chronology to combine with the present one.
        comments: list (optional)
            The comments from the combined chronology.
        keepcomments: bool (default True)
            Add the comments from the self chronology into the new chronology.
        """

        newchron = Chronology(chronologyname=chronologyname, cal=self.calendar)
        if self.calendar == chronology[KEYS['CALENDAR']]:
            if keepcomments:
                newchron.comments.extend(self.comments)
            newchron.comments.extend(comments)
            for key in self.maindictionaries:
                newchron.chronology[key].update(self.chronology[key])
                newchron.chronology[key].update(chronology[key])
            return newchron
        else:
            raise ValueError(f'The calendars "{self.calendar}" and "{chronology[KEYS['CALENDAR']]}" do not match.')
            
