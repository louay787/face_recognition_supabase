from abc import ABC
import os
import face_recognition


class Storage(ABC):
    def load(): pass
    def registred_face_encoding(): pass
    def get_registred_encodings(): pass


class EncodingLocalStorage(Storage):
    # OUR REGISTRED USER FACES ARE STORED HERE
    REGISTRED_ENCODINGS = {}

    def __init__(self, images_path):
        self.check_or_make_directory(images_path)
        self.REGISTRED_ENCODINGS = self.load(images_path)

    def check_or_make_directory(self, images_folder):
        if not os.path.exists(images_folder) or not os.path.isdir(images_folder):
            os.makedirs(images_folder)
        return True

    def load(self, images_folder):
        person_to_encoding = {}

        for person_folder in os.listdir(images_folder):
            person_path = os.path.join(images_folder, person_folder)

            if not os.path.isdir(person_path):
                continue  # Use 'continue' instead of 'return' to proceed with the next iteration

            encodings = []  # Initialize encodings list for each person
            for image_file in os.listdir(person_path):
                user_image_path = os.path.join(person_path, image_file)

                if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue  # Use 'continue' instead of 'return' to proceed with the next iteration

                user_image = face_recognition.load_image_file(user_image_path)
                face_encodings = face_recognition.face_encodings(user_image)

                if not face_encodings:
                    continue  # Use 'continue' instead of 'return' to proceed with the next iteration

                encodings.extend(face_encodings)  # Extend the encodings list

            person_to_encoding[person_folder] = encodings  # Assign the encodings list to the person
        return person_to_encoding

    def get_registred_encodings(self):
        return self.REGISTRED_ENCODINGS

    def register_face_encoding(face_id, encodings):
        pass