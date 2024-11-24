import face_recognition
import cv2
import numpy as np

# Function to encode faces from images
def encode_faces(image_paths):
    known_face_encodings = []
    known_face_names = []

    for image_path in image_paths:
        # Load the image
        image = face_recognition.load_image_file(image_path)
        
        # Get the face encoding for the image
        face_encoding = face_recognition.face_encodings(image)
        
        if len(face_encoding) > 0:
            known_face_encodings.append(face_encoding[0])
            known_face_names.append(image_path.split('/')[-1].split('.')[0])  # Using file name as person's name
        else:
            print(f"No face found in {image_path}")
    
    return known_face_encodings, known_face_names

# Function to recognize faces in a given image (for login)
def recognize_face(known_face_encodings, known_face_names, image_path):
    # Load the test image
    image = face_recognition.load_image_file(image_path)
    
    # Find all face locations and encodings in the test image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    print(f"Number of faces detected: {len(face_encodings)}")  # Debugging line

    if len(face_encodings) == 0:
        return "No face detected"
    
    # Check if any faces match the known faces with a tolerance level
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)  # Tolerance adjusted to 0.6

        name = "Unknown"
        
        # If a match is found, get the name of the person
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        return name
    
    return "No match found"
