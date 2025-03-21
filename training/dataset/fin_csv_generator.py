import random

import pandas as pd
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Number of rows
num_rows = 100000

error_messages = {
    "200": [
        (f"User User{random.randint(1, 1000000)} logged in successfully.", ["Web Server"], ["Low"]),
        (f"User User{random.randint(1, 1000000)} logged out successfully.", ["Web Server"], ["Low"]),
        (f"Payment Session P{random.randint(1000000, 10000000)} Closed Successfully.", ["Payment Gateway"], ["Low"]),
        (f"Transaction T{random.randint(1000000, 10000000)} completed without errors.", ["Web Server"], ["Low"]),
        (f"Payment Session P{random.randint(1000000, 10000000)} initiated for authenticated user.", ["Payment Gateway"],
         ["Low"])
    ],
    "201": [
        ("New account created successfully.", ["Web Server"], ["Low"]),
        (f"Transaction T{random.randint(1000000, 10000000)} confirmation received.", ["Payment Gateway"], ["Low"]),
        (f"Transaction T{random.randint(1000000, 10000000)} completed and recorded.", ["Database Server"], ["Low"]),
        (f"User User{random.randint(1, 1000000)} registration successful.", ["Web Server"], ["Low"]),
        (f"Profile User{random.randint(1, 1000000)} updated successfully.", ["Web Server"], ["Low"])
    ],
    "301": [
        ("Resource moved permanently to a new URL.", ["Load Balancer"], ["Low"]),
        ("Redirection successful for secure login.", ["Web Server"], ["Low"]),
        ("Page redirection to updated banking portal.", ["Load Balancer"], ["Low"]),
        ("Redirection to new payment endpoint successful.", ["Load Balancer"], ["Low"])
    ],
    "400": [
        ("Invalid transaction request syntax.", ["Load Balancer"], ["High"]),
        ("Incorrect input data for account lookup.", ["Database Server"], ["High"]),
        ("Payment submission format error.", ["Payment Gateway"], ["High"]),
        ("Invalid request structure detected.", ["Web Server"], ["High"]),
        ("Malformed API request in banking system.", ["Payment Gateway"], ["High"])
    ],
    "401": [
        ("Unauthorized access attempt to sensitive data.", ["Firewall"], ["Critical"]),
        ("Login failed due to incorrect credentials.", ["Web Server"], ["Medium"]),
        ("Unauthorized request for fund transfer API.", ["Firewall", "Payment Gateway"], ["Critical"]),
        ("Security token missing in authentication process.", ["Web Server"], ["Medium"]),
        ("Unauthorized API key used for customer data retrieval.", ["Firewall"], ["Critical"])
    ],
    "403": [
        ("Unauthorized access attempt detected from unknown IP.", ["Firewall"], ["Critical"]),
        ("Multiple failed login attempts detected.", ["Web Server"], ["High", "Critical"]),
        ("Potential brute force attack identified.", ["Firewall"], ["Critical"]),
        ("Suspicious access attempt using expired credentials.", ["Web Server"], ["High"])
    ],
    "404": [
        ("Requested banking resource not found.", ["Load Balancer"], ["Medium"]),
        ("Account details endpoint unavailable.", ["Load Balancer"], ["Medium"]),
        ("Transaction history page missing.", ["Web Server"], ["Medium"]),
        ("Invalid URL for credit card statement lookup.", ["Load Balancer"], ["Medium"]),
    ],
    "500": [
        ("SyntaxError: Invalid syntax in payment processing module.", ["Payment Gateway"], ["High", "Medium"]),
        ("IndentationError: Incorrect indentation in transaction_logic.", ["Payment Gateway"], ["Medium"]),
        ("NameError: Variable 'account_balance' not defined in fund transfer function.", ["Payment Gateway"],
         ["Medium"]),
        ("ValueError: Invalid credit card number format in payment gateway.", ["Payment Gateway"], ["Critical"]),
        ("TypeError: Unsupported operand type in balance calculation.", ["Payment Gateway", "Database Server"],
         ["High"]),
        ("ZeroDivisionError: Division by zero in interest rate calculation.", ["Payment Gateway", "Web Server"],
         ["Medium"]),
        ("FileNotFoundError: Missing encryption key file for secure data transfer.", ["Web Server"],
         ["Critical"]),
        (
            "ModuleNotFoundError: Missing security module for authentication logic.", ["Web Server"],
            ["Critical", "High"]),
        ("MemoryError: Out of memory during high transaction load.", ["Database Server"], ["Medium"]),
        ("PermissionError: Insufficient permissions for accessing critical banking files.", ["Database Server"],
         ["Critical"]),
        ("Deadlock detected in concurrent transaction processing.", ["Database Server"], ["High"]),
        ("Corrupted data block found in transaction logs.", ["Payment Gateway"], ["High", ]),
        ("Uncaught recursion error in interest calculation logic.", ["Payment Gateway", "Web Server"],
         ["High"]),
        ("Timeout error in secure socket layer (SSL) handshake.", ["Payment Gateway"], ["High", "Critical"]),
        ("Critical error in credit score verification module.", ["Payment Gateway"], ["Critical"]),
    ],
    "TIMEOUT": [
        ("Timeout error during API request processing.", ["Load Balancer"], ["High", "Medium"]),
        ("Transaction timeout detected in payment module.", ["Payment Gateway"], ["Critical", "High"]),
        ("Banking system request timeout in customer authentication.", ["Web Server"], ["High", "Medium"]),
        ("Timeout error in secure data encryption service.", ["Database Server"], ["High", "Critical"])
    ],
    "DB_CONN_FAIL": [
        ("Database connection failure detected during transaction processing.", ["Database Server"], ["Critical"]),
        ("Banking data retrieval timeout error.", ["Database Server"], ["High", "Critical"]),
        ("Core database system temporarily unreachable.", ["Database Server"], ["Critical"])
    ],
    "NULL_POINTER": [
        ("Null pointer exception detected in transaction processing logic.", ["Payment Gateway"], ["High", "Medium"]),
        ("Critical banking data reference missing in core module.", ["Database Server"], ["Critical"]),
        ("Unexpected system crash due to unhandled null pointer error.", ["Web Server"], ["Critical", "High"])
    ],
    "MAINT_1000": [
        ("Scheduled maintenance started on database servers.", ["Database Server"], ["Low"]),
        ("System update in progress for web servers.", ["Web Server"], ["Low"]),
        ("Backup process initiated for transaction logs.", ["Database Server"], ["Medium"]),
        ("Security patch installation started.", ["Firewall"], ["Medium"])
    ],
    "MAINT_1001": [
        ("Completion of database optimization task.", ["Database Server"], ["Low"]),
        ("Web server update completed successfully.", ["Web Server"], ["Low"]),
        ("Security update deployment finished.", ["Firewall"], ["Medium"]),
        ("Maintenance task completed ahead of schedule.", ["Database Server"], ["Low"])
    ],
    "MAINT_1002": [
        ("Unscheduled maintenance required for critical systems.", ["Database Server"], ["Critical"]),
        ("Emergency patch applied to payment gateway.", ["Payment Gateway"], ["High"]),
        ("Temporary downtime for system upgrade.", ["Web Server"], ["Medium"])
    ],
    "MAINT_1003": [
        ("Maintenance window extended due to unexpected issues.", ["Database Server"], ["High"]),
        ("Rollback of updates due to stability concerns.", ["Web Server"], ["High"])
    ],
    "25": [
        ("SMTP connection failure while sending email notifications.", ["Email Service"], ["Critical"]),
        ("SMTP port timeout (port 25) during email transmission.", ["Email Service"], ["High", "Critical"]),
        ("SMTP port 25 connection refused.", ["Email Service"], ["Critical"])
    ],
    "110": [
        ("POP connection failure while retrieving emails.", ["Email Service"], ["Critical"]),
        ("POP3 port 110 connection failure.", ["Email Service"], ["Critical"]),
        ("POP3 authentication failure on port 110.", ["Email Service"], ["Critical"])
    ],
    "587": [
        ("Failed to connect to SMTP server on alternate port 587.", ["Email Service"], ["Critical"])
    ],
    "334": [
        ("Email delivery failure due to invalid recipient address.", ["Email Service"], ["High", "Medium"]),
        ("Email timeout during batch processing of notifications.", ["Email Service"], ["Medium", "High"]),
        ("Invalid email template detected during notification dispatch.", ["Email Service"], ["Medium", "Low"]),
        ("Failure to send email alert for suspicious activity detected.", ["Email Service"], ["Critical"]),
        ("Authentication failure with email server.", ["Email Service"], ["Critical"]),
        ("Email queue overflow causing delayed notifications.", ["Email Service"], ["High", "Medium"]),
        ("SMTP server rejecting email due to blacklisting.", ["Email Service"], ["Critical"]),
        ("POP3 server rejecting connections due to overload.", ["Email Service"], ["High", "Critical"]),
        ("SMTP server certificate validation error.", ["Email Service"], ["High", "Critical"]),
        ("POP3 server certificate validation error.", ["Email Service"], ["High", "Critical"]),
        ("Delayed email delivery due to SMTP queue backlogs.", ["Email Service"], ["High", "Medium"])
    ],
    "22": [
        ("SSH connection failed due to network timeout.", ["VPN Server"], ["High"]),
        ("Port 22 connection refused by remote host.", ["VPN Server"], ["Critical"]),
        ("Unauthorized access attempt on SSH port 22 detected.", ["Firewall", "VPN Server"], ["Critical"]),
        ("SSH handshake failure during authentication.", ["VPN Server"], ["High"]),
        ("Unrecognized SSH protocol version on port 22.", ["VPN Server"], ["Medium"]),
        ("Excessive SSH login attempts detected on port 22.", ["Firewall", "VPN Server"], ["Critical"])
    ]
}
process_ip_mapping = {
    "Web Server": "192.168.1.10",
    "Payment Gateway": "192.168.1.20",
    "Database Server": "192.168.1.30",
    "Load Balancer": "192.168.1.40",
    "Firewall": "192.168.1.50",
    "Email Service": "192.168.1.60",
    "VPN Server": "192.168.1.70"
}


def get_destination_ip(process):
    return process_ip_mapping.get(process, fake.ipv4_private())


# Possible log types and their distribution
log_types = [
    "Http Success", "HTTP Error", "Security Breach", "System Failure", "Maintenance", "Warning"
]

# Error codes with weighted distribution
error_codes = ["200", "201", "301", "400", "401", "403", "404", "500", "DB_CONN_FAIL", "TIMEOUT", "NULL_POINTER",
               "MAINT_1000", "MAINT_1001", "MAINT_1002", "MAINT_1003", "25", "110", "587", "334",
               "22"]

error_weights = [
    1, 1, 1, 1, 1, 1, 1, 1,  # Common HTTP errors
    0.2, 0.2, 0.2,  # Database & timeout errors
    0.02, 0.02, 0.02, 0.02,  # Maintenance logs
    0.001, 0.001, 0.001, 0.001,  # Email-logs
    0.005,  # VPN-logs
]


def generate_message_and_log_type(error_code):
    if error_code in error_messages:
        message, processes, severities = random.choice(error_messages[error_code])

        process = random.choice(processes)
        severity = random.choice(severities)

        if error_code in ["200", "201"]:
            log_type = "Http Success"
        elif error_code in ["301", "400", "401", "404", "TIMEOUT"]:
            log_type = "HTTP Error"
        elif error_code in ["403"]:
            log_type = "Security Breach" if process == "Firewall" else "HTTP Error"
        elif error_code in ["500"]:
            log_type = "System Failure"
        elif error_code == "DB_CONN_FAIL":
            log_type = "System Failure"
        elif error_code == "NULL_POINTER":
            log_type = "Warning"
        elif error_code.startswith("MAINT"):
            log_type = "Maintenance"
        elif error_code == "22":  # VPN error
            log_type = "Access Control Violation"
        elif error_code in ["25", "110", "587", "334"]:  # Email errors
            log_type = "Email Failure"
        else:
            log_type = random.choices(log_types, weights=[1, 1, 1, 1, 0, 0])[0]

        return message, process, log_type, severity
    else:
        raise ValueError(f"Invalid error code: {error_code}")


def validate_source_ip(process, source_ip):
    if process == "Payment Gateway":
        expected_ip = process_ip_mapping["Load Balancer"]
    elif process == "Database Server":
        expected_ip = process_ip_mapping["Web Server"]
    else:
        return True  # No validation for other processes

    return source_ip == expected_ip


# Generate dataset
data = []

for _ in range(num_rows):
    code = random.choices(error_codes, weights=error_weights)[0]
    message, process, log_type, severity = generate_message_and_log_type(code)

    # Introduce 1 in 1,000 chance of a fake source IP
    if random.randint(1, 1000) == 1:  # 1 in 1,000 probability
        source_ip = fake.ipv4()  # Generate a fake IP
    else:
        # Use the expected IP for the process
        if process == "Payment Gateway":
            source_ip = process_ip_mapping["Load Balancer"]
        elif process == "Database Server":
            source_ip = process_ip_mapping["Web Server"]
        else:
            source_ip = fake.ipv4()  # Random IP for other processes

    dest_ip = get_destination_ip(process)

    # Validate source IP
    if not validate_source_ip(process, source_ip):
        code = "TIMEOUT"
        message = f"Unauthorized attempt to access service by {source_ip}."
        log_type = "Security Breach"
        severity = "Critical"

    data.append({
        "timestamp": fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
        "error_code": code,
        "message": message,
        "log_type": log_type,
        "severity": severity,
        "source_ip": source_ip,
        "destination_ip": dest_ip,
        "process": process
    })

# Create DataFrame
df = pd.DataFrame(data)

# Sort dataset by timestamp for realistic log flow
df.sort_values(by="timestamp", inplace=True)

# Export to CSV
file_path = "banking_finance_logs.csv"
df.to_csv(file_path, index=False)
print(f"File successfully converted: {file_path}")
