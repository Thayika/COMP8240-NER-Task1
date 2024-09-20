import string
import os

# Define base path where all files are located
base_path = "/workspaces/COMP8240-NER-Task1/stanford-ner-2020-11-17"

# Input and output file paths
wikipedia_input = os.path.join(base_path, "stanford-wikipedia3.txt")
fanwiki_input = os.path.join(base_path, "stanford-fanwiki3.txt")
wikipedia_output_fixed = os.path.join(base_path, "stanford-wikipedia-fixed.txt")
fanwiki_output_fixed = os.path.join(base_path, "stanford-fanwiki-fixed.txt")

# Function to fix punctuation tags
def fix_punctuation(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            tokens = line.strip().split()
            fixed_tokens = []
            for token in tokens:
                if '/' in token:
                    word, tag = token.rsplit('/', 1)
                    # Check if the word is punctuation
                    if word in string.punctuation or word in ['``', "''", '--', '...']:
                        # Change tag of punctuation to 'O'
                        fixed_tokens.append(f"{word}/O")
                    else:
                        fixed_tokens.append(f"{word}/{tag}")
                else:
                    # If token doesn't contain '/', write it as is
                    fixed_tokens.append(token)
            outfile.write(' '.join(fixed_tokens) + '\n')

# Apply the function to both Wikipedia and Fanwiki NER outputs
fix_punctuation(wikipedia_input, wikipedia_output_fixed)
fix_punctuation(fanwiki_input, fanwiki_output_fixed)

print(f"Fixed NER outputs written to:\n{wikipedia_output_fixed}\n{fanwiki_output_fixed}")
