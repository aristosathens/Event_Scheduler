'''
    Aristos Athens

    Get list of events of from Google's API.
'''

import os
import datetime
import pickle
import webbrowser # Let's us open links in user's browser
from pprint import pprint

# Google provided libraries. See https://developers.google.com/calendar/quickstart/python
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Ensure cwd is the location of this file.
print("Updating cwd...")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Redirect url if credentials.json not found.
_credentials_not_found_url = "https://developers.google.com/calendar/quickstart/python"

def _get_credentials():
    '''
        Load user credentials.
        Looks in current directory for credentials.json and token.pickle.
    '''
    creds = None

    # If user does not have 'credentials.json'
    if not os.path.isfile("credentials.json"):
        try:
            webbrowser.open(_credentials_not_found_url, new = 2)
        except:
            pass

        raise Exception("\n\nError: No 'credentials.json' file found. Go to the following url: " + 
            _credentials_not_found_url + 
            "\nPress 'ENABLE THE GOOGLE CALENDAR API' to download credentials.json, and put it in: " + 
            os.path.dirname(os.path.abspath(__file__)) + "\n")

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # If user does not have 'token.pickle'
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def _get_events(credentials,
                num_events = 10,
                start_date = None,
                end_date = None,
                weeks = 1,
                days = 0,
                hours = 0,
                minutes = 0):
    '''
        Get events from user's calendar.
        Returns list, which is ordered in ascending time/date.
    '''
    if start_date == None:
        start_date = datetime.datetime.utcnow()
    if end_date == None:
        end_date = start_date + datetime.timedelta(weeks = weeks, days = days, hours = hours, minutes = minutes)

    # Convert datetime objects to strings for http request.
    try:
        start_date = start_date.isoformat() + 'Z' # 'Z' indicates UTC time
        end_date = end_date.isoformat() + 'Z'
    except AttributeError:
        pass

    # Call the Calendar API.
    service = build('calendar', 'v3', credentials = credentials)
    events_result = service.events().list(calendarId = 'primary',
                                            timeMin = start_date,
                                            timeMax = end_date,
                                            maxResults = num_events,
                                            singleEvents = True,
                                            orderBy = 'startTime').execute()
    return events_result.get('items', [])

def get_events(num_events):
    '''

    '''
    credentials = _get_credentials()
    return _get_events(credentials, num_events = num_events)

if __name__ == '__main__':
    raise Exception("Don't run this as a script. Import get_events().")
