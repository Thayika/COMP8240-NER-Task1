import os

wikipedia_ner_output = "stanford-wikipedia3.txt"
fanwiki_ner_output = "stanford-fanwiki3.txt"
wikipedia_gold_output = "wikipedia-gold3.txt"
fanwiki_gold_output = "fanwiki-gold3.txt"

def convert_ner_output_to_gold(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            tokens = line.strip().split()
            for token in tokens:
                if '/' in token:
                    word, tag = token.rsplit('/', 1)
                    fout.write(f"{word}\t{tag}\n")
                else:
                    fout.write(f"{token}\tO\n")
            fout.write("\n")  # Add a blank line after each sentence

convert_ner_output_to_gold('stanford-wikipedia3.txt', 'wikipedia-gold3.txt')
convert_ner_output_to_gold('stanford-fanwiki3.txt', 'fanwiki-gold3.txt')

