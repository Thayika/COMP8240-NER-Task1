import requests
import os
import fandom
import re

def extract_wikipedia():
    article_title = 'Tom Cruise'
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'explaintext': True,
        'titles': article_title,
        'utf8': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    if 'extract' in page:
        content = page['extract']
        with open('wikipedia_tom_cruise2.txt', 'w', encoding='utf-8') as file:
            file.write(content)
            print("Wikipedia content successfully written.")
    else:
        print("No Wikipedia content found.")

def extract_fandom():
    fandom.set_wiki("jojo")
    character_name = 'Jotaro Kujo'
    character_page = fandom.search(character_name)
    if character_page:
        page = character_page[0]
        page_content = fandom.page(page[0]).content
        if isinstance(page_content, dict):
            page_content = page_content.get('content', '')
        with open('fanwiki_jotaro_kujo2.txt', 'w', encoding='utf-8') as file:
            file.write(page_content)
            print(f"Fandom content successfully written.")
    else:
        print(f"No Fandom content found for {character_name}.")

def run_ner(input_file, output_file):
    ner_command = f"./ner.sh {input_file} > {output_file}"
    os.system(ner_command)
    print(f"NER output written to {output_file}.")

def extract_entities(filename):
    entities = set()
    unwanted_entities = {'O', 'of', 'the', '-', '(', ')', ',', '.', 'and', 'in', 'at'}  # Expanding unwanted list
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            tokens = line.split()
            for token in tokens:
                if '/' in token:
                    word, tag = token.rsplit('/', 1)
                    # Exclude unwanted tokens and ensure tag is valid
                    if tag not in ['O'] and word.lower() not in unwanted_entities:
                        entities.add(f"{word} [{tag}]")
    return entities


def main():
    extract_wikipedia()
    extract_fandom()
    run_ner('wikipedia_tom_cruise2.txt', 'stanford-wikipedia2.txt')
    run_ner('fanwiki_jotaro_kujo2.txt', 'stanford-fanwiki2.txt')
    wikipedia_entities = extract_entities('stanford-wikipedia2.txt')
    fanwiki_entities = extract_entities('stanford-fanwiki2.txt')
    print("\nWikipedia Entities:")
    for entity in sorted(wikipedia_entities):
        print(entity)
    print("\nFanwiki Entities:")
    for entity in sorted(fanwiki_entities):
        print(entity)

if __name__ == "__main__":
    main()
