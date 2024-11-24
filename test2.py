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

# Streamlit app interface
st.title("Retina Image Match Finder")

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
