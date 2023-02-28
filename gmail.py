from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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

    service = build('gmail', 'v1', credentials=creds)

    return service


def send_message(service):
    message = EmailMessage()
    content = input('Írd be mi legyen az e-mail szövege: ')
    to = input('Írd be kinek akarod küldeni az e-mailt: ')
    from_email = input('Írd be melyik e-mailről akarod küldeni az üzenetet: ')
    subject = input('Írd be mi legyen az e-mail tárgya: ')

    message.set_content(content)

    message['To'] = to
    message['From'] = from_email
    message['Subject'] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }
    szam = 0
    while szam < 4:
        send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
        szam = szam + 1
        print(F'Message Id: {send_message["id"]}')


def main():
    service = get_service()
    send_message(service)


main()
