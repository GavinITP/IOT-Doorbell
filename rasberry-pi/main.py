import asyncio
import websockets
import logging
import os

logging.basicConfig(level=logging.INFO)


async def send_image(websocket, image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            await websocket.send(image_data)
            logging.info(f"Sent image: {image_path}")
    else:
        logging.error(f"Image file not found: {image_path}")


async def main():
    uri = "ws://localhost:6969?type=sender"
    async with websockets.connect(uri) as websocket:
        image_path = "path/to/your/image.jpg"
        await send_image(websocket, image_path)


if __name__ == "__main__":
    asyncio.run(main())
