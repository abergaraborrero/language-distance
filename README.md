# language-distance
Script to calculate a self-defined Levenshtein distance between languages based on phonological features from an array of transcriptions of Swadesh lists.

The input file should be a .txt file. This file should be a table (elements separated by Tab key) containing the IPA transcriptions of a word list. Every column will correspond to a language. The first row must already be the first word of the wordlist. See example.txt

All files (operators.txt, features.txt and the file containing the Swadesh list should be stored in the same directory as the main script).

The formula used to calculate the distance is self-made. Check algorithm_formula_scheme_cat.pdf

DISCLAIMER: This script has been created to be applied on a handful of languages. However, there may be diacritics or characters missing. 
