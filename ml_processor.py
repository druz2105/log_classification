import pickle

import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load saved embeddings and DBSCAN model
with open("./models/dbscan_model.pkl", "rb") as f:
    dbscan = pickle.load(f)

df = pd.read_csv("./models/log_clusters.csv")
embeddings = np.load("./models/log_embeddings.npy")

# Compute cluster centers for matching new messages
cluster_centers = {
    cluster_id: np.mean(embeddings[df['cluster'] == cluster_id], axis=0)
    for cluster_id in set(df['cluster']) if cluster_id != -1
}

severity_classifier_model = joblib.load('./models/severity_logistic_model.joblib')


def classify_with_bert(log_message):
    """Checks if a log message belongs to a known cluster, then classifies severity."""

    # Encode new log message
    message_embedding = transformer_model.encode(log_message, normalize_embeddings=True).reshape(1, -1)

    # Compute similarity with known clusters
    similarities = {
        cluster_id: cosine_similarity(message_embedding, cluster_centroid.reshape(1, -1))[0, 0]
        for cluster_id, cluster_centroid in cluster_centers.items()
    }

    best_cluster = max(similarities, key=similarities.get, default=None)
    max_similarity = similarities.get(best_cluster, 0)
    print(f"Similarity with known clusters: {max_similarity}")
    # Threshold for matching
    SIMILARITY_THRESHOLD = 0.5
    if max_similarity >= SIMILARITY_THRESHOLD:
        # Message belongs to a known cluster → Classify severity
        severity_class = severity_classifier_model.predict(message_embedding)[0]
        return severity_class
    else:
        return "Unclassified"


if __name__ == "__main__":
    logs = [
        "Unexpected system crash due to unhandled null pointer error.",
        "hey chill men",
        "ValueError: Invalid credit card number format in payment gateway.",
        "Banking data retrieval timeout error.",
        "Unauthorized access attempt detected from unknown IP.",
        "Unauthorized access for payment gateway API."
    ]
    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)
