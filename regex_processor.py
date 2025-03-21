import re


def classify_with_regex(message):
    patterns = {
        r"User User\d+ logged (in|out) successfully\.": "Low",
        r"Payment Session P\d{7,} Closed Successfully\.": "Low",
        r"Transaction T\d{7,} completed without errors\.": "Low",
        r"Payment Session P\d{7,} initiated for authenticated user\.": "Low",
        r"New account created successfully\.": "Low",
        r"Transaction T\d{7,} confirmation received\.": "Low",
        r"Transaction T\d{7,} completed and recorded\.": "Low",
        r"User User\d+ registration successful\.": "Low",
        r"Profile User\d+ updated successfully\.": "Low",
        r"Resource moved permanently to a new URL\.": "Low",
        r"Redirection successful for secure login\.": "Low",
        r"Page redirection to updated banking portal\.": "Low",
        r"Redirection to new payment endpoint successful\.": "Low",
    }

    for pattern, category in patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            return category
    return None


if __name__ == "__main__":
    print(classify_with_regex("User User123 logged in successfully."))
    print(classify_with_regex("Payment Session P12345678 Closed Successfully."))
    print(classify_with_regex("Transaction T12345678 completed without errors."))
    print(classify_with_regex("Payment Session P12345678 initiated for authenticated user."))
    print(classify_with_regex("New account created successfully."))
    print(classify_with_regex("Transaction T12345678 confirmation received."))
    print(classify_with_regex("Transaction T12345678 completed and recorded."))
    print(classify_with_regex("User User123 registration successful."))
    print(classify_with_regex("Profile User123 updated successfully."))
    print(classify_with_regex("Multiple failed login attempts detected."))
