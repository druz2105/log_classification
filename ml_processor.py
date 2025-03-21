import joblib
from sentence_transformers import SentenceTransformer

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
severity_classifier_model = joblib.load('./models/severity_logistic_model.joblib')


def classify_with_bert(log_message):
    message_embedding = transformer_model.encode(log_message)
    severity_predict_class = severity_classifier_model.predict([message_embedding])[0]
    return severity_predict_class


if __name__ == "__main__":
    logs = [
        "Unexpected system crash due to unhandled null pointer error.",
        "hey chill men",
        "ValueError: Invalid credit card number format in payment gateway.",
        "Banking data retrieval timeout error.",
        "Unauthorized access attempt detected from unknown IP."
    ]
    for log in logs:
        label = classify_with_bert(log)
        print(log, "->", label)
