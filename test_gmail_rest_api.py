import pytest
import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@pytest.fixture(scope="module")
def setup():
    creds = None
    SCOPES = ['https://mail.google.com/']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print(creds)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service


def test_get_labels(setup):
    """
    Test the gmail GET API
    underlying GET API call: url = GET "https://gmail.googleapis.com/gmail/v1/users/{user_id}/labels"
    :param setup: fixture returns the API binding object to gmail service
    """
    service = setup
    label_name = "APITestLabel"
    found = False
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
        assert False, "No labels found"
    print('Labels:')
    for label in labels:
        print(label['name'])
        if label_name in label['name']:
            found = True
            break
    assert found, f"The label {label_name} not found"


def test_post_msg(setup):
    """
    Test the gmail POST API
    underlying POST API call: url = "POST https://gmail.googleapis.com/upload/gmail/v1/users/{userId}/messages/send"
    :param setup: fixture returns the API binding object to gmail service
    """
    service = setup
    label_name = "APITestLabels"
    found = False
    email_msg = "This is a test email"
    mime_message = MIMEMultipart()
    mime_message['to'] = "nagaraj.quantify@gmail.com"
    mime_message['subject'] = "This email"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(f"Details of the message posted: {message}")
    assert message['id'], "Message send unsuccessful"

def test_get_message_positive(setup):
    """
    Test the gmail GET API
    underlying GET API call: url = "GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}"
    :param setup: fixture returns the API binding object to gmail service
    """
    service = setup
    found = False
    results = service.users().messages().list(userId='me').execute()
    print(f"Results messages {results}")
    print(len(results['messages']))
    for message in results['messages']:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        msg_body = msg['snippet']
        if msg_body == "This is a test email":
            found = True
            break
    assert found, f"Intended email not found"

def test_get_message_negative(setup):
    """
    Test the gmail GET API
    underlying GET API call: url = "GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}"
    :param setup: fixture returns the API binding object to gmail service
    """
    service = setup
    found = False
    results = service.users().messages().list(userId='me').execute()
    print(f"Results messages {results}")
    print(len(results['messages']))
    for message in results['messages']:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        msg_body = msg['snippet']
        if msg_body == "Some Random Dummy message for negative scenario":
            found = True
            break
    assert not found, f"Email found, which was supposed to be not found"

def test_delete_message(setup):
    """
    Test the gmail DELETE API
    underlying DELETE API call: url = "DELETE https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}"
    :param setup: fixture returns the API binding object to gmail service
    """
    service = setup
    results = service.users().messages().list(userId='me').execute()
    message_list = results['messages']
    assert results['resultSizeEstimate'] != 0, "There are no messages in Inbox"
    print(len(results['messages']))
    id_list = []
    for count in range(0, len(message_list)):
        id_list.append(message_list[count]['id'])
    for count in range(0, len(id_list)):
        service.users().messages().delete(userId='me', id=id_list[count]).execute()
    results = service.users().messages().list(userId='me').execute()
    assert results['resultSizeEstimate'] == 0, "There are still some messages in the Inbox"
    print(f"last test case second: {results}")
