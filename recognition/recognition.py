import face_recognition 
import numpy as np

class Recognition:
    
    def __init__(self, encodings_storage) -> None:  
        self.encodings_storage = encodings_storage
    
    def face_locations_encodings(self, numpy_image_data):
        face_locations = face_recognition.face_locations(numpy_image_data)
        face_encodings = face_recognition.face_encodings(numpy_image_data, face_locations)
        return face_encodings, face_locations

    def find_matches(self, face_encodings, face_locations):
        matches = []
        registered_faces = self.encodings_storage.get_registred_encodings()  # Fixed typo in variable name
        
        for name, known_encodings in registered_faces.items():
            for face_encoding, face_location in zip(face_encodings, face_locations):
                if not len(face_encoding):  # Check if face_encoding is empty or None
                    continue

                confidence_threshold = 0.5# Adjust as needed
                matched = face_recognition.compare_faces(known_encodings, face_encoding, confidence_threshold)

                if all(matched):
                    matches.append({
                        "name": name,
                        "encodings": known_encodings,
                        "location": face_location
                    })
        for face_encoding, face_location in zip(face_encodings, face_locations):
            if not any(face_encoding):  # Check if face_encoding is empty or None
                continue
            
            # Iterate through registered faces to find matches
            is_unknown = True
            for _, known_encodings in registered_faces.items():
                confidence_threshold = 0.5 # Adjust as needed
                matched = face_recognition.compare_faces(known_encodings, face_encoding, confidence_threshold)
                if any(matched):  # If any match is found, it's not an unknown face
                    is_unknown = False
                    break
            
            if is_unknown:
                matches.append({
                    "name": "Unknown",
                    "encodings": [],
                    "location": face_location,
                    "known": False  # Indicates that the face is unknown
                })       

        return matches






