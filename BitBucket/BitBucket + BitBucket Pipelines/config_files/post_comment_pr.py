import os
import requests
import json
from openai import Client

key = os.getenv("OPENAI_API_KEY")


client = Client(api_key=key)

def read_file(file_path):
    with open(file_path, 'r+') as file:
        file.readline()
        content = file.read()
        file.seek(0)
        file.write(content)
        file.truncate()
        return content


def generate_report(before_file, after_file):
    before_content = read_file(before_file)
    after_content = read_file(after_file)


    prompt = f"""You are an AI code reviewer. Given two versions of code, the old code and the new code, please analyze the changes between them. 
For any line that has been added in the new code (compared to the old code) that you think would potentially cause an issue, generate a detailed comment on the change, only if it might be harmful, or any suggestions for improvement.
The response should be in a structured format that includes the following fields for each added line:

- "from": The comment's anchor line in the old version of the file. (Minimum 1)
- "to": The comment's anchor line in the new version of the file. If the 'from' line is also provided, this value will be removed. (Minimum 1)
- "comment": the generated review comment.


here is the old code: {before_content}
here is the new code: {after_content}

DO NOT MAKE IT IN JSON FORMAT
ONLY MAKE COMMENTS ON LINES WHERE YOU IDENTIFY SEVERE ISSUES.
---
EXAMPLE
from: 14
to: 45
comment: your comment about the added line and its affects

from: 4
to: 6
comment: your comment about the added line and its affects

from: 3
to: 2
comment: your comment about the added line and its affects

"""
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "assistant", "content": [{"type": "text", "text": prompt}]}],
        max_tokens=3000,
        temperature=0.1,
        top_p=1.0
    )
    
    
    content = response.choices[0].message.content
        
    return content

if __name__ == "__main__":
    
    import sys
    before_file = sys.argv[1]
    after_file = sys.argv[2]
    
    resp = generate_report(before_file, after_file)
    
    comments_lines = resp.strip().split("\n\n")
    comments = []
    
    for comment_block in comments_lines:
        lines = comment_block.strip().split("\n")
 
        if len(lines) < 3 or ":" not in lines[0] or ":" not in lines[1] or ":" not in lines[2]:
            print(f"Skipping malformed comment block: {comment_block}")
            continue
    
        from_line = int(lines[0].split(": ")[1])
        to_line = int(lines[1].split(": ")[1])
        comment_text = lines[2].split(": ", 1)[1]
    
        comments.append({
            "from": from_line,
            "to": to_line,
            "comment": comment_text,
            "path": "test.py"  
        })
    
    
    workspace = os.getenv("BITBUCKET_WORKSPACE")
    repo_slug = os.getenv("BITBUCKET_REPO_SLUG")
    pr_id = os.getenv("BITBUCKET_PR_ID")
    access_token = os.getenv("SPARKLE_BOT_AT")
    
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/comments"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    for comment in comments:
        payload = {
            "content": {
                "raw": comment["comment"]
            },
            "inline": {
                "from": comment["from"],
                "to": comment["to"],
                "path": comment["path"]
            }
        }
    
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            print(f"Comment posted for lines {comment['from']} to {comment['to']}: {comment['comment']}")
        else:
            print(f"Failed to post comment for lines {comment['from']} to {comment['to']}. Error: {response.text}")
    