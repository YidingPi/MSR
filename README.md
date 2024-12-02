
# Description
This repository contains the data, scripts, and documentation for the study "A Study of Repository Characteristics of Search Results from GitHub and Software Heritage Search Tools." The goal of this project is to explore the overlap, metadata differences, and search result relevance of repositories retrieved from GitHub and Software Heritage search tools using the keyword(We use "python" as an example).

# Data Sources
Data Source: GitHub Repositories from Software Heritage API and GitHub API

Example of Software Heritage API: https://archive.softwareheritage.org/api/1/origin/search/python/?limit=1000&?with_visit=1&visit_type=git

Example of GitHub API: https://api.github.com/search/repositories?q=python

Date of Access: December 1, 2024

# Research Questions

RQ1: How many repositories retrieved from Software Heritage are no longer valid on GitHub?

RQ2: For the same keyword, how many overlapping repositories are retrieved from GitHub and Software Heritage?

RQ3: How well does repositories’ metadata (full names, descriptions, and readme) match with search keywords via search tools?

RQ4: What proportion of repositories are missing critical metadata like readme or description?

RQ5: What are the differences in repository metadata(stars, forks, age) between the two platforms? 

# Mining Process
![image](https://github.com/user-attachments/assets/c59923df-3ba7-4ef9-90ed-b2b498d32fc5)
The figure shows the mining process.

# Repository Structure
![image](https://github.com/user-attachments/assets/79b191a9-558d-4bf1-af9d-dc250a43a415)


# Raw dataset (selection process)

Due to our need, we need to request metadata for each repository.

However, Software Heritage API only allows 1200 requests per hour.

So we only select 1000 repositories from each platform (2000 repositories in total) here.

In keyword selection, we use "python" as an example. Because it's a hot keyword on GitHub and Software Heritage. 

However, you can select any keyword to reproduce this study.

Before starting this study, you need to get your **tokens** of GitHub and Software Heritage and write them in Program **1. Github Search.py and 2. SWH Search.py**.
![image](https://github.com/user-attachments/assets/1ee512b2-e5db-454c-97c9-4dc31002bd37)

Guidance of Software Heritage token creation: https://archive.softwareheritage.org/api/#authentication

Guidance of GitHub token creation: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens


## Step 1: Run 1. Github Search.py and Write "python"

Input: Keyword "python"

Output: Txt files of metadata and age of repositories from GitHub Search will be stored in raw_data/GITHUB_OUTPUT and raw_data/GITHUB_AGE.

This step uses GitHub API to get metadata and calculate the age of repositories using a keyword search on GitHub.

We calculate the age using Update Date-Create Date and Push Date-Create Date.

## Step 2: Run 2. SWH Search.py

**Function 1 of 2. SWH Search.py**

Input: Same Keyword as Step 1

Output: A txt file of URLs of repositories from Software Heritage Search will be stored in raw_data/SWH_URLs.

This step uses Software Heritage API to get URLs of search results on Software Heritage using the same keyword. Because Software Heritage can not directly search the metadata of repositories. 

Software Heritage only allows developers to limit the type of repositories (such as git and pypi) instead of the source of repositories (such as GitHub and GitLab).

So we limit our results type to "git". The results include the repositories from GitLab. We filter the results so that we get 954 repositories as shown in raw_data/SWH_URLs.


# Refined dataset (extraction process)

## Step 2: Run 2. SWH Search.py (RQ1)

**Function 2 of 2. SWH Search.py**

Input: Txt file of URLs of repositories from Software Heritage Search will be stored in raw_data/SWH_URLs.

Output: refined_data\SWH_OUTPUT: Store repositories are still valid on GitHub. 

        refined_data\SWH_VALID_COUNTER: Count the number of valid repositories for further usage. 
        
        refined_data\SWH_INVALID:Store repositories are still invalid on GitHub.

Program 2. SWH Search.py has both functions of extract and refining.

In step 2, we also conduct filtering of Software Heritage to filter out repositories that are currently invalid on GitHub **(RQ1)**. We get 844 repositories in refined_data\SWH_OUTPUT are stored age of repositories in refined_data\SWH_AGE.

## Step 3: Run 3. Random Selection.py
Input: Get the currently valid number of repositories of Software Heritage from refined_data\SWH_VALID_COUNTER. 

        Randomly Select repositories from raw_data\GITHUB_OUTPUT and raw_data\GITHUB_AGE.

Output: GitHub Repositories which have the same number of Repositories from Software Heritage.

Currently, there are 844 repositories from Software Search that are still valid. So we randomly select 844 repositories from 1000 repositories from GitHub Search.

So that we can compare the repositories.

## Step 4: Run 4. Overlap Check.py (RQ2)
Input: Repositories from refined_data\SWH_OUTPUT and refined_data\GITHUB_OUTPUT_REFINED.

Output: Information of overlapping repositories is stored in analysis\Overlapping_Repositories.

In our example which used "python" as the keyword, there are only 2 overlapping repositories.

It shows that search algorithms employed by GitHub and Software Heritage are fundamentally different, which leads to different results even with identical search queries.

## Step 5: Run 5. Similarity Calculation.py (RQ3, RQ4)

**Function 1 of 5. Similarity Calculation.py (RQ3)** 

Input: Metadata in refined_data\SWH_OUTPUT and refined_data\GITHUB_OUTPUT_REFINED.

Output: Semantic similarity between search keyword with metadata of repository (name, description, and readme) is stored in refined_data\SWH_OUTPUT_SIMILARITY and refined_data\GITHUB_OUTPUT_REFINED_SIMILARITY.


We want to know how well the search tool from each platform can help us find matching repositories. So we employ semantic transformer "sentence-transformers/all-MiniLM-L6-v2" from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 to convert the metadata of repositories to vector and compare similarity using cosine calculation with search keyword. 

In the calculation, we assume that our goal is to find the repositories with the highest semantic similarity between the metadata of the repository and the search keyword.

Based on assumptions, semantic similarity represents how well the search tool helps us to find matching repositories.

**Function 2 of 5. Similarity Calculation.py (RQ4)**
Input: Write keyword "python" to calculate.
        
        Metadata in refined_data\SWH_OUTPUT and refined_data\GITHUB_OUTPUT_REFINED.

Output: Repositories that miss metadata are stored in refined_data\GITHUB_OUTPUT_REFINED_NO_DESCRIPTION, refined_data\GITHUB_OUTPUT_REFINED_NO_README, refined_data\SWH_OUTPUT_NO_DESCRIPTION, and refined_data\SWH_OUTPUT_NO_README.

In this function, we check what proportion of repositories are missing critical metadata like readme or description.

Result: 341 (40.4%)Repositories from Software Heritage Search miss readme.

        443 (52.5%)Repositories from Software Heritage Search miss description.

        32 (3.8%)Repositories from GitHub Search miss readme.

        62 (7.3%)Repositories from GitHub Search miss description.



# Analysis of refined data


## Step 6: Run 6. ML-based Similarity Visualization.py

Input: Semantic Similarity from refined_data\GITHUB_OUTPUT_REFINED_SIMILARITY and refined_data\SWH_OUTPUT_SIMILARITY.

Output: Similarity visualization images are stored in analysis\Similarity.

We employed a Neural Network to help us fit curves. The visualization will be slightly different in each run due to different training results of the neural network.

![predicted_scores](https://github.com/user-attachments/assets/9484e75f-e170-4dd0-9a5f-75cfd22aab38)

The figure shows the fitting curve of repositories from GitHub Search and Software Heritage Search.

![score_boxplot](https://github.com/user-attachments/assets/1694e6de-7208-4488-ad62-b755b37bb094)

The figure shows the boxplot of repositories from GitHub Search and Software Heritage Search.

![score_distribution](https://github.com/user-attachments/assets/1983a773-5ce3-4742-818d-4c34a1fd5a78)

The figure shows the distribution of semantic similarity of repositories from GitHub Search and Software Heritage Search.

## Step 7: Run 7. Star Fork Comparison.py

Input: Star and Fork Information from refined_data\SWH_OUTPUT and refined_data\GITHUB_OUTPUT_REFINED.

Output: Visualization features of Fork and Star are stored in analysis\Star_Fork.

![forks_stars_distributions](https://github.com/user-attachments/assets/0bf20001-d57e-47b3-9b4c-09293446fd6b)

## Step 8: Run 8. Age Comparison.py
Input: Age Information from refined_data\GITHUB_AGE_REFINED and refined_data\SWH_AGE.

Output: Visualization features of Fork and Star are stored in analysis\Star_Fork.
![Updated - Created (days) Comparison](https://github.com/user-attachments/assets/34f5d1e9-c433-4b5e-8cc0-70c263caeb3c)
![Pushed - Created (days) Comparison](https://github.com/user-attachments/assets/615f0f1b-df90-45c5-8dac-d66c83d5659d)
![Distribution of Updated-Created](https://github.com/user-attachments/assets/5d9b3eee-d6e8-4d71-a2e5-f44dc8b50548)
![Distribution of Pushed-Created](https://github.com/user-attachments/assets/9bad0e96-fd34-4136-8958-dffb9cf7c947)

# Licensing

This repository is licensed under the GPL-3.0 license, ensuring open use and modification.
