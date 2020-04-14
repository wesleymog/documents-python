from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1xxpl8MBLvG2HwIxuLGHNN-c9eIl5I1oGnzLS9IkrvIw'

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    mergedocs(service)

def createdocs(service):
    title = 'My document'
    body = {
        'title': title
    }
    doc = service.documents() \
        .create(body=body).execute()
    print('Created document with title: {0}'.format(
        doc.get('title')))

def mergedocs(service):
    emission_date = datetime.datetime.now().strftime("%y/%m/%d")
    text1 = "asssssssssssssssssaaaaaaaaaaaaaaa dsaksçsaça"
    text2 = "asssssssssssssssssaaaaaaaaaaaaaaa dsaksçsaça"
    text3 = "asssssssssssssssssaaaaaaaaaaaaaaa dsaksçsaça"
    document_id = DOCUMENT_ID
    requests = [
                    {
                        'insertText': {
                            'location': {
                                'index': 412,
                            },
                            'text': text1
                        }
                    },
                            {
                        'insertText': {
                            'location': {
                                'index': 550,
                            },
                            'text': text2
                        }
                    },
                            {
                        'insertText': {
                            'location': {
                                'index': 1000,
                            },
                            'text': text3
                        }
                    },
                ]

    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()

if __name__ == '__main__':
    main()