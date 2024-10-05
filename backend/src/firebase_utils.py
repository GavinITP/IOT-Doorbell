import logging
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime

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


async def fetch_all_history_images():
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    history = []
    current_time = datetime.now()
    expiry_time = int(current_time.timestamp()) + 60 * 60 * 24 * 7 + 3600
    for blob in blobs:
        history.append({
            "name": blob.name,
            "url": blob.generate_signed_url(expiration=expiry_time),
            "timestamp": blob.time_created
        })
    return history
