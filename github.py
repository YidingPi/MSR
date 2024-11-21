import requests

#instruction: change 'q' to search different projects
#return 1000 results

# personal token to access
headers = {
    'Authorization': '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',
    'Accept': 'application/vnd.github.v3+json',
}
# search keywords
params = {
    #add search limitation language stars time size topic user in:name in:description in:readme
    #'q': 'language:python stars:>1 created:>2023-01-01 pushed:>2023-06-01 size:<500000 in:name example in:description example in:readme example user:octocat is:public topic:machine-learning',
    #'q': 'language:python stars:>1 created:>2023-01-01 pushed:>2023-06-01 size:<500000 in:name s in:description s in:readme s is:public topic:machine-learning',
    #'q' : 'language:Java',
    'q' : 'language:C++',
    #'q' : 'language:Javascript',
    #'q' : 'language:Python',
    'sort': 'stars',  # use stars to sort
    'order': 'desc', #high to low
    'per_page': 100 #max 100 per page
}
all_repos = [] #store
#per page 100 we get 10 pages
page = 1
while True:
    # limitation #1000
    if(page==10):
        break
    params['page'] = page
    response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params)
    #print(response.json())
    if response.status_code == 200:
        data = response.json()
        if not data['items']:
            break
        all_repos.extend(data['items'])
        page+=1
        #for repo in data['items']:
            #print(f"Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}")
    else:
        print(f"Error: {response.status_code}")
        break
#list selected items
for repo in all_repos:
    print(f"id: {repo['id']}")
    #print(f"node_id: {repo['node_id']}")
    print(f"Name: {repo['name']}")
    #print(f"full_name: {repo['full_name']}")
    print(f"owner: {repo['owner']}")
    print(f"Description: {repo['description']}")
    print(f"Created at: {repo['created_at']}")
    print(f"Updated at: {repo['updated_at']}")
    print(f"Pushed at: {repo['pushed_at']}")
    print(f"Stars: {repo['stargazers_count']}")
    print(f"Forks: {repo['forks_count']}")
    print(f"Open Issues: {repo['open_issues_count']}")
    print(f"Owner: {repo['owner']['login']}")
    print(f"Language: {repo['language']}")
    print(f"Topics: {repo['topics']}")
    print(f"Watchers: {repo['watchers']}")
    print(f"Size: {repo['size']} KB")
    print(f"Default Branch: {repo['default_branch']}")
    print(f"URL: {repo['html_url']}")
    print("-" * 40)
#list all items
#for repo in all_repos:
#    for key, value in repo.items():
#        print(f"{key}: {value}")
#    print("-" * 40)