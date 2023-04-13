import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]
flow = InstalledAppFlow.from_client_secrets_file("App/gmail_info.json", SCOPES)
creds = flow.run_local_server(port = 0)
service = build("gmail", "v1", credentials = creds)

def send_email(to):
    message = MIMEText("HELLO " + str(to) + "!!!")
    message["to"] = to
    message["subject"] = "This is very important."
    create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userID = "me", body = create_message).execute())
    except HTTPError as error:
        print("OH NO")
        message = None