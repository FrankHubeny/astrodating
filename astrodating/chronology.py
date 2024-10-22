# Licensed under a 3-clause BSD style license - see LICENSE.md
"""
This module provides procedures to create chronologies.
"""

import pandas as pd
import numpy as np

__all__ = [
    'Calendar',
    'Chronology'
]

class Calendar():
    """This class defines the calendar system in which the chronology will be built.
    By default the calendar will be the Gregorian calendar with AD/BC labels.
    """

    def __init__(self, 
                 calendarname: str = 'Gregorian', 
                 poslabel: str = ' AD', 
                 neglabel: str = ' BC', 
                 zeroyear: float = 0.0, 
                 usezero: bool = False):
        """Parameters to be used for the calendar in which this chronology is constructed

        Parameters
        ----------
        calendarname: string (default 'Gregorian')
            The name of the calendar
        neglabel: string (default 'AD')
            The epoch label to add to negative values
        poslabel: string (default 'BC')
            The epoch label to add to positive values
        zeroyear: float (default 0.0)
            The beginning of the epoch
        usezero: boolean (default False)
            True: start the epoch with the zeroyear 
            Talse: start the epoch with 1
        """
        self.calendarname = calendarname
        self.poslabel = poslabel
        self.poslabellen = len(poslabel)
        self.neglabel = neglabel
        self.neglabellen = len(neglabel)
        self.zeroyear = zeroyear
        self.usezero = usezero

    def numericdate(self, date: str):
        """A procedure to convert an ISO string with labels to astronomical year numbering.
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
                    numericdate = np.datetime64('-'+date[0:-self.neglabellen]) + np.timedelta64(365, 'D')
            elif date[-self.poslabellen:] == self.poslabel:
                numericdate = np.datetime64(date[0:-self.poslabellen]))
            else:
                numericdate = np.datetime64(date)
        return numericdate

    def stringdate(self, date: np.datetime64):
        """A procedure to convert a numeric date to a date labelled with an epoch label
        
        Parameters
        ----------
        date: np.datetime64
            The numeric date to be converted to a string
        """
        pass

class Chronology(Calendar):
    """
    This is a data structure that is used to store a list of events, 
    dates when they occurred and references to texts justifying
    those dates.  
    """

    def __init__(self, 
                 chronologyname: str, 
                 displayname: str = '', 
                 source: str = '',
                 calendarname: str = 'Gregorian', 
                 poslabel: str = ' AD', 
                 neglabel: str = ' BC', 
                 zeroyear: float = 0.0, 
                 usezero: bool = False):
        super().__init__(calendarname, poslabel, neglabel, zeroyear, usezero)
        self.chronologyname = chronologyname
        if displayname == '':
            self.displayname = self.chronologyname
        else:
            self.displayname = displayname
        self.source = source
        self.eventorder = []
        self.chronology = {'meta': [self.chronologyname, self.displayname, self.source]}
        self.metakey = 'meta'
        self.dateindex = 0
        self.textindex = 1
        self.numericindex = 2

    def __str__(self):
        eventlist = []
        for key in self.chronology:
            if key != self.metakey:
                eventlist.append([
                    key, 
                    self.chronology[key][self.dateindex], 
                    self.chronology[key][self.numericindex], 
                    self.chronology[key][self.textindex]
                ])
        return eventlist

    def add(self, event: str, date: str, text: str = ''):
        """Add an event in a chronology and to its event ordering.
        
        Parameters
        ----------
        event: string
            The name of the event to add
        date: string
            The date of the event to add.
            The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
            Otional ' AD', ' BC', ' CE', ' BCE' labels may be added.
            The years may be negative if the labels are not used.
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
        
        self.chronology[event] = [date, super().numeric(date), text]
        self.eventorder.append(event)
        return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.chronologyname}" chronology.')
    
    def update(self, event: str, date: str, text: str = ''):
        """Update an event in a chronology.
        
        Parameters
        ----------
        event: string
            The name of the event to update
        date: string
            The date of the event to update.
            The date is in ISO format `YYYY-MM-DDTHH:MM:SS.SSS` with only the year required.
            Otional ' AD', ' BC', ' CE', ' BCE' labels may be added.
            The years may be negative if the labels are not used.
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
        self.chronology.update({event : [date, super().numeric(date), text]})
        return(f'Event "{event}" with date "{date}" and text "{text}" has been added to the "{self.chronologyname}" chronology.')

    def remove(self, event: str):
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
        self.chronology.pop(event)
        self.eventorder.remove(event)
        return(f'Event "{event}" has been removed from the "{self.chronologyname}" chronology.')
    
    def show(self, vertical: bool = False):
        """Display the chronology as a table.  The default display will show
        the metadata associated with the chronology.  The vertical display
        will only show the events in their current event ordering.
        
        Parameters:
        vertical: boolean
            Display the events vertically rather than horizontally

        Examples
        --------
        """
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
        self.eventorder = events
        return f'The event ordering of the "{self.chronologyname}" has been updated.'
    


        
