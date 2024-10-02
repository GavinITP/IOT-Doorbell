import asyncio
import websockets
import logging
import os
from PIL import Image
import io

logging.basicConfig(level=logging.INFO)


async def send_image(websocket, image_path):
    if os.path.exists(image_path):
        try:

            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format="PNG")
                image_data = img_byte_arr.getvalue()

                await websocket.send(image_data)
                logging.info(f"Sent image: {image_path}")
        except Exception as e:
            logging.error(f"Error sending image: {e}")
    else:
        logging.error(f"Image file not found: {image_path}")


async def receive_status(websocket):
    try:
        response_message = await websocket.recv()
        logging.info(f"Received status from server")
        logging.info(f"{response_message}")

    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed while waiting for status: {e}")


async def main():
    PORT = 8080
    uri = f"ws://localhost:{PORT}?type=rasberry_pi"

    async with websockets.connect(uri) as websocket:
        image_path = "images/Elon Musk/18.jpg"

        await send_image(websocket, image_path)
        await receive_status(websocket)


if __name__ == "__main__":
    asyncio.run(main())
