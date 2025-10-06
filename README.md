# language-distance
Script to calculate a self-defined Levenshtein distance between languages based on phonological features from an array of transcriptions of Swadesh lists.

The input file should be a .txt file. This file should be a table (elements separated by Tab key) containing the IPA transcriptions of a word list. Every column will correspond to a language. The first row must already be the first word of the wordlist. See example.txt

The formula used to calculate the distance is self-made. 

DISCLAIMER: This script has been created to be applied on a handful of languages. However, there may be diacritics or characters missing. 
