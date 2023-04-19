from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = "client_secrets.json"

def get_authenticated_service():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    return InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
   
def build_youtube(credentials):
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
