# Description
This repository contains the data, scripts, and documentation for the study **"A Study of Repository Characteristics of Search Results from GitHub and Software Heritage Search Tools."** The goal of this project is to explore the overlap, metadata differences, and search result relevance of repositories retrieved from GitHub and Software Heritage search tools using a keyword (e.g., "python").

---

# Data Sources

- **Data Source:** GitHub Repositories from Software Heritage API and GitHub API  
  - **Software Heritage API Example:** [Search Python Repositories](https://archive.softwareheritage.org/api/1/origin/search/python/?limit=1000&?with_visit=1&visit_type=git)  
  - **GitHub API Example:** [Search Python Repositories](https://api.github.com/search/repositories?q=python)  
- **Date of Access:** December 1, 2024  

---

# Research Questions

1. **RQ1:** How many repositories retrieved from Software Heritage are no longer valid on GitHub?
2. **RQ2:** For the same keyword, how many overlapping repositories are retrieved from GitHub and Software Heritage?
3. **RQ3:** How well does repositories’ metadata (e.g., full names, descriptions, and README files) match search keywords via search tools?
4. **RQ4:** What proportion of repositories are missing critical metadata such as README or description?
5. **RQ5:** What are the differences in repository metadata (e.g., stars, forks, age) between the two platforms?

---

# Mining Process
![Mining Process](https://github.com/user-attachments/assets/c59923df-3ba7-4ef9-90ed-b2b498d32fc5)  
_The figure above shows the mining process._

---

# Repository Structure
![Repository Structure](https://github.com/user-attachments/assets/79b191a9-558d-4bf1-af9d-dc250a43a415)
_The figure above shows the Repository Structure._

---

# Raw Dataset (Selection Process)

- **Selection Details:**
  - Each platform's API constraints required limiting requests (Software Heritage: 1200/hour).
  - We selected **1000 repositories from each platform** (2000 total) using the keyword **"python"** as an example due to its popularity.

- **Setup Instructions:**
  1. Obtain **tokens** for both GitHub and Software Heritage APIs:
     - [Software Heritage Token Guide](https://archive.softwareheritage.org/api/#authentication)
     - [GitHub Token Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
  2. Write tokens into the programs `1. Github Search.py` and `2. SWH Search.py`.

![Token Setup](https://github.com/user-attachments/assets/1ee512b2-e5db-454c-97c9-4dc31002bd37)

---

## Steps for Dataset Collection and Refinement

### Step 1: GitHub Search (`1. Github Search.py`)
- **Input:** Keyword "python"  
- **Output:** Metadata and repository age stored in:
  - `raw_data/GITHUB_OUTPUT`
  - `raw_data/GITHUB_AGE`  
- **Details:**  
  - Metadata retrieved using GitHub API.
  - Repository age calculated as `(Update Date - Create Date)` and `(Push Date - Create Date)`.

### Step 2: Software Heritage Search (`2. SWH Search.py` - Function 1)
- **Input:** Keyword "python"  
- **Output:** URLs of repositories stored in `raw_data/SWH_URLs`.  
- **Details:**  
  - Filters results to get GitHub repositories from Git-type repositories(including GitHub and GitLab).  
  - 954 repositories are stored from 1000 Git-type repositories.

---

# Refined Dataset (Extraction Process)

### Step 3: Validation of Software Heritage Repositories (`2. SWH Search.py` - Function 2)
- **Input:** URLs from `raw_data/SWH_URLs`  
- **Output:**  
  - `refined_data/SWH_OUTPUT`: Valid repositories on GitHub.  
  - `refined_data/SWH_VALID_COUNTER`: Count of valid repositories.  
  - `refined_data/SWH_INVALID`: Invalid repositories on GitHub.  
- **Details:**  
  - Out of 954 repositories, 844 are valid and stored.

### Step 4: Random Selection (`3. Random Selection.py`)
- **Input:** Valid repository count (`SWH_VALID_COUNTER`).  
- **Output:** Randomly selected repositories from GitHub stored in `refined_data/GITHUB_OUTPUT_REFINED`.  
- **Details:** Matches 844 repositories for comparison.

### Step 5: Overlap Check (`4. Overlap Check.py`)
- **Input:** Valid repositories from both platforms.  
- **Output:** Overlapping repositories in `analysis/Overlapping_Repositories`.  
- **Result:** Only 2 overlapping repositories found for the "python" keyword.

---

## Analysis of Refined Data

### Step 6: Similarity Calculation (`5. Similarity Calculation.py`)
- **Function 1 (RQ3):**  
  - **Input:** Metadata from `refined_data/SWH_OUTPUT` and `refined_data/GITHUB_OUTPUT_REFINED`.  
  - **Output:** Semantic similarity scores stored.  
  - **Details:** Uses [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) for similarity calculation.

- **Function 2 (RQ4):**  
  - **Input:** Metadata from both platforms.  
  - **Output:** Missing metadata reports:
    - GitHub: `GITHUB_OUTPUT_REFINED_NO_DESCRIPTION` and `GITHUB_OUTPUT_REFINED_NO_README`
    - Software Heritage: `SWH_OUTPUT_NO_DESCRIPTION` and `SWH_OUTPUT_NO_README`  
  - **Results:**  
    - **Software Heritage:**  
      - 40.4% missing README.  
      - 52.5% missing description.  
    - **GitHub:**  
      - 3.8% missing README.  
      - 7.3% missing description.

---

# Visualization

### Step 7: Semantic Similarity Visualization (`6. ML-based Similarity Visualization.py`)
![Predicted Scores](https://github.com/user-attachments/assets/9484e75f-e170-4dd0-9a5f-75cfd22aab38)  
_Fitting curve of repositories._  

![Boxplot](https://github.com/user-attachments/assets/1694e6de-7208-4488-ad62-b755b37bb094)  
_Boxplot comparison._  

![Score Distribution](https://github.com/user-attachments/assets/1983a773-5ce3-4742-818d-4c34a1fd5a78)  
_Distribution of semantic similarity._

### Step 8: Star and Fork Comparison (`7. Star Fork Comparison.py`)
![Forks and Stars Distribution](https://github.com/user-attachments/assets/0bf20001-d57e-47b3-9b4c-09293446fd6b)

### Step 9: Age Comparison (`8. Age Comparison.py`)
![Updated-Created Comparison](https://github.com/user-attachments/assets/34f5d1e9-c433-4b5e-8cc0-70c263caeb3c)  
![Pushed-Created Comparison](https://github.com/user-attachments/assets/615f0f1b-df90-45c5-8dac-d66c83d5659d)

---

# Licensing
This repository is licensed under the **GPL-3.0 license**, ensuring open use and modification.
