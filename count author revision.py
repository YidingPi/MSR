import os
import pandas as pd
import pyarrow.orc as orc
from collections import Counter

def read_orc_full(file_path):
    """
    Read full data from an ORC file and convert it to a Pandas DataFrame.
    """
    try:
        orc_file = orc.ORCFile(file_path)
        table = orc_file.read()
        return table.to_pandas()
    except Exception:
        return None

def read_all_orc_files_in_folder(folder_path):
    """
    Read all ORC files in a folder and merge them into a single DataFrame.
    """
    all_data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            df = read_orc_full(file_path)
            if df is not None:
                all_data.append(df)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return None

def write_in_chunks(df, output_file_path, chunk_size=1000):
    """
    Write data to a file in chunks to avoid memory issues.
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for start in range(0, len(df), chunk_size):
                chunk = df.iloc[start:start+chunk_size]
                f.write(chunk.to_string(index=False))
                f.write('\n')  # Add newline to separate different chunks
    except Exception:
        pass

def count_revisions_by_author(df, author_column_name='author', output_file_path=None):
    """
    Count the number of revisions per author and write the results to a file.
    """
    if author_column_name not in df.columns:
        return

    author_revision_count = Counter(df[author_column_name].dropna())
    total_revisions = sum(author_revision_count.values())

    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for author, count in author_revision_count.items():
                    f.write(f"{author}: {count}\n")
                f.write(f"Total revisions: {total_revisions}\n")
        except Exception:
            pass

# Main function
def main():
    # Replace with your folder path
    orc_folder_path = "C:/orc/revision/"
    output_file_path = "c:/orc/12orc_data_output.txt"
    stats_file_path = "c:/orc/author_stats.txt"

    # Read all ORC file data from the folder
    df = read_all_orc_files_in_folder(orc_folder_path)
    if df is None or df.empty:
        return

    # Count revisions by author and write to file
    count_revisions_by_author(df, author_column_name='author', output_file_path=stats_file_path)

    # Write data to file in chunks
    write_in_chunks(df, output_file_path, chunk_size=1000)

# Execute main function
if __name__ == "__main__":
    main()
