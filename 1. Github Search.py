"""
This script demonstrates how to search for GitHub repositories using the GitHub API,
fetch their metadata, calculate date differences (such as time elapsed between
creation and last update), and store results in separate output files for further analysis.
"""
import requests
import json
import os
import base64
from datetime import datetime
# Fetch the complete README content of a repository
# !!!!
# !!!!
# USE YOUR TOKEN
# !!!!
# !!!!
token = ""
def fetch_readme(repo_full_name, headers):
    """Fetch the complete README content of a repository"""
    url = f'https://api.github.com/repos/{repo_full_name}/readme'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        readme_data = response.json()
        if 'content' in readme_data:
            content = base64.b64decode(readme_data['content']).decode('utf-8', errors='ignore')
            return content
    return ""

# Calculate the difference between two dates (returns the number of days)
def calculate_date_difference(date1, date2):
    """Calculate the difference between two dates (returns the number of days)"""
    dt1 = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%SZ")
    dt2 = datetime.strptime(date2, "%Y-%m-%dT%H:%M:%SZ")
    return (dt1 - dt2).days

# GitHub search API: Retrieve repositories based on a query
def search_github_repositories(query, token=None):
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    repositories = []
    per_page = 100  # Maximum number of items per page
    max_pages = 10  # GitHub search API returns up to 1000 results (100 items * 10 pages)

    for page in range(1, max_pages + 1):
        url = f'https://api.github.com/search/repositories?q={query}&per_page={per_page}&page={page}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])
            if not repos:
                break
            for idx, repo in enumerate(repos, start=(page - 1) * per_page + 1):
                readme_content = fetch_readme(repo.get("full_name"), headers)
                updated_created_diff = calculate_date_difference(repo["updated_at"], repo["created_at"])
                pushed_created_diff = calculate_date_difference(repo["pushed_at"], repo["created_at"])
                repositories.append({
                    "id": idx,
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description", "No description"),
                    "created_at": repo.get("created_at"),
                    "updated_at": repo.get("updated_at"),
                    "pushed_at": repo.get("pushed_at"),
                    "updated_created_diff": updated_created_diff,
                    "pushed_created_diff": pushed_created_diff,
                    "language": repo.get("language"),
                    "watchers": repo.get("watchers"),
                    "html_url": repo.get("html_url"),
                    "forks": repo.get("forks"),
                    "stargazers_count": repo.get("stargazers_count"),
                    "topics": repo.get("topics", []),
                    "readme": readme_content  # Complete README content
                })
            print(f'Retrieved {len(repos)} repositories from page {page}.')
            if len(repos) < per_page:
                break  # End of results
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            break

    # Create top-level 'raw_data' folder and subfolders
    raw_data_path = 'raw_data'
    output_path = os.path.join(raw_data_path, 'GITHUB_OUTPUT')
    age_path = os.path.join(raw_data_path, 'GITHUB_AGE')
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(age_path, exist_ok=True)

    # Save detailed repository information to separate files
    for repo in repositories:
        # Output to 'github_output' folder
        repo_filename = os.path.join(output_path, f"{repo['id']}_{repo['full_name'].replace('/', '_')}.txt")
        with open(repo_filename, 'w', encoding='utf-8') as f:
            f.write(
                f"ID: {repo['id']}\n"
                f"Full Name: {repo['full_name']}\n"
                f"Description: {repo['description']}\n"
                f"Created At: {repo['created_at']}\n"
                f"Updated At: {repo['updated_at']}\n"
                f"Pushed At: {repo['pushed_at']}\n"
                f"Language: {repo['language']}\n"
                f"URL: {repo['html_url']}\n"
                f"Forks: {repo['forks']}\n"
                f"Stars: {repo['stargazers_count']}\n"
                f"Topics: {', '.join(repo['topics'])}\n"
                f"README:\n{repo['readme']}\n"
            )

        # Output to 'github_age' folder
        age_filename = os.path.join(age_path, f"{repo['id']}_{repo['full_name'].replace('/', '_')}.txt")
        with open(age_filename, 'w', encoding='utf-8') as f:
            f.write(
                f"Full Name: {repo['full_name']}\n"
                f"Updated - Created (days): {repo['updated_created_diff']} days\n"
                f"Pushed - Created (days): {repo['pushed_created_diff']} days\n"
            )

    print(f"Saved details of {len(repositories)} repositories to the 'github_output' folder under 'raw_data'.")
    print(f"Saved update and push date differences to the 'github_age' folder under 'raw_data'.")

if __name__ == '__main__':
    query = input('Enter search keyword: ')

    search_github_repositories(query, token)
