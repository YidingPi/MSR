""""Software Heritage Search and GitHub Repository Data Processing Program

This program performs the following tasks:
1. Searches the Software Heritage (SWH) archive for repositories matching a specified URL pattern.
2. Extracts GitHub URLs from the search results and saves them to a file.
3. Retrieves repository metadata from GitHub, including detailed information such as README content, creation dates,
   activity metrics, language, and repository stats.
4. Calculates and stores additional metrics (e.g., date differences).
5. Saves valid and error details separately for further analysis.

This program is designed to aid in analyzing repository data across platforms for research or development purposes.
"""
import requests
import os
import base64
from datetime import datetime
# !!!!
# !!!!
# USE YOUR TOKEN
# !!!!
# !!!!
# GitHub token for authentication
# GitHub token for authentication
tokengithub=""
# Software Heritage token for authentication
tokenswh = ""
prefix = "https://github.com/"
TOKEN = tokenswh

idxy=0
counterror=0
countgit=0

# Ensure all directories are created at the start
output_dirs = [
    os.path.join('refined_data', 'SWH_OUTPUT'),
    os.path.join('refined_data', 'SWH_AGE'),
    os.path.join('refined_data', 'SWH_INVALID'),
    os.path.join('raw_data', 'SWH_URLs')
]

for dir_path in output_dirs:
    os.makedirs(dir_path, exist_ok=True)
    print(f"Ensured directory exists: {dir_path}")
def fetch_readme(repo_full_name, headers):
    """get readme information"""
    urlf = f'https://api.github.com/repos/{repo_full_name}/readme'
    response = requests.get(urlf, headers=headers)
    if response.status_code == 200:
        readme_data = response.json()
        if 'content' in readme_data:
            content = base64.b64decode(readme_data['content']).decode('utf-8', errors='ignore')
            return content
    return "" #not found or error


def calculate_date_difference(date1, date2):
    """Calculate age"""
    dt1 = datetime.strptime(date1, "%Y-%m-%dT%H:%M:%SZ")
    dt2 = datetime.strptime(date2, "%Y-%m-%dT%H:%M:%SZ")
    return (dt1 - dt2).days


def search_github_repositories(newurl, token=None):
    global countgit
    global idxy
    global counterror
    countgit=countgit+1
    # Create output folders
   # os.makedirs(os.path.join('raw_data','swhgithub_output'), exist_ok=True)
   # os.makedirs(os.path.join('raw_data','swhgithub_age'), exist_ok=True)
  # os.makedirs(os.path.join('raw_data','swhgithub_error'), exist_ok=True)

    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    repositories = []
    idxy=idxy+1
    # Fetch repository details
    url = f'https://api.github.com/repos/{newurl}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo = response.json()

        # Fetch README content
        readme_content = fetch_readme(repo.get("full_name"), headers)

        # Calculate date differences
        updated_created_diff = calculate_date_difference(repo["updated_at"], repo["created_at"])
        pushed_created_diff = calculate_date_difference(repo["pushed_at"], repo["created_at"])
        # Add repository details to the list
        repositories.append({
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
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        error_filename = os.path.join('refined_data\SWH_INVALID', f"{idxy}_{newurl.replace('/', '_')}.txt")

        with open(error_filename, 'w', encoding='utf-8') as fw:
            fw.write(newurl)
            fw.write("\n")
            fw.write(f"Error: {response.status_code} - {response.reason}")
            counterror=counterror+1
            fw.write("\n")



    # Save each repository's details
    for idx, repo in enumerate(repositories):
        # Output to output folder
        repo_filename = os.path.join('refined_data','SWH_OUTPUT', f"{idxy}_{repo['full_name'].replace('/', '_')}.txt")
        with open(repo_filename, 'w', encoding='utf-8') as f:
            f.write(
                #f"ID: {idx}\n"
                f"Full Name: {repo['full_name']}\n"
                f"Description: {repo['description']}\n"
                f"created_at: {repo['created_at']}\n"
                f"updated_at: {repo['updated_at']}\n"
                f"pushed_at: {repo['pushed_at']}\n"
                f"Language: {repo['language']}\n"
                f"URL: {repo['html_url']}\n"
                f"Forks: {repo['forks']}\n"
                f"Stars: {repo['stargazers_count']}\n"
                f"Topics: {', '.join(repo['topics'])}\n"
                f"README:\n{repo['readme']}\n"
            )

        # Output to age folder
        age_filename = os.path.join('refined_data','SWH_AGE', f"{idxy}_{repo['full_name'].replace('/', '_')}.txt")
        with open(age_filename, 'w', encoding='utf-8') as f:
            f.write(
                f"Full Name: {repo['full_name']}\n"
                f"Updated - Created (days): {repo['updated_created_diff']} days\n"
                f"Pushed - Created (days): {repo['pushed_created_diff']} days\n"
            )

    print(f"Saved {len(repositories)} repository details to 'swhgithub_output' and 'swhgithub_age'.")
# def read_urls(filename):
#     #idx=0
#     urls = []
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             if line.startswith('metadata_authorities_url:'):
#                 url = line.strip().split('metadata_authorities_url:')[1].strip()
#                 urls.append(url)
#             if line.startswith('https://github.com/'):
#                 url1 = line.strip().split('url:')[1].strip()
#                 print("url1")
#                 print(url1)
#                 if url1.startswith(prefix):
#                     # 删除前缀部分
#                     new_url = url1[len(prefix):]
#                     print("new_url")
#                     print(new_url)
#                 else:
#                     print("URL不包含指定的前缀。")
#                 #idx=idx+1
#                 search_github_repositories(new_url, tokengithub)
#                 print("url1")
#                 print(url1)
#                 #urls.append(url)
#     return urls

def read_urls():
    filename=os.path.join('raw_data','SWH_URLs','Urls_Results.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            # delete prefix of url
            if url.startswith(prefix):
                new_url = url[len(prefix):]
                print("Processed URL:", new_url)
                search_github_repositories(new_url, tokengithub)
            else:
                print("URL does not contain the specified prefix:", url)

def fetch_data(urls, token):
    headers = {'Authorization': f'Bearer {token}'}
    results = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            results.append(response.text)
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            results.append(f"Error fetching {url}: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
            results.append(f"Error fetching {url}: {err}")
    return results

#def write_output(data, output_filename):
    # with open(output_filename, 'w', encoding='utf-8') as file:
    #     for item in data:
    #         file.write(item + '\n')


def search_swh_origin(url_pattern, limit=10, with_visit=True, visit_type=None):
    """
    Search for software origins in Software Heritage archive.

    :param url_pattern: The string pattern to search in origin URLs, separated by /.
    :param limit: The maximum number of results to return (bounded to 1000).
    :param with_visit: If True, only return origins with at least one visit.
    :param visit_type: Filter by specific visit type (e.g., 'git', 'pypi').
    :return: A list of search results or an error message.
    """
    base_url = f"https://archive.softwareheritage.org/api/1/origin/search/{url_pattern}/"
    params = {
        "limit": limit,
        "with_visit": str(with_visit).lower()
    }
    if visit_type:
        params["visit_type"] = visit_type

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"  # 使用Bearer令牌
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def save_github_urls(results, output_file="Urls_Results.txt"):
    """
    Save GitHub URLs from the search results to a file.
    """
    if "error" in results:
        print(f"Error: {results['error']}")
        return

    if not results:
        print("No results found.")
        return


    output_dir = "raw_data/SWH_URLs"
    os.makedirs(output_dir, exist_ok=True)
    output_file2 = "Urls_Counter.txt"
    # file path
    output_path = os.path.join(output_dir, output_file)
    output_path2=os.path.join(output_dir, output_file2)
    github_urls = []
    for result in results:  # Iterate directly over the list of results
        url = result.get("url", "")
        if "github.com" in url:  # Filter only GitHub URLs
            github_urls.append(url)

    # Save URLs to a file
    with open(output_path, "w") as file:
        for url in github_urls:
            file.write(url + "\n")

    with open(output_path2, "w") as file:
        file.write(f"{len(github_urls)}")


    print(f"Saved {len(github_urls)} GitHub URLs to {output_path}.")

if __name__ == "__main__":
    print("Software Heritage Search Program")
    url_pattern = input("Enter the Search Keyword: ").strip()

    # Check if URL pattern is empty
    if not url_pattern:
        print("Warning: URL pattern is required. Please provide a valid input.")
    else:
        #limit = int(input("Enter the maximum number of results to retrieve (default 1000): ") or 1000)
        #with_visit = input("Filter only origins with visits? (yes/no, default yes): ").strip().lower() != "no"
        #visit_type_input = input(
       #     "Enter visit type to filter by (default 'git', or type 'None' for no filtering): "
        #    "(supported types are git, pypi, deb, cran, tar, npm, content, golang, maven...): "
       # ).strip()
        limit = 1000
        with_visit = 1
        visit_type = "git"

        print("\nSearching...\n")
        results = search_swh_origin(url_pattern, limit, with_visit, visit_type)
        save_github_urls(results)
        urls = read_urls()
        # data = fetch_data(urls, tokenswh)
        # write_output(data, 'raw-extrinsic-metadata.txt')

        print("The data has been written to the file.")
        print(counterror)
        percentage = (counterror / countgit) * 100

        # invalid percentage
        print(f"{percentage:.2f}%")
        os.makedirs(os.path.join('refined_data', 'SWH_VALID_COUNTER'), exist_ok=True)
        error_filename = os.path.join('refined_data', 'SWH_VALID_COUNTER', f"counter.txt")
        with open(error_filename, 'w', encoding='utf-8') as fw:
            # fw.write(f"counterror")
            # fw.write("\n")
            fw.write(f"{countgit - counterror}")
