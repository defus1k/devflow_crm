from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.core.config import settings

class GoogleDriveService:
    """
    Сервіс для автоматизації роботи з Google Drive: завантаження звітів та файлів.
    """
    def __init__(self):
        # Використовуємо JSON-файл сервісного облікового запису (Service Account)
        self.creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        self.service = build('drive', 'v3', credentials=self.creds)

    async def upload_file(self, file_path: str, folder_id: str, file_name: str):
        """
        Завантаження файлу (звіту/документа) у вказану папку на Google Drive.
        """
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        
        # Виконуємо синхронний запит (для Drive API це стандарт)
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')