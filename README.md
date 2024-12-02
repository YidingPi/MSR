Repository-Insights
# Description
This repository contains the data, scripts, and documentation for the study "A Study of Repository Characteristics Using GitHub and Software Heritage Search Tools." The goal of this project is to explore the overlap, metadata differences, and search result relevance of repositories retrieved from GitHub and Software Heritage search tools using the keyword(We use "python" as an example).

# Mining Process
![image](https://github.com/user-attachments/assets/c59923df-3ba7-4ef9-90ed-b2b498d32fc5)

![image](https://github.com/user-attachments/assets/dec15f3b-7676-4bad-a29c-6c08341e52a4)

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
