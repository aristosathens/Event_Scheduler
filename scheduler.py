'''
    Aristos Athens

    Google calendar scheduler design.

    Input:
        User schedule
        Meeting duration
        Optional: Data range

    Ouptut:
        Best meeting time?
        Selection of meeting times?

    API:
'''

# -------------------------- Imports -------------------------- #

# My modules
from google_calendar import get_events

import datetime
from pytz import timezone

# -------------------------- Constants -------------------------- #

# datetime codes. Monday == 0, Sunday == 6.
_weekdays = [ 0, 1, 2, 3, 4 ]
_weekends = [ 5, 6 ]
_all_days = _weekdays + _weekends

# datetime hours.
_workday_hours = list(range(9, 17))             # 9am-5pm
_extended_workday_hours = list(range(8, 19))    # 8am-7pm
_all_hours = list(range(0, 24))                 # 24 hours

# -------------------------- General Helper Functions -------------------------- #

def _minutes_to_seconds(minutes):
    return 60 * minutes

def _hours_to_seconds(hours):
    return _minutes_to_seconds(60 * hours)

def _days_to_seconds(days):
    return _hours_to_seconds(24 * days)

def _get_duration_in_seconds(days = 0, hours = 0, minutes = 0, seconds = 0):
    return _days_to_seconds(days) \
            + _hours_to_seconds(hours) \
            + _minutes_to_seconds(minutes) \
            + seconds

# -------------------------- Scheduler Helper Functions -------------------------- #

def _get_datetime_object(event_dict):
    '''
        Get date-time object from event dict.
        event_dict has form:
            {'date' : '2019-02-25'}
        or:
            {'dateTime' : '2019-02-25 13:30:00-08:00'}
    '''
    event_dict = event_dict.get('dateTime', event_dict.get('date'))
    # This handles colon in time-zone: 2019-02-25 13:30:00-08:00 --> 2019-02-25 13:30:00-0800
    if ':' in event_dict[-4:]:
        event_dict = ''.join(event_dict.rsplit(':', 1))

    try:
        datetime_object = datetime.datetime.strptime(event_dict, '%Y-%m-%dT%H:%M:%S%z')
    except:
        datetime_object = datetime.datetime.strptime(event_dict, '%Y-%m-%d')
        # Add timezone info
        localtz = timezone('America/Los_Angeles')
        datetime_object = localtz.localize(datetime_object)
    
    return datetime_object

def _get_start_datetime(event):
    '''
        Get start dateTime object from event.
    '''
    return _get_datetime_object(event['start'])

def _get_end_datetime(event):
    '''
        Get end dateTime object from event.
    '''
    return _get_datetime_object(event['end'])

def _is_valid_datetime(datetime_object, allowed_days, allowed_hours):
    '''
        Checks that datetime_object conforms to allowed parameters.
    '''
    if datetime_object.week not in allowed_days:
        return False
    elif datetime_object.hour not in allowed_hours:
        return False

    return True

# -------------------------- Event Scheduling Function -------------------------- #

def _schedule_event(events,
                    days = 0,
                    hours = 0,
                    minutes = 0,
                    seconds = 0,
                    allowed_days = _all_days,
                    allowed_hours = _all_hours
                    ):
    '''
        Checks for open slots to schedule the event.
    '''
    requested_time = _get_duration_in_seconds(days = days, hours = hours, minutes = minutes, seconds = seconds)

    for i in range(len(events) - 1):
        start_event = events[i]
        start = _get_end_datetime(start_event)
        next_event = events[i + 1]
        end = _get_start_datetime(next_event)
        
        hour = end.hour
        # print("hours: ", hour)
        # print("start: ", start)
        # print("end: ", end)
        available_time = (end - start).seconds
        if available_time >= requested_time:
            return start

    return "Could not scheduled a meeting."
        # print("available_time: ", available_time)

# -------------------------- Testing -------------------------- #

def schedule_event(num_hours):
    events = get_events(num_events = 10)
    return _schedule_event(events, hours = num_hours)

if __name__ == '__main__':
    schedule_event(1)
