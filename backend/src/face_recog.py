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


def recognize_faces_in_image(known_face_encodings, known_face_names, image_path):
    test_image = fr.load_image_file(image_path)
    face_encodings = fr.face_encodings(test_image)

    if len(face_encodings) == 0:
        print("No face detected")
        return

    for face_encoding in face_encodings:
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        face_distances = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if not matches[best_match_index]:
            print("Unknown!")
            print("Status: Reject")

            return False

        name = known_face_names[best_match_index]
        print(f"Welcome {name} ~")
        print("Status: Accept")

        return True


if __name__ == "__main__":
    dataset_path = "dataset"

    if os.path.exists(MODEL_PATH):
        print("Loading encodings from file...")
        with open(MODEL_PATH, "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)
    else:
        print("Encoding faces from dataset...")
        known_face_encodings, known_face_names = load_and_encode_faces(dataset_path)

    test_image_path = "validation/Lilas Ikuta/20.jpg"
    recognize_faces_in_image(known_face_encodings, known_face_names, test_image_path)
