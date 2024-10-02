import logging
import firebase_admin
from firebase_admin import credentials, storage

FIREBASE_AUTH_FILE_PATH = "src/service_account_key.json"


def initialize_firebase():
    cred = credentials.Certificate(FIREBASE_AUTH_FILE_PATH)
    firebase_admin.initialize_app(
        cred, {"storageBucket": "smart-doorbell-9bd31.appspot.com"}
    )
    logging.info("Firebase initialized.")


async def upload_image_to_firebase(image_data, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_data, content_type="image/jpeg")
    logging.info(f"Image uploaded to Firebase Storage: {file_name}")
