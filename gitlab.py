import requests
import json

#instruction: change 'search' to search differnt results
#in the future, the program can add more restrictions to search
#currently, the program will search 2 pages, delete the code, it can search infinite results


token = 'glpat-LLMUoUQ1zCKNewx4yRo1'
headers = {'PRIVATE-TOKEN': token}
# Define search parameters
params = {
    'search': 'python',
    'visibility': 'public',
    'order_by': 'last_activity_at',
    'sort': 'desc',
    'per_page': 100
   # 'owned': 'true'
}
page = 1
all_repos = []
# Search for projects with specific parameters
with open('gitlab_projects_new.json', 'w') as f:
    while True:
        params['page'] = page
        response = requests.get('https://gitlab.com/api/v4/projects', headers=headers, params=params)
        if response.status_code != 200:
            print(f"error: {response.status_code}")
        else:
            projects = response.json()
            if not projects:
                break
            json.dump(projects, f, indent=4) #write to file
            f.write("-" * 40)
            #List all items
            # print(projects)
            for repo in projects:
                for key, value in repo.items():
                    print(f"{key}: {value}")
                print("-" * 40)
            # limit result number, otherwise infinite results
            if(page==2):
                break
            page+= 1
print("The search results have been saved to gitlab_projects.json file.")

# # Get a specific project
# project_id = '<project_id>'
# response = requests.get(f'https://gitlab.com/api/v4/projects/{project_id}', headers=headers)
# project = response.json()
# print(project)
#
# # List repository files
# response = requests.get(f'https://gitlab.com/api/v4/projects/{project_id}/repository/tree', headers=headers)
# files = response.json()
# print(files)
