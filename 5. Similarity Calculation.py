import os
from sentence_transformers import SentenceTransformer, util
#!!!! pipei
nor=0
nod=0
def extract_txt_info(folder_path):
    global nor
    global nod
    combined_info = []
    noreadme_folder = f"{folder_name}_NO_README"
    nodescription_folder = f"{folder_name}_NO_DESCRIPTION"
    os.makedirs(noreadme_folder, exist_ok=True)
    os.makedirs(nodescription_folder, exist_ok=True)
    no_description_path = os.path.join(nodescription_folder, "nodescription.txt")
    no_readme_path = os.path.join(noreadme_folder, "noreadme.txt")
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Extract relevant fields
                full_name = extract_field(content, "Full Name:")
                description = extract_field(content, "Description:")
                topics = extract_field(content, "Topics:")
                readme = extract_field(content, "README:", to_end=True)

                # Check for missing fields and write to `nodescription.txt` if necessary
                if description == "None":
                    with open(no_description_path, 'a', encoding='utf-8') as no_desc_file:
                        no_desc_file.write(f"File: {filename}\n")
                        nod=nod+1
                        no_desc_file.write(content + "\n\n")
                if readme == "":
                    with open(no_readme_path, 'a', encoding='utf-8') as no_desc_file:
                        no_desc_file.write(f"File: {filename}\n")
                        #print(description)
                        nor=nor+1
                        no_desc_file.write(content + "\n\n")
                # Combine fields into a single string
                combined = f"{full_name} {description} {topics} {readme}"
                combined_info.append((filename, combined))

    return combined_info


def extract_field(content, field_name, to_end=False):
    """Extract the content of a specific field from the text."""
    try:
        start_idx = content.index(field_name) + len(field_name)
        if to_end:
            # Extract everything from the field to the end of the file
            return content[start_idx:].strip()
        else:
            # Extract only the line following the field name
            end_idx = content.find("\n", start_idx)
            if end_idx == -1:  # In case the field is the last one
                end_idx = len(content)
            return content[start_idx:end_idx].strip()
    except ValueError:
        return "Not Found"


def process_txt_files_with_similarity(folder_name, keywords):
    # Load the pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    scorex = []
    # Extract combined information from .txt files
    combined_info = extract_txt_info(folder_name)

    # Compute embeddings for project texts and keyword
    descriptions = [info[1] for info in combined_info]
    description_embeddings = model.encode(descriptions, convert_to_tensor=True)
    keyword_embedding = model.encode(keywords, convert_to_tensor=True)
    #print(descriptions)
    # Compute cosine similarity
    cosine_scores = util.cos_sim(keyword_embedding, description_embeddings)[0]

    # Pair descriptions with similarity scores
    description_similarity = [(combined_info[i][0], combined_info[i][1], cosine_scores[i].item()) for i in
                              range(len(combined_info))]

    # Sort by similarity score
    description_similarity.sort(key=lambda x: x[2], reverse=True)

    # Prepare result folder
    result_folder = f"{folder_name}_SIMILARITY"
    os.makedirs(result_folder, exist_ok=True)

    # Save results to files in the result folder
    for i, (file_name, content, score) in enumerate(description_similarity):
        result_file_path = os.path.join(result_folder, f"{i + 1}_{file_name}_SIMILARITY.txt")
        with open(result_file_path, 'w', encoding='utf-8') as result_file:
            result_file.write(f"Score: {score:.4f}\n")
            scorex.append(score)
            result_file.write(content)
    result_folder1 = f"{folder_name}_SIMILARITY_OVERALL"
    os.makedirs(result_folder1, exist_ok=True)
    qpath = os.path.join(result_folder1, "overallresult.txt")
    with open(qpath, 'w', encoding='utf-8') as result_file1:
        for q in scorex:
            result_file1.write(f"{q:.4f}\n")
    print(f"Results saved in folder: {result_folder}")
    print(scorex)


# Main function for interactive input
if __name__ == "__main__":
    #folder_name = input("Enter the folder name containing .txt files: ").strip()
    folder_name = os.path.join('refined_data','SWH_OUTPUT')
    keywords = input("Enter the keywords to calculate semantic similarity: ").strip()
    process_txt_files_with_similarity(folder_name, keywords)
    # Check for missing fields and write to `nodescription.txt` if necessary
    noreadme_folder = f"{folder_name}_NO_README"
    nodescription_folder = f"{folder_name}_NO_DESCRIPTION"
    no_description_path = os.path.join(nodescription_folder, "nodescription_overall.txt")
    no_readme_path = os.path.join(noreadme_folder, "noreadme_overall.txt")

    with open(no_description_path, 'a', encoding='utf-8') as no_desc_file:
        no_desc_file.write(f"{nod}\n")

    with open(no_readme_path, 'a', encoding='utf-8') as no_desc_file:
        no_desc_file.write(f"{nor}\n")
    nor = 0
    nod = 0
    folder_name = os.path.join('refined_data','GITHUB_OUTPUT_REFINED')

    process_txt_files_with_similarity(folder_name, keywords)
    # Check for missing fields and write to `nodescription.txt` if necessary
    noreadme_folder = f"{folder_name}_NO_README"
    nodescription_folder = f"{folder_name}_NO_DESCRIPTION"
    no_description_path = os.path.join(nodescription_folder, "nodescription_overall.txt")
    no_readme_path = os.path.join(noreadme_folder, "noreadme_overall.txt")

    with open(no_description_path, 'a', encoding='utf-8') as no_desc_file:
        no_desc_file.write(f"{nod}\n")

    with open(no_readme_path, 'a', encoding='utf-8') as no_desc_file:
        no_desc_file.write(f"{nor}\n")