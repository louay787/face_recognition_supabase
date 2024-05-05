from io import BytesIO
import face_recognition 
import numpy as np


class Recognition:

    def __init__(self) -> None:  
        self.encodings_storage = {}

    def trained_dataset(self, dataset):
        trained_dataset = {}
        for user_id, user_faces in dataset.items():
            for image_bytes in user_faces:
                image_ = face_recognition.load_image_file(BytesIO(image_bytes))
                face_encodings = face_recognition.face_encodings(image_)

                if not face_encodings:
                    continue  # Use 'continue' instead of 'return' to proceed with the next iteration

                trained_dataset.setdefault(user_id, []).extend(face_encodings)  # Extend the encodings list
        self.encodings_storage = trained_dataset

    def face_locations_encodings(self, numpy_image_data):
        face_locations = face_recognition.face_locations(numpy_image_data)
        face_encodings = face_recognition.face_encodings(numpy_image_data, face_locations)
        return face_encodings, face_locations

    def detect_faces(self, numpy_image_data):
        result = []
        face_encodings, face_locations = self.face_locations_encodings(numpy_image_data)

        if not len(self.encodings_storage.items()):
            return result

        for face_encoding, face_location in zip(face_encodings, face_locations):
            found_match = False
            for id, known_encodings in self.encodings_storage.items():
                if not any(face_encoding):  # Check if face_encoding is empty or None
                    continue

                confidence_threshold = 0.6  # Adjust as needed
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                min_distance = min(distances)
                if min_distance <= confidence_threshold:
                    found_match = True
                    result.append({
                        "id": id,
                        "location": face_location,
                        "known": True,
                        "confidence": 1 - min_distance
                    })
                    break  # Exit loop once a known match is found

            if not found_match:
                result.append({
                    "id": "unknown",
                    "location": face_location,
                    "known": False,
                    "confidence": 0.0
                })

        return result





