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

from google_calendar import get_events

import datetime
from pytz import timezone


def get_datetime_object(event_dict):
    '''
        Get date-time object from event dict.
        event_dict has form:
            {'date' : 2019-02-25}
        or:
            {'dateTime' : 2019-02-25 13:30:00-08:00}

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

def get_start_datetime(event):
    '''

    '''
    return get_datetime_object(event['start'])

def get_end_datetime(event):
    '''

    '''
    return get_datetime_object(event['end'])

def schedule_event(events, desired_duration):
    '''
        Checks for open slots to schedule the event.
    '''
    for i in range(len(events) - 1):
        start_event = events[i]
        start = get_end_datetime(start_event)
        next_event = events[i + 1]
        end = get_start_datetime(next_event)


        print("start: ", start)
        print("end: ", end)
        available_time = (end - start).seconds
        print("available_time: ", available_time)


        raise NotImplementedError("schedule_event() has not yet been implemented.")

if __name__ == '__main__':
    events = get_events(num_events = 10)
    schedule_event(events, 2)
    print("Finished main.")
