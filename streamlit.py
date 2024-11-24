import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import face_recognition
from PIL import Image

# Helper function to interact with the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE NOT NULL,
            case_date TEXT NOT NULL,
            case_details TEXT NOT NULL,
            crime_type TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_case(case_id, case_date, case_details, crime_type, location):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases (case_id, case_date, case_details, crime_type, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_id, case_date, case_details, crime_type, location))
    conn.commit()
    conn.close()

def delete_case(case_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cases WHERE case_id = ?', (case_id,))
    conn.commit()
    conn.close()

def view_cases():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cases')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Streamlit app title
st.title("Criminal Management System")

# Login Page
def login():
    st.header("Login to the System")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    
    if st.button("Login"):
        if username == "admin" and password == "admin123" :
            st.success("Login successful!")
            return True
        else:
            st.error("Login failed. Please check your credentials and face verification.")

    return False

# Crime Pattern Analysis Page (CSV Upload)
def crime_pattern_analysis():
    st.header("Crime Pattern Analysis")
    file_path = st.file_uploader("Upload Crime Data CSV", type="csv")

    if file_path is not None:
        data = pd.read_csv(file_path)
        data = data.drop(columns=['Unnamed: 2'])
        data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()
        data = data.dropna(subset=['area_name', 'date', 'group_name', 'sub_group_name', 'auto_theft_stolen'])
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data.dropna(subset=['date'])

        st.write("Cleaned Dataset Information:")
        st.write(data.info())
        st.write("\nFirst few rows of the cleaned dataset:")
        st.write(data.head())

        # Crime Counts by Area
        st.subheader("Total Crime Incidents by Area")
        area_counts = data['area_name'].value_counts()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=area_counts.index, y=area_counts.values, palette='viridis', ax=ax)
        plt.xticks(rotation=90)
        plt.title('Total Crime Incidents by Area')
        plt.xlabel('Area Name')
        plt.ylabel('Crime Count')
        st.pyplot(fig)

        # Auto Theft Incidents by Type
        st.subheader("Auto Theft Incidents by Type")
        theft_cols = ['auto_theft_coordinated/traced', 'auto_theft_recovered', 'auto_theft_stolen']
        theft_totals = data[theft_cols].sum()
        fig, ax = plt.subplots(figsize=(8, 5))
        theft_totals.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax)
        plt.title('Auto Theft Incidents by Type')
        plt.xlabel('Type of Auto Theft')
        plt.ylabel('Number of Incidents')
        st.pyplot(fig)

        # Monthly Crime Trends
        st.subheader("Monthly Crime Trend")
        data['month'] = data['date'].dt.to_period('M')
        monthly_trend = data.groupby('month').size()
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_trend.plot(ax=ax)
        plt.title('Monthly Crime Trend')
        plt.xlabel('Month')
        plt.ylabel('Number of Crimes')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        
        
# Import necessary libraries
import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained model for feature extraction
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)

# Load the saved database of features
with open("retina_database.pkl", "rb") as f:
    database_features = pickle.load(f)

# Preprocess and extract features from an uploaded image
def preprocess_and_extract_features_for_upload(image):
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)
    return features.flatten()

# Retina match finder function
def retina_match_page():
    st.header("Retina Image Match Finder")
    
    uploaded_file = st.file_uploader("Upload a retinal image to check for a match...", type=["jpg", "jpeg", "png", "ppm"])
    
    if uploaded_file is not None:
        uploaded_features = preprocess_and_extract_features_for_upload(uploaded_file)
        
        # Compare with database features
        found_match = False
        for image_name, db_features in database_features.items():
            similarity = cosine_similarity([uploaded_features], [db_features])
            if similarity[0][0] > 0.9:  # Threshold for match (adjust as needed)
                st.write(f"**Match Found:** The uploaded retina matches with {image_name}")
                found_match = True
                break
        
        if not found_match:
            st.write("**Match Not Found:** No matching retina image found in the database.")

# Add 'Retina Image Match Finder' to the menu
menu = ["Login", "Home", "Add Case", "Delete Case", "View Cases", "Crime Pattern Analysis", "Face Recognition", "Retina Match Finder", "Contact"]
choice = st.sidebar.selectbox("Select a Page", menu)

# Call the appropriate function based on the user's choice
if choice == "Retina Match Finder":
    retina_match_page()
        
# Add page for face detection
def face_recognition_page():
    st.header("Face Recognition Login")
    
    # Start webcam
    webcam_image = st.camera_input("Capture your face to login")

    if webcam_image:
        # Save the image
        with open("temp.jpg", "wb") as f:
            f.write(webcam_image.getbuffer())
        
        # Recognize the face
        name = recognize_face(known_face_encodings, known_face_names, "temp.jpg")
        
        if name != "No match found":
            st.success(f"Hello, {name}! You are successfully logged in.")
        else:
            st.error("No match found! Try again.")
    
    else:
        st.warning("Please capture an image from your webcam.")

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

# Prepare the dataset of known faces
image_paths = [r"D:\cms extra1\Static\face_images\WhatsApp Image 2024-11-14 at 2.09.42 AM.jpeg", 
               r"D:\cms extra1\Static\face_images\WhatsApp Image 2024-11-14 at 2.09.44 AM (1).jpeg"]  # Add more paths as needed
known_face_encodings, known_face_names = encode_faces(image_paths)

# Initialize the database
init_db()



if choice == "Login":
    if login():
        choice = st.sidebar.selectbox("Select a Page", menu[1:])

# Home Page
if choice == "Home":
    st.header("Welcome to the Criminal Management System")
    st.write("This system is designed to manage criminal cases, analyze crime patterns, and perform biometric checks.")

# Add Case Page
elif choice == "Add Case":
    st.header("Add a New Case")
    with st.form("case_form"):
        case_id = st.text_input("Case ID")
        case_date = st.date_input("Date", datetime.date.today())
        case_details = st.text_area("Case Details")
        crime_type = st.text_input("Type of Crime")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Add Case")

        if submitted:
            if case_id and case_date and case_details and crime_type and location:
                add_case(case_id, case_date.strftime('%Y-%m-%d'), case_details, crime_type, location)
                st.success("Case added successfully!")
            else:
                st.warning("Please fill out all fields.")

# Delete Case Page
elif choice == "Delete Case":
    st.header("Delete a Case")
    with st.form("delete_form"):
        delete_case_id = st.text_input("Enter Case ID to Delete")
        delete_submitted = st.form_submit_button("Delete Case")

        if delete_submitted:
            if delete_case_id:
                delete_case(delete_case_id)
                st.success("Case deleted successfully!")
            else:
                st.warning("Please enter a Case ID.")

# View Cases Page
elif choice == "View Cases":
    st.header("View All Cases")
    cases = view_cases()

    if cases:
        df = pd.DataFrame(cases, columns=["ID", "Case ID", "Date", "Details", "Crime Type", "Location"])
        st.write(df)
    else:
        st.warning("No cases found.")

# Crime Pattern Analysis Page
elif choice == "Crime Pattern Analysis":
    crime_pattern_analysis()

# Face Recognition Page
elif choice == "Face Recognition":
    face_recognition_page()



# Contact Page
elif choice == "Contact":
    st.header("Contact Us")
    st.write("""
        For inquiries, please reach out at:
        - **Email**: support@criminalsystem.com
        - **Phone**: +123 456 7890
    """)

