import os
import requests
import subprocess
import shutil
from git import Repo
from importlib.machinery import SourceFileLoader
credentials = SourceFileLoader("credentials", "credentials.py").load_module()
owner = credentials.owner
repo = credentials.repo
branch = credentials.branch
local_repo_path = credentials.local_repo_path
access_token = credentials.access_token
nginx_path = '/var/www/html/'
# API request headers
headers = {
    'Authorization': f'Bearer {access_token}'
}
# API URL to get latest commit
url = f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}'
response = requests.get(url, headers=headers)
if response.status_code == 200:
    latest_commit_hash = response.json()['commit']['sha']
else:
    print("Error fetching commit hash:", response.text)
    latest_commit_hash = None
# Check if there's a new commit
previous_commit_hash_file = '84d3df4a5fa1e609dfa5a7775522fb427fb4d82'
if os.path.exists(previous_commit_hash_file):
    with open(previous_commit_hash_file, 'r') as file:
        previous_commit_hash = file.read().strip()
else:
    previous_commit_hash = None
if latest_commit_hash and latest_commit_hash != previous_commit_hash:
    print("New commit detected:", latest_commit_hash)
    #method 1: using the bash script to clone the repo to ngnix folder
    subprocess.run(["bash","/home/ubuntu/ci_cd_pipeline/DeployScript.sh"])
    #Method 2 : check if the repo is already there if not then clone it.
    # Clone or pull the repository
    if os.path.exists(local_repo_path):
        repo = Repo(local_repo_path)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(f'https://github.com/{owner}/{repo}.git', local_repo_path)
    # Check if index.html has changed
    if repo.git.diff(previous_commit_hash, latest_commit_hash, '--', file_to_copy):
        src_path = os.path.join(local_repo_path, file_to_copy)
        dest_path = os.path.join(nginx_path, file_to_copy)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            print("Copied index.html to Nginx folder.")
    else:
        print("No changes in index.html.")
    # Update the previous commit hash
    with open(previous_commit_hash_file, 'w') as file:
        file.write(latest_commit_hash)
else:
    print("No new commits.")