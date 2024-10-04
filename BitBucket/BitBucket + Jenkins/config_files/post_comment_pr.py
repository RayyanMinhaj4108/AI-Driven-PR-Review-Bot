import requests
import json
import os

workspace = os.getenv("BITBUCKET_WORKSPACE_SLUG")
repo_slug = os.getenv("BITBUCKET_REPO_SLUG")
pr_id = os.getenv("BITBUCKET_PR_ID")
access_token = os.getenv("BITBUCKET_ACCESS_TOKEN")

with open('PR_report.txt', 'r') as file:
    pr_report_content = file.read()


repo_slug = repo_slug.split('/')[1]  # Extract the slug from the full name

url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/comments"


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Define the payload with the comment variable
payload = {
    "content": {
        "raw": pr_report_content
    }
}

# Convert the payload to JSON
payload_json = json.dumps(payload)

# Make the POST request
response = requests.post(
    url,
    data=payload_json,
    headers=headers
)

# Print the response
print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))