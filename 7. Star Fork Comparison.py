"""
This script analyzes repository metadata extracted from text files in two folders.
It compares the number of forks and stars between repositories stored in two different datasets.
The analysis includes:
1. Extracting Fork and Star counts from text files using regular expressions.
2. Saving the extracted data to CSV files for further inspection.
3. Conducting statistical comparisons (t-tests) between the two datasets for forks and stars.
4. Generating boxplots to visualize the differences in forks and stars between the datasets.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Ensure the output directory exists
os.makedirs(os.path.join('analysis', 'Star_Fork'), exist_ok=True)

# Define a function to extract Forks and Stars from text files
def extract_forks_stars(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Use regex to extract Forks and Stars
                forks = re.search(r"Forks:\s*(\d+)", content)
                stars = re.search(r"Stars:\s*(\d+)", content)
                if forks and stars:
                    data.append({'Forks': int(forks.group(1)), 'Stars': int(stars.group(1))})
    return pd.DataFrame(data)

# Define folder paths
folder1_path = os.path.join('refined_data', 'SWH_OUTPUT')
folder2_path = os.path.join('refined_data', 'GITHUB_OUTPUT_REFINED')

# Extract data from both folders
folder1_data = extract_forks_stars(folder1_path)
folder2_data = extract_forks_stars(folder2_path)

# Save extracted data to CSV for inspection
folder1_data.to_csv(os.path.join('analysis', 'Star_Fork', 'SWH.csv'), index=False)
folder2_data.to_csv(os.path.join('analysis', 'Star_Fork', 'github.csv'), index=False)

# Perform statistical comparison between Forks and Stars
forks_ttest = ttest_ind(folder1_data['Forks'], folder2_data['Forks'], equal_var=False)
stars_ttest = ttest_ind(folder1_data['Stars'], folder2_data['Stars'], equal_var=False)

# Plotting the data
plt.figure(figsize=(12, 6))

# Boxplot for Forks
plt.subplot(1, 2, 1)
plt.boxplot([folder1_data['Forks'], folder2_data['Forks']], labels=['Folder 1', 'Folder 2'])
plt.title('Forks Comparison (Boxplot)')
plt.ylabel('Number of Forks')

# Boxplot for Stars
plt.subplot(1, 2, 2)
plt.boxplot([folder1_data['Stars'], folder2_data['Stars']], labels=['Folder 1', 'Folder 2'])
plt.title('Stars Comparison (Boxplot)')
plt.ylabel('Number of Stars')

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(os.path.join('analysis', 'Star_Fork', 'forks_stars_distributions.png'))
plt.show()

# Print statistical results
print("Forks T-test Results:", forks_ttest)
print("Stars T-test Results:", stars_ttest)
