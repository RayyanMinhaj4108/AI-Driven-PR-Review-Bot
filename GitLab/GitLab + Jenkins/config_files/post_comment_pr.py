import requests
import os

GITLAB_API_TOKEN = os.getenv('GITLAB_API_TOKEN')  
GITLAB_PROJECT_ID = os.getenv('GITLAB_TARGET_PROJECT_ID')
MERGE_REQUEST_IID = os.getenv('GITLAB_MERGE_REQUEST_ID')

with open('PR_report.txt', 'r') as file:
    pr_report_content = file.read()


url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/merge_requests/{MERGE_REQUEST_IID}/notes"


headers = {
    "Private-Token": GITLAB_API_TOKEN,
    "Content-Type": "application/json"
}


data = {
    "body": pr_report_content
}


response = requests.post(url, headers=headers, json=data)


if response.status_code == 201:
    print("Comment posted successfully!")
else:
    print(f"Failed to post comment. Status code: {response.status_code}")
    print(f"Response: {response.text}")
