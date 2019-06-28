from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from datetime import datetime
import pandas

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



def printMessages(service, user_id, query=''):
    response = service.users().messages().list(userId=user_id, q=query, maxResults=250).execute()

    test_dict = {}
    test_dict['unixtime'] = []
    test_dict['date_time'] = []
    test_dict['day_of_the_week'] = []
    test_dict['day_of_lesson'] = []
    test_dict['time_of_lesson'] = []
    test_dict['place_of_lesson'] = []
    test_dict['performer'] = []

    if 'messages' in response:
        for message_id in response['messages']:
            message = service.users().messages().get(userId=user_id, id=message_id['id'], format='raw').execute()
            unixTimeStamp = int(message['internalDate'][:10])
            dateTime = datetime.fromtimestamp(unixTimeStamp)
            weekDay = dateTime.weekday()
            snippest_list = message['snippet'].split(" ")
            dayOfLesson = snippest_list[3].split("：")[1]
            timeOfLesson = snippest_list[4]
            placeOfLesson = snippest_list[6].split("パフォーマー")[0]
            performer = snippest_list[7]


            test_dict['unixtime'] = unixTimeStamp
            test_dict['date_time'].append(dateTime)
            test_dict['day_of_the_week'].append(weekDay)
            test_dict['day_of_lesson'].append(dayOfLesson)
            test_dict['time_of_lesson'].append(timeOfLesson)
            test_dict['place_of_lesson'].append(placeOfLesson)
            test_dict['performer'].append(performer)
   
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
        for message_id in response['messages']:
            message = service.users().messages().get(userId=user_id, id=message_id['id'], format='raw').execute()
            unixTimeStamp = int(message['internalDate'][:10])
            dateTime = datetime.fromtimestamp(unixTimeStamp)
            weekDay = dateTime.weekday()
            snippest_list = message['snippet'].split(" ")
            dayOfLesson = snippest_list[3].split("：")[1]
            timeOfLesson = snippest_list[4]
            placeOfLesson = snippest_list[6].split("パフォーマー")[0]
            performer = snippest_list[7]

            test_dict['unixtime'] = unixTimeStamp
            test_dict['date_time'].append(dateTime)
            test_dict['day_of_the_week'].append(weekDay)
            test_dict['day_of_lesson'].append(dayOfLesson)
            test_dict['time_of_lesson'].append(timeOfLesson)
            test_dict['place_of_lesson'].append(placeOfLesson)
            test_dict['performer'].append(performer)
    columns=['unixtime', 'date_time', 'day_of_the_week', 'day_of_lesson','time_of_lesson','place_of_lesson','performer']
    return pandas.DataFrame.from_dict(test_dict).ix[:,columns]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
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
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    test=printMessages(service, 'me', 'from:noreply@b-monster.jp キャンセル待ち登録をいただいた以下')
    
    test.to_csv("bmonster_canceldata.csv",index=False)
if __name__ == '__main__':
    main()
