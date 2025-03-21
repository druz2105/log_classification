# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def get_account_id_by_email():
    url = f"https://{JIRA_DOMAIN}/rest/api/3/user/search?query={JIRA_EMAIL}"
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200 and response.json():
        return response.json()[0]["accountId"]  # Get the first matching user
    else:
        print("Error fetching account ID:", response.json())
        return None


def create_jira_issue(criticality, log_type, log_message, process):
    account_id = get_account_id_by_email()
    payload = {
        "fields": {
            "project": {
                "key": "LCL"
            },
            "issuetype": {
                "name": "Error"
            },
            "summary": f"[{criticality}] {log_type} issue detected in process {process}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": log_message
                            }
                        ]
                    }
                ]
            },
            "priority": {
                "name": "Highest" if criticality == "Critical" else "High" if criticality == "High" else "Medium"
            }
        }
    }
    if account_id:
        payload["fields"]["assignee"] = {"accountId": account_id}
    print(payload)
    response = requests.request(
        "POST",
        url=f"https://{JIRA_DOMAIN}/rest/api/3/issue",
        json=payload,  # Use `json` instead of `data` to ensure proper JSON encoding
        headers=headers,
        auth=auth
    )

    return response.json()
