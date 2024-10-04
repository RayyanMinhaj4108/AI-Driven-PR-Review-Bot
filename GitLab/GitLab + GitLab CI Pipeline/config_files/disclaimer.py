import requests
import os

GITLAB_API_URL = os.getenv('CI_API_V4_URL')  # GitLab API v4 URL
PRIVATE_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN')  # Personal access token (use CI_JOB_TOKEN if available)
PROJECT_ID = os.getenv('CI_PROJECT_ID')  # Project ID
MERGE_REQUEST_IID = os.getenv('CI_MERGE_REQUEST_IID')  # Merge Request IID

comment = "### Welcome to `SparklingCleanCode.com`, your automated AI PR Reviewing bot! \nYour report is being generated please wait... \n> **DISCLAIMER: GPT 4o MINI only has the capability to process 128k tokens for both input and output. If the Pull Request exceeds the limit by being too large, it will not be processed through AI and the results will be unreliable!**"


url = f'{GITLAB_API_URL}/projects/{PROJECT_ID}/merge_requests/{MERGE_REQUEST_IID}/notes'


headers = {
    'PRIVATE-TOKEN': PRIVATE_TOKEN,
    'Content-Type': 'application/json'
}


data = {
    "body": comment
}


response = requests.post(url, headers=headers, json=data)


if response.status_code == 201:
    print("Comment posted successfully!")
else:
    print(f"Failed to post comment. Status code: {response.status_code}")
    print(f"Response: {response.text}")
