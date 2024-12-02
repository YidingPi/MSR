"""
This program performs the following tasks:
1. Reads a number from a specified file.
2. Randomly selects a given number of files from a source directory.
3. Copies the selected files into a target directory.
4. If files with the same names exist in another source directory, they are also copied to a corresponding target directory.

The purpose of the script is to automate the selection and copying of files for data refinement.
"""

import os
import random
import shutil


def read_number_from_file(file_path):
    """Reads a number from the specified file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            # Extract the number from the file
            number = int(content)
            return number
    except (FileNotFoundError, ValueError) as e:
        print(f"Failed to read the file: {e}")
        return 0


def random_select_and_copy_files(source_dir1, source_dir2, num_files):
    """Randomly selects files from source_dir1 and copies them to target directories.
    If files with the same names exist in source_dir2, they are also copied."""
    # Ensure the target directories exist
    target_dir1 = os.path.join('refined_data', 'GITHUB_OUTPUT_REFINED')  # Path to the target directory for source_dir1 files
    os.makedirs(target_dir1, exist_ok=True)
    target_dir2 = os.path.join('refined_data', 'GITHUB_AGE_REFINED')  # Path to the target directory for source_dir2 files
    os.makedirs(target_dir2, exist_ok=True)

    # Get all file names in source_dir1
    files1 = os.listdir(source_dir1)

    # Randomly select num_files files
    selected_files = random.sample(files1, min(num_files, len(files1)))

    for file_name in selected_files:
        # Construct the full paths for source and target files in source_dir1
        source_file1 = os.path.join(source_dir1, file_name)
        target_file1 = os.path.join(target_dir1, file_name)
        # Copy the file from source_dir1 to the target directory
        shutil.copy(source_file1, target_file1)

        # Check if a file with the same name exists in source_dir2
        source_file2 = os.path.join(source_dir2, file_name)
        if os.path.exists(source_file2):
            target_file2 = os.path.join(target_dir2, file_name)
            # Copy the file from source_dir2 to the target directory
            shutil.copy(source_file2, target_file2)

    print(f"Randomly selected files: {selected_files}")
    print(f"Files have been copied to the target directory: {target_dir1}")


# Example usage
a_directory = os.path.join('raw_data', 'GITHUB_OUTPUT')  # Path to the first source directory
b_directory = os.path.join('raw_data', 'GITHUB_AGE')  # Path to the second source directory
c_file_path = os.path.join('refined_data', 'SWH_VALID_COUNTER', "counter.txt")  # Path to the file containing the number of files to select

# Read the number from the file
num_files_to_select = read_number_from_file(c_file_path)
#print(num_files_to_select)
if num_files_to_select > 0:
    # Perform random file selection and copying
    random_select_and_copy_files(a_directory, b_directory, num_files_to_select)
else:
    print("No valid number read. Operation canceled.")
