import re
from utils.groq_client import get_groq_client


def classify_with_llm(log_message):
    prompt = f'''Classify the log message criticality into one of these categories: 
    (1) Low, (2) Medium, (3) High, (4) Critical (5) Unclassified.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category></category> tags. 
    Log message: {log_message}'''

    chat_completion = get_groq_client(prompt)
    content = chat_completion.choices[0].message.content
    match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    category = "Unclassified"
    if match:
        category = match.group(1)

    return category


if __name__ == "__main__":
    print(classify_with_llm("Unauthorized access attempt on SSH port 22 detected."))
    print(classify_with_llm("Maintenance window extended due to unexpected issues."))
