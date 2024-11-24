import os
import numpy as np
import cv2
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load pre-trained VGG16 model for feature extraction (excluding the top layers)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
model = Model(inputs=base_model.input, outputs=base_model.layers[-1].output)

# Function to preprocess and extract features from an image
def preprocess_and_extract_features(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)
    return features.flatten()

# Simulate a database of retina images
image_dir = r"D:\cms extra1\img"
database_features = {}

# Extract and store features for each image in the database
for image_file in os.listdir(image_dir):
    if image_file.endswith(('jpg', 'jpeg', 'png', 'ppm')):
        image_path = os.path.join(image_dir, image_file)
        features = preprocess_and_extract_features(image_path)
        database_features[image_file] = features

# Save the database features to a file for future use
with open("retina_database.pkl", "wb") as f:
    pickle.dump(database_features, f)
