from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Load client secrets from a file
SERVICE_ACCOUNT_FILE = 'service.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Create credentials from client secrets



def upload_video_to_youtube(video_file, title, description, privacy_status):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': privacy_status
            }
        },
        media_body=video_file
    )
    response = request.execute()
    return response