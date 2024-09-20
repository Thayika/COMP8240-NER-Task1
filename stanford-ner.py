import os

def run_ner(input_file, output_file):
    # Command to run the Stanford NER system
    command = f"./ner.sh {input_file} > {output_file}"
    os.system(command)
    print(f"NER tagging complete. Output saved to {output_file}")

def main():
    # Paths to your input and output files
    wikipedia_input = 'wikipedia_tom_cruise2.txt'
    wikipedia_output = 'stanford-wikipedia3.txt'
    fanwiki_input = 'fanwiki_jotaro_kujo2.txt'
    fanwiki_output = 'stanford-fanwiki3.txt'

    # Run NER on the Wikipedia text
    run_ner(wikipedia_input, wikipedia_output)

    # Run NER on the Fanwiki text
    run_ner(fanwiki_input, fanwiki_output)

if __name__ == "__main__":
    main()
