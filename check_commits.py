import requests
from datetime import datetime, timedelta

def get_last_commit_timestamp(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    
    # Send a request to the GitHub API to get the commits
    response = requests.get(url)
    
    if response.status_code == 200:
        # Get the timestamp of the last commit
        last_commit_timestamp = response.json()[0]['commit']['author']['date']
        return last_commit_timestamp
    else:
        print(f"Failed to fetch commits. Status code: {response.status_code}")
        return None

def check_for_new_commits(repo_owner, repo_name, days_threshold=1):
    # Get the timestamp of the last commit
    last_commit_timestamp = get_last_commit_timestamp(repo_owner, repo_name)
    
    if last_commit_timestamp:
        last_commit_date = datetime.strptime(last_commit_timestamp, "%Y-%m-%dT%H:%M:%SZ")
        threshold_date = datetime.utcnow() - timedelta(days=days_threshold)
        
        if last_commit_date >= threshold_date:
            print("New commits found!")
        else:
            print("No new commits.")
    else:
        print("Failed to get last commit timestamp.")

if __name__ == "__main__":
    # Replace 'your_username' and 'your_repository' with your GitHub username and repository name
    repo_owner = 'YogeshShejul2023'
    repo_name = 'cicd_project'
    
    check_for_new_commits(repo_owner, repo_name)
