"""
This script compares two folders to find common project names based on file names.
The project name is identified as the part of the file name after the first underscore.
It then calculates the percentage of common project names relative to a total number
stored in a separate file and writes the results to an output file.
"""

import os

def extract_project_names(folder_path):
    """
    Extracts the project names from all files in the specified folder.
    The project name is considered the part of the file name after the first underscore.

    Args:
        folder_path (str): Path to the folder containing the files.

    Returns:
        set: A set of project names extracted from the file names.
    """
    project_names = set()
    for file_name in os.listdir(folder_path):
        if "_" in file_name:
            _, project_name = file_name.split("_", 1)
            project_names.add(project_name)
    return project_names

def read_number_from_file(file_path):
    """
    Reads a number from the specified file.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: The number read from the file, or 0 if reading fails.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            # Extract the number from the file
            number = int(content)
            return number
    except (FileNotFoundError, ValueError) as e:
        print(f"Failed to read the file: {e}")
        return 0

def compare_folders(folder1, folder2):
    """
    Compares the project names in two folders and identifies common project names.

    Args:
        folder1 (str): Path to the first folder.
        folder2 (str): Path to the second folder.

    Returns:
        set: A set of common project names found in both folders.
    """
    projects_folder1 = extract_project_names(folder1)
    projects_folder2 = extract_project_names(folder2)

    common_projects = projects_folder1.intersection(projects_folder2)
    return common_projects

# Example usage
folder1_path = os.path.join('refined_data', 'SWH_OUTPUT')  # Path to folder 1
folder2_path = os.path.join('refined_data', 'GITHUB_OUTPUT_REFINED')  # Path to folder 2

common_projects = compare_folders(folder1_path, folder2_path)

# Prepare output directory and file
output_dir = os.path.join('analysis', 'Overlapping_Repositories')
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, 'Overlapping.txt')

# Write the output to the file
with open(output_file_path, 'w') as output_file:
    output_file.write("The common project names in both folders are:\n")
    for project in common_projects:
        output_file.write(f"{project}\n")
    output_file.write(f"\nThere are {len(common_projects)} common project names.\n")
    output_file.write(f"\nThe percentage of common projects is: ")
    c_file_path = os.path.join('refined_data', 'SWH_VALID_COUNTER', "counter.txt")  # Path to counter file

    num_files_to_select = read_number_from_file(c_file_path)
    percentage = (len(common_projects) / num_files_to_select) * 100
    output_file.write(f"{percentage:.2f}%")

print(f"Output written to {output_file_path}")
