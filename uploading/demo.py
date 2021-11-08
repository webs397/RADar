from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

folder_id = '1pHL26t0oeDGo7h0FmMMQ08e76J0JaTRn'

file_names = []
mime_types = ['application/vnd.google-apps.video']

for file_name in file_names:
    file_metadata={
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload('~/RADar/danger/{0}'.format(file_name), mimetype='application/vnd.google-apps.video')
    service.files().create(
        body=file.metadata,
        media_body=media,
        fields='id'
    ).execute()