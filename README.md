# COMP8240-NER-Task1
COMP8240 Assessment Task 1
Introduction
This project is to work with code that does Named Entity Recognition (NER) and required to:
- use a VM;
- install and run existing code in the VM;
- scrape data from the web;
- write some (small) scripts for evaluating the NER system; and
- use a GitHub repository for the scripts and data files.

The procedures are:
1. Environment Setup
- Virtual Machine: GitHub Codespaces.
- Programming Language: Python 3.
- NER Tool: Stanford NER system (version 4.2.0).
- Dependencies:
  - Java (required for Stanford NER).
  - Python libraries: requests, fandom, re, os, string.

2. Data Extraction
- File: extract-data.py 
  - Wikipedia Target Article: "Tom Cruise"
  - Fandom Target Character: "Jotaro Kujo"
- Method:
  - Wikipedia
    - Use Wikipedia API
    - The data is saved to wikipedia_tom_cruise2.txt.
  - Fandom 
    - Use fandom library to retrieve data
    - The data is saved to fanwiki_jotaro_kujo2.txt.

3. Apply Standard NER
- File: stanford-ner.py
- Purpose: Purpose: To tag each word in the texts with their respective NER labels
- Method: 
    - apply NER using ner.sh on the input files extracted from previous procedures
    - the data is saved to:
        - stanford-fanwiki3.txt
        - stanford-wikipedia3.txt

4. Extracting Named Entities
- File: ner-list.py
 - Purpose: Extract named entities from the NER-tagged output files and list each unique entity
- Method:
    - Read stanford-wikipedia3.txt, stanford-fanwiki3.txt
    - Parses tokens and groups adjacent words with the same entity tag.
    - Collects all unique entities and writes them to output files.
- The data is saved to:
    - ner-list-wikipedia.txt
    - ner-list-fanwiki.txt
- Sample Output:
    - Wikipedia:
        Academy Awards
        American
        Cruise
        Golden Globe Awards
        Hollywood
        Honorary Palme d'Or
        Mission: Impossible
        North America
        Thomas Cruise Mapother IV
        Tom Cruise
    - Fandom
        DIO
        Egypt
        Jotaro
        Jotaro Kujo
        Joestar Family
        JoJo
        Kujo
        Star Platinum
4. Creating the Gold Standard
- Method:
    - Converted the NER-tagged output files into a two-column format
- Challenges:
    - Handling special characters and punctuation.
    - Ensuring consistent tagging of multi-word entities.
- The data saved to:
    - wikipedia-gold3.txt
    - fanwiki-gold3.txt
5. Evaluation of NER Results
- Script: eval.sh
- Method:  
    - Modified the ner.sh script to create eval.sh, which uses the -testFile option for evaluation.
    - Generated evaluation reports:
        - wikipedia-eval.txt
        - fanwiki-eval.txt
    - Scripts used:
        ./eval.sh wikipedia-gold.txt > wikipedia-eval.txt
        ./eval.sh fanwiki-gold.txt > fanwiki-eval.txt
    - Output 
    Wikipedia NER Results:
            Entity  P       R       F1      TP    FP   FN
         LOCATION 1.0000  1.0000  1.0000   54    0    0
     ORGANIZATION 1.0000  1.0000  1.0000   72    0    0
           PERSON 1.0000  1.0000  1.0000  284    0    0
           Totals 1.0000  1.0000  1.0000  410    0    0
    Fanwiki NER Results:
            Entity  P       R       F1      TP    FP   FN
         LOCATION 1.0000  1.0000  1.0000    1    0    0
     ORGANIZATION 1.0000  1.0000  1.0000    5    0    0
           PERSON 1.0000  1.0000  1.0000   26    0    0
           Totals 1.0000  1.0000  1.0000   32    0    0
Interpretation of Results
    - Perfect Scores:
            - The NER system achieved 100% precision, recall, and F1 scores for all entity types.
    - Possible Reasons:
            - Evaluation Setup: The evaluation might be comparing the gold standard file against itself, leading to perfect scores.
            - Data Simplicity: The texts may contain well-known entities that the NER system recognizes effectively.
            - Alignment Issues: The predicted outputs and gold standard files might be identical or incorrectly aligned.
6. Fixing NER Tagging for Punctuation
- Purpose punctuation on the files sometimes cause the evaluation to be incorrect
- File: fix-ner.py
- Method:
    - The script reads each token in the NER outputs and checks if it is a punctuation mark.
    - If a token is a punctuation mark, its NER tag is set to 'O' (outside any named entity).
    - Applied the script to both the Wikipedia and Fanwiki NER output files to produce corrected versions.
7. Re-evaluation of NER Results
    The initial evaluation using eval.sh resulted in perfect precision, recall, and F1 scores, which is highly unusual in real-world NER tasks.
    Upon investigation, it was discovered that the evaluation script was incorrectly configured.
    The eval.sh script was designed to evaluate a test file containing both tokens and gold standard labels, but we were passing it the NER output with predicted labels, causing it to compare the predictions against themselves.

- Correct Evaluation Process
- Created convert_predictions.py to convert the fixed NER outputs (stanford-wikipedia-fixed.txt and stanford-fanwiki-fixed.txt) into a two-column format 
Code: 
    convert_predictions.py

    def convert_ner_output_to_conll(input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as fin, \
            open(output_file, 'w', encoding='utf-8') as fout:
            for line in fin:
                tokens = line.strip().split()
                for token in tokens:
                    if '/' in token:
                        word, tag = token.rsplit('/', 1)
                        fout.write(f"{word}\t{tag}\n")
                fout.write('\n')  # Add a blank line to separate sentences

    #Convert the fixed NER outputs
    convert_ner_output_to_conll('stanford-wikipedia-fixed.txt', 'wikipedia-predicted.txt')
    convert_ner_output_to_conll('stanford-fanwiki-fixed.txt', 'fanwiki-predicted.txt')
- Scripts Used:
    - python evaluate.py wikipedia-gold3.txt wikipedia-predicted.txt > wikipedia-eval.txt
    - python evaluate.py fanwiki-gold3.txt fanwiki-predicted.txt > fanwiki-eval.txt
    
    Wikipedia NER Results
              precision    recall  f1-score   support

      PERSON     1.0000    0.9957    0.9979       469
ORGANIZATION     1.0000    0.9874    0.9937       159
    LOCATION     1.0000    1.0000    1.0000        83

   micro avg     1.0000    0.9944    0.9972       711
   macro avg     1.0000    0.9944    0.9972       711
weighted avg     1.0000    0.9944    0.9972       711

    Fanwiki NER Results
                  precision    recall  f1-score   support

      PERSON     1.0000    1.0000    1.0000        46
ORGANIZATION     1.0000    1.0000    1.0000        10
    LOCATION     1.0000    1.0000    1.0000         1

   micro avg     1.0000    1.0000    1.0000        57
   macro avg     1.0000    1.0000    1.0000        57
weighted avg     1.0000    1.0000    1.0000        57

8. Interpretation 
- Analysis:
    - Wikipedia Data:
        - PERSON Entities: Recall of 0.9957 suggests that a few person entities were missed by the NER system.
        - ORGANIZATION Entities: Recall of 0.9874 indicates a small number of missed organization entities.
        - LOCATION Entities: Perfect precision and recall imply all location entities were correctly identified.
    - Fanwiki Data:

        - Perfect scores across all metrics suggest that the NER system effectively recognized all entities in the Fanwiki text.

9. Use of AI Generators in This Assessed Task
- Used ChatGPT
- Helped on fixing some errors while running.
Example of usage:
"  File "/workspaces/COMP8240-NER-Task1/extract-wikipedia.py", line 3, in <module>
    wiki_wiki = wikipediaapi.Wikipedia('en')
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.python/current/lib/python3.12/site-packages/wikipediaapi/__init__.py", line 167, in __init__
    raise AssertionError(
AssertionError: Please, be nice to Wikipedia and specify user agent - https://meta.wikimedia.org/wiki/User-Agent_policy. Current user_agent: 'en' is not sufficient." 


Respond: 
"It looks like the error is due to not setting a proper user agent when initializing the Wikipedia object from the wikipediaapi library. Wikipedia requires a user agent that describes the purpose of your bot, as stated in their User-Agent policy.

To fix this, you'll need to specify a user agent that includes details about your application, why you're accessing the API"