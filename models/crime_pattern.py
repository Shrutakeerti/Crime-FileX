
# backend/models/crime_pattern_model.py
from sklearn.cluster import KMeans
import joblib
import numpy as np

# Sample crime pattern data
X = np.random.rand(100, 5)
model = KMeans(n_clusters=3)
model.fit(X)
joblib.dump(model, "crime_pattern_model.pkl")
