# gmail.py

import os
import base64
from email.mime.text import MIMEText

# ⚠️ Import the correct Request for token refresh
from google.auth.transport.requests import Request  
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = 'token.json'
CREDS_PATH = 'credentials.json'
REDIRECT_PORT = 54333

def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        print("→ No valid token, starting OAuth flow…")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            print(f"→ Spinning up local server on port {REDIRECT_PORT}…")
            creds = flow.run_local_server(
                port=REDIRECT_PORT,
                open_browser=True,
                prompt='consent'
            )
            print("→ OAuth flow complete, tokens acquired.")

        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def send_email(to: str, subject: str, body: str):
    service = get_gmail_service()
    message = MIMEText(body, 'plain')
    message['to']      = to
    message['from']    = 'me'
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
