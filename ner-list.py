import os

def extract_entities(ner_input_file, output_file):
    entities = set()
    with open(ner_input_file, 'r', encoding='utf-8') as f:
        for line in f:
            tokens = line.strip().split()
            current_entity = []
            current_tag = None
            for token in tokens:
                if '/' in token:
                    word, tag = token.rsplit('/', 1)
                    # Handle tokens where tag might be missing
                    if not tag:
                        continue
                    # Skip if tag is 'O'
                    if tag == 'O':
                        if current_entity:
                            # End of current entity, add to set
                            entity = ' '.join(current_entity)
                            entities.add(entity)
                            current_entity = []
                            current_tag = None
                        continue
                    else:
                        # If we are in the middle of an entity with the same tag
                        if current_tag == tag:
                            current_entity.append(word)
                        else:
                            if current_entity:
                                # Different tag, save the previous entity
                                entity = ' '.join(current_entity)
                                entities.add(entity)
                            # Start a new entity
                            current_entity = [word]
                            current_tag = tag
                else:
                    # Handle tokens without '/' (unlikely but safe)
                    if current_entity:
                        # End of current entity, add to set
                        entity = ' '.join(current_entity)
                        entities.add(entity)
                        current_entity = []
                        current_tag = None
            # After processing all tokens in line, check if any entity remains
            if current_entity:
                entity = ' '.join(current_entity)
                entities.add(entity)
                current_entity = []
                current_tag = None
    # Write the entities to the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for entity in sorted(entities):
            f_out.write(entity + '\n')
    print(f"Extracted entities have been saved to {output_file}")

def main():
    # Paths to your NER-tagged input files and output files
    wikipedia_ner_input = 'stanford-wikipedia3.txt'
    wikipedia_entities_output = 'ner-list-wikipedia.txt'
    fanwiki_ner_input = 'stanford-fanwiki3.txt'
    fanwiki_entities_output = 'ner-list-fanwiki.txt'

    # Extract entities from the Wikipedia NER output
    extract_entities(wikipedia_ner_input, wikipedia_entities_output)

    # Extract entities from the Fanwiki NER output
    extract_entities(fanwiki_ner_input, fanwiki_entities_output)

if __name__ == '__main__':
    main()
