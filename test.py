import streamlit as st
import face_recognition

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

    # Check if any faces match the known faces
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        name = "Unknown"
        
        # If a match is found, get the name of the person
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        return name
    
    return "No match found"

# Function to capture and recognize face for login
def webcam_face_login():
    st.title("Face Login")
    
    # Start webcam
    webcam_image = st.camera_input("Capture your face to login")

    if webcam_image:
        # Save the image
        with open("temp.jpg", "wb") as f:
            f.write(webcam_image.getbuffer())
        
        # Recognize the face4
        name = recognize_face(known_face_encodings, known_face_names, "temp.jpg")
        
        if name != "No match found":
            st.success(f"Hello, {name}! You are successfully logged in.")
        else:
            st.error("No match found! Try again.")
    
    else:
        st.warning("Please capture an image from your webcam.")

# Prepare the dataset of known faces
image_paths = [r"D:\cms extra1\Static\face_images\WhatsApp Image 2024-11-14 at 2.09.42 AM.jpeg", r"D:\cms extra1\Static\face_images\WhatsApp Image 2024-11-14 at 2.09.44 AM (1).jpeg"]  # Add more paths as needed
known_face_encodings, known_face_names = encode_faces(image_paths)

# Call the login function
webcam_face_login()
