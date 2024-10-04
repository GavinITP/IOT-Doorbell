# IoT Doorbell

This project implements a smart doorbell system that leverages facial recognition technology to enhance home security.
The system comprises three main components: a backend service, a frontend application, and a Raspberry Pi interface.

# Set Up & Guide

## Requirements
- [Requirements for face_recognition package](https://github.com/ageitgey/face_recognition)
- Python 3

## Backend

### Navigate to backend/
```
cd backend
```

### Firebase credential
- Add service_account_key.json in src/

### Set Up a Virtual Environment (Optional)
1. Create a Virtual Environment
```
python -m venv .venv
```
2. Activate the Virtual Environment
  - MacOS/ Linux
```
source .venv/bin/activate
```
  - Windows
```
.venv\Scripts\activate
```
### Install Packages
```
pip install -r requirements.txt
```
### Run
```
python3 src/main.py
```
## How can I train a face recognition model ?
*(Assume that you have already navigated to backend/ and completely set up the backend)*
1. Delete encoded.pickle in the backend/model if that file exists
```
rm model/encoded.pickle
```
2. In dataset/, Create a new folder with the person's name and insert their face images
- Recommend: >= 15 images
- You can use any file name and file extension with **.jpg .jpeg or .png**

![folder](https://i.ibb.co/mCr2N66/Screenshot-2567-10-04-at-17-24-15.png)

4. Run
```
python3 src/main.py
``` 

## Frontend

### Navigate to frontend/
```
cd frontend
```
### Install Dependencies
```
npm install
```
### Run
```
npm run dev
```

## Raspberry Pi

### Navigate to raspberry-pi/
```
cd raspberry-pi
```

### Choose image to sent to backend
- change image_path in src/main.py

### Set Up a Virtual Environment (Optional)
*(Same as above)*

### Install Packages
```
pip install -r requirements.txt
```

### Run
```
python3 src/main.py
```
