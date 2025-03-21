from ml_processor import classify_with_bert
from llm_processor import classify_with_llm
from regex_processor import classify_with_regex


def classify_logs(type, message):
    if type in ['Maintenance', 'Access Control Violation', 'Email Failure']:
        label = classify_with_llm(message)
    else:
        label = classify_with_regex(message)
        if label is None:
            label = classify_with_bert(message)

    return label


if __name__ == "__main__":
    test_cases = [
        ("HTTP Error", "Unauthorized access attempt to sensitive data."),
        ("HTTP Error", "Invalid transaction request syntax."),
        ("System Failure", "Multiple failed login attempts detected."),
        ("Security Breach", "NameError: Variable 'account_balance' not defined in fund transfer function."),
        ("HTTP Error", "Unauthorized request for fund transfer API."),
        ("HTTP Error", "Security token missing in authentication process."),
        ("Security Breach", "Timeout error in secure socket layer (SSL) handshake."),
        ("Http Success", "Payment Session P8444113 initiated for authenticated user."),
        ("HTTP Error", "Unauthorized access attempt detected from unknown IP."),
        ("HTTP Error", "Payment submission format error."),
        ("HTTP Error", "Requested banking resource not found."),
        ("Warning", "Unexpected system crash due to unhandled null pointer error."),
        ("Http Success", "Transaction T5462957 completed without errors."),
        ("HTTP Error", "Page redirection to updated banking portal."),
        ("HTTP Error", "Login failed due to incorrect credentials."),
        ("HTTP Error", "Invalid request structure detected."),
        ("Maintenance", "Maintenance window extended due to unexpected issues."),
        ("Access Control Violation", "Unauthorized access attempt on SSH port 22 detected.."),
        ("Email Failure", "Invalid email template detected during notification dispatch."),
    ]

    for log_type, log_message in test_cases:
        label = classify_logs(log_type, log_message)
        print(f"Type: {log_type}, Message: {log_message} -> Classified As: {label}")
