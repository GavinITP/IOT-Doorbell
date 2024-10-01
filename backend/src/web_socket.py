import asyncio
import websockets
import logging
import time
import firebase_admin
from firebase_admin import credentials, storage

logging.basicConfig(level=logging.INFO)

cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(
    cred, {"storageBucket": "smart-doorbell-9bd31.appspot.com"}
)

sender_conn = None
receiver_conn = None


async def upload_image_to_firebase(image_data, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_data, content_type="image/jpeg")
    logging.info(f"Image uploaded to Firebase Storage: {file_name}")


async def ws_handler(websocket, path):
    global sender_conn, receiver_conn

    client_type = path.split("?type=")[-1] if "?type=" in path else ""

    if client_type == "sender":
        sender_conn = websocket
        logging.info("Sender connected")
    elif client_type == "receiver":
        receiver_conn = websocket
        logging.info("Receiver connected")
    else:
        logging.error("Unknown client type")
        return

    try:
        async for message in websocket:
            logging.info(f"{client_type.capitalize()} received message")
            if client_type == "sender":
                if receiver_conn:
                    await receiver_conn.send(message)
                    if isinstance(message, bytes):
                        file_name = time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
                        await upload_image_to_firebase(message, file_name)
            elif client_type == "receiver":
                if sender_conn:
                    await sender_conn.send(message)
    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed: {e}")
    finally:
        if client_type == "sender":
            sender_conn = None
            logging.info("Sender disconnected")
        elif client_type == "receiver":
            receiver_conn = None
            logging.info("Receiver disconnected")


async def main():
    async with websockets.serve(ws_handler, "localhost", 6969):
        logging.info("WebSocket server started at ws://localhost:6969")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
