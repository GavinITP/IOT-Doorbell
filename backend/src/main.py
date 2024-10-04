import asyncio
import datetime
import os
import pickle
import websockets
import logging

from firebase_utils import initialize_firebase, upload_image_to_firebase
from face_recog import load_and_encode_faces, recognize_faces_in_image

MODEL_PATH = "model/encoded.pickle"

known_face_encodings = []
known_face_names = []

logging.basicConfig(level=logging.INFO)
connections = {"raspberry_pi": None, "frontend": None}


async def ws_handler(websocket, path):
    client_type = path.split("?type=")[-1] if "?type=" in path else None

    if client_type not in connections:
        logging.error(f"Unknown client type: {client_type}")
        return

    connections[client_type] = websocket
    logging.info(f"{client_type} connected")

    try:
        async for image_data in websocket:
            logging.info(f"Received image from {client_type}")
            if connections["frontend"]:
                await connections["frontend"].send(image_data)
            else:
                logging.warning("Frontend connection is not available.")

            await process_image_data(image_data)

    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed for {client_type}: {e}")
    finally:
        connections[client_type] = None
        logging.info(f"{client_type} disconnected")


async def process_image_data(image_data):
    try:
        name, accepted = recognize_faces_in_image(
            known_face_encodings, known_face_names, image_data
        )
        status = "Accept" if accepted else "Reject"
        response_message = f"{name}: {status}"

        if connections["frontend"]:
            await connections["frontend"].send(image_data)
            logging.info(f"Sent image to frontend")

        if connections["frontend"]:
            await connections["frontend"].send(response_message)
            logging.info(f"Sent response message to frontend: {response_message}")

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        file_extension = "jpg" if image_data.startswith(b"\xff\xd8") else "png"
        file_name = f"{current_datetime}_{name}.{file_extension}"
        await upload_image_to_firebase(image_data, file_name)

        if connections["raspberry_pi"]:
            await connections["raspberry_pi"].send(response_message)
        else:
            logging.warning("Raspberry Pi connection is not available")

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        if connections["raspberry_pi"]:
            await connections["raspberry_pi"].send("Error processing image")


async def main():
    global known_face_encodings, known_face_names

    initialize_firebase()

    if os.path.exists(MODEL_PATH):
        logging.info("Loading encodings from file...")
        with open(MODEL_PATH, "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)
    else:
        logging.info("Encoding faces from dataset...")
        dataset_path = "dataset"
        known_face_encodings, known_face_names = load_and_encode_faces(dataset_path)

    logging.info("Completely loaded face encoding")

    async with websockets.serve(ws_handler, "localhost", 8080):
        logging.info("WebSocket server started at ws://localhost:8080")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
