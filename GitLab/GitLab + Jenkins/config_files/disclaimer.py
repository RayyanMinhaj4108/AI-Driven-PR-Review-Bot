import requests
import os

GITLAB_API_TOKEN = os.getenv('GITLAB_API_TOKEN')  
GITLAB_PROJECT_ID = os.getenv('GITLAB_TARGET_PROJECT_ID')
MERGE_REQUEST_IID = os.getenv('GITLAB_MERGE_REQUEST_ID')

comment = "### Welcome to `SparklingCleanCode.com`, your automated AI PR Reviewing bot! \nYour report is being generated please wait... \n> **DISCLAIMER: GPT 4o MINI only has the capability to process 128k tokens for both input and output. If the Pull Request exceeds the limit by being too large, it will not be processed through AI and the results will be unreliable!**"


url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/merge_requests/{MERGE_REQUEST_IID}/notes"


headers = {
    "Private-Token": GITLAB_API_TOKEN,
    "Content-Type": "application/json"
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
