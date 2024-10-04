import io
from PIL import Image
import face_recognition as fr
import numpy as np
import os
import pickle

MODEL_PATH = "model/encoded.pickle"


def load_and_encode_faces(dataset_path):
    known_face_encodings = []
    known_face_names = []

    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)

        if os.path.isdir(person_folder):
            for image_name in os.listdir(person_folder):
                image_path = os.path.join(person_folder, image_name)
                image = fr.load_image_file(image_path)
                face_encodings = fr.face_encodings(image)

                if len(face_encodings) > 0:
                    known_face_encodings.append(face_encodings[0])
                    known_face_names.append(person_name)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)

    return known_face_encodings, known_face_names


def recognize_faces_in_image(known_face_encodings, known_face_names, image_data):
    image = Image.open(io.BytesIO(image_data))
    test_image = np.array(image)

    face_encodings = fr.face_encodings(test_image)

    if len(face_encodings) == 0:
        return ("No face detected", False)

    for face_encoding in face_encodings:
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        face_distances = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            return (name, True)

    return ("Unknown", False)
