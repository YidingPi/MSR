Repository-Insights
# Description
This repository contains the data, scripts, and documentation for the study "A Study of Repository Characteristics of Search Results from GitHub and Software Heritage Search Tools." The goal of this project is to explore the overlap, metadata differences, and search result relevance of repositories retrieved from GitHub and Software Heritage search tools using the keyword(We use "python" as an example).

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
![image](https://github.com/user-attachments/assets/dec15f3b-7676-4bad-a29c-6c08341e52a4)

# Raw dataset (selection process)

Due to our need, we need to request metadata for each repository.

However, Software Heritage API only allows 1200 requests per hour.

So we only select 1000 repositories from each platform (2000 repositories in total) here.

In keyword selection, we use "python" as an example. Because it's a hot keyword on GitHub and Software Heritage. 

However, you can select any keyword to reproduce this study.

Before starting this study, you need to get your **tokens** of GitHub and Software Heritage and write them in Program **1. Github Search.py and 2. SWH Search.py**.

Guidance of Software Heritage token creation: https://archive.softwareheritage.org/api/#authentication

Guidance of GitHub token creation: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

Data Source: Software Heritage API and GitHub API

## Step 1: Run 1. Github Search.py and Write "python"
Input: Keyword "python"
Output: Txt files of metadata and age of repositories from GitHub Search will be stored in raw_data/GITHUB_OUTPUT and raw_data/GITHUB_AGE.

This step uses GitHub API to get metadata and calculate the age of repositories using a keyword search on GitHub.
We calculate the age using Update Date-Create Date and Push Date-Create Date.

## Step 2: Run 2. SWH Search.py
Input: Same Keyword as Step 1
Output: A txt file of URLs of repositories from Software Heritage Search will be stored in raw_data/SWH_URLs.

This step uses Software Heritage API to get URLs of search results on Software Heritage using the same keyword. Because Software Heritage can not directly search the metadata of repositories. 

Software Heritage only allows developers to limit the type of repositories (such as git and pypi) instead of the source of repositories (such as GitHub and GitLab).

So we limit our results type to "git". The results include the repositories from GitLab. We filter the results so that we get 954 repositories as shown in raw_data/SWH_URLs.


# Refined dataset (extraction process)

## Step 2: Run 2. SWH Search.py
Input: Txt file of URLs of repositories from Software Heritage Search will be stored in raw_data/SWH_URLs.

Output: refined_data\SWH_OUTPUT: Store repositories are still valid on GitHub. refined_data\SWH_VALID_COUNTER: Count the number of valid repositories for further usage refined_data\SWH_INVALID:Store repositories are still invalid on GitHub.

In step 2, we also conduct filtering of Software Heritage to filter out repositories that are currently invalid on GitHub. We get 844 repositories in refined_data\SWH_OUTPUT are stored age of repositories in refined_data\SWH_AGE.

## Step 3: Run 3. Random Selection.py
Input: Get the currently valid number of repositories of Software Heritage from refined_data\SWH_VALID_COUNTER. Randomly Select repositories from raw_data\GITHUB_OUTPUT and raw_data\GITHUB_AGE.
Output: GitHub Repositories which have the same number of Repositories from Software Heritage
Currently, there are 844 repositories from Software Search that are still valid. So we randomly select 844 repositories from 1000 repositories from GitHub Search.

So that we can compare the repositories.



Purpose of the Dataset
The dataset includes:

Raw Data: Search results and metadata collected directly from the APIs of GitHub and Software Heritage.
Refined Data: Processed and analyzed data to address research questions on repository overlaps, metadata completeness, and semantic relevance.
Repository Structure
The repository is organized as follows:


data/
raw/: Contains raw datasets retrieved from GitHub and Software Heritage APIs.
refined/: Contains processed datasets with metadata and analysis results.
scripts/
data_collection.py: Automates the retrieval of repository metadata from APIs.
data_processing.py: Processes raw datasets into a refined format.
semantic_similarity.py: Calculates semantic similarity for relevance analysis.
docs/
Contains the LaTeX files and PDF presentation of the study.
Includes a diagram of the selection and extraction processes.
results/
Visualizations and statistical summaries of the refined dataset.
Dataset and Selection Process
Raw Dataset
Sources

GitHub API: https://api.github.com
Software Heritage API: https://archive.softwareheritage.org/api/
Accessed: November 2024
Selection Criteria

Repositories retrieved using the keyword "Python."
API limits: 5,000 requests/hour for GitHub, 1,200 requests/hour for Software Heritage.
Dataset limited to 1,000 repositories per platform due to constraints.
Reproducibility

Scripts for data collection (scripts/data_collection.py) are provided with detailed usage instructions.
Instructions for API access and key setup are included in the docs/ folder.
Availability

The raw dataset is available in the data/raw/ directory in CSV format.
Refined Dataset
Extraction Process

Scripts in scripts/data_processing.py extract and transform metadata, calculate statistics, and clean missing or inconsistent data.
Descriptive Statistics

Includes metadata summaries such as repository age, stars, forks, and missing fields.
Availability

The refined dataset is available in the data/refined/ directory in CSV format.
Key Features
Non-Proprietary Formats: Data is provided in widely accepted formats like CSV.
Schema and Processes: A flowchart in docs/selection_schema.pdf illustrates the selection and extraction processes.
Documentation: Comprehensive instructions for reproducing results are included.
Licensing: This repository is licensed under the MIT License, ensuring open use and modification.
