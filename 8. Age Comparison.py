"""
This program analyzes and compares repository age data extracted from two datasets:
GitHub repositories and Software Heritage (SWH) repositories. It calculates the number of days
between key repository events (e.g., "updated - created" and "pushed - created") and performs
statistical tests to determine differences between the two datasets. Additionally, it generates
boxplots and histograms to visualize the distributions of these age-related metrics.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Create output directory for analysis results
os.makedirs(os.path.join('analysis', 'Age'), exist_ok=True)

# Define paths for the two data folders
folder1_path = os.path.join('refined_data', 'GITHUB_AGE_REFINED')
folder2_path = os.path.join('refined_data', 'SWH_AGE')


# Function to extract data from text files
def extract_data_from_folder(folder_path):
    """
    Extracts the "updated - created" and "pushed - created" metrics from text files in the specified folder.

    Parameters:
        folder_path (str): Path to the folder containing text files with data.

    Returns:
        tuple: Two lists containing the extracted "updated - created" and "pushed - created" metrics.
    """
    updated_created = []
    pushed_created = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.txt'):
            with open(file_path, 'r') as file:
                content = file.read()
                updated_match = re.search(r'Updated - Created \(days\): (\d+)', content)
                pushed_match = re.search(r'Pushed - Created \(days\): (\d+)', content)
                if updated_match and pushed_match:
                    updated_created.append(int(updated_match.group(1)))
                    pushed_created.append(int(pushed_match.group(1)))
    return updated_created, pushed_created


# Extract data from both folders
folder1_updated, folder1_pushed = extract_data_from_folder(folder1_path)
folder2_updated, folder2_pushed = extract_data_from_folder(folder2_path)

# Create a dataframe for statistical comparison
data = {
    'Folder': ['Folder1'] * len(folder1_updated) + ['Folder2'] * len(folder2_updated),
    'Updated_Created': folder1_updated + folder2_updated,
    'Pushed_Created': folder1_pushed + folder2_pushed,
}

df = pd.DataFrame(data)

# Perform statistical tests
updated_ttest = stats.ttest_ind(folder1_updated, folder2_updated)
pushed_ttest = stats.ttest_ind(folder1_pushed, folder2_pushed)

# Visualize the "updated - created" data
plt.figure(figsize=(10, 6))
plt.boxplot([folder1_updated, folder2_updated], labels=['GitHub Updated', 'SWH Updated'])
plt.title('Updated - Created (days) Comparison')
plt.ylabel('Days')
plt.savefig(os.path.join('analysis', 'Age', 'Updated - Created (days) Comparison.png'))
plt.show()

# Visualize the "pushed - created" data
plt.figure(figsize=(10, 6))
plt.boxplot([folder1_pushed, folder2_pushed], labels=['GitHub Pushed', 'SWH Pushed'])
plt.title('Pushed - Created (days) Comparison')
plt.ylabel('Days')
plt.savefig(os.path.join('analysis', 'Age', 'Pushed - Created (days) Comparison.png'))
plt.show()

# Display statistical test results
results = {
    "Updated - Created T-Test": updated_ttest,
    "Pushed - Created T-Test": pushed_ttest,
}
print(results)

# Generate histograms for the distributions
plt.figure(figsize=(10, 6))
plt.hist(folder1_updated, bins=30, alpha=0.7, label='GitHub Updated - Created')
plt.hist(folder2_updated, bins=30, alpha=0.7, label='SWH Updated - Created')
plt.title('Distribution of Updated - Created (days)')
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.legend()
plt.savefig(os.path.join('analysis', 'Age', 'Distribution of Updated-Created.png'))
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(folder1_pushed, bins=30, alpha=0.7, label='GitHub Pushed - Created')
plt.hist(folder2_pushed, bins=30, alpha=0.7, label='SWH Pushed - Created')
plt.title('Distribution of Pushed - Created (days)')
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.legend()
plt.savefig(os.path.join('analysis', 'Age', 'Distribution of Pushed-Created.png'))
plt.show()
