"""
cleaning properties:
- convert text to lowercase
- remove punctuation and special characters
- remove extra whitespaces

"""

# Imports ------------------------------------------------------------

import textExtraction
import re
import unicodedata

"""
regex module for text cleaning
 - provides tools to search, match, split and replace text base on
 patterns
"""

# Functions ------------------------------------------------------------

def cleanText(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove accents
    """
    NFD = Normalization Form Decomposition
    Separates 'é' into 'e' + accent mark
    Mn = Mark, nonspacing
    """
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text 
                   if unicodedata.category(char) != 'Mn')
    
    # Remove puntuation and special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Individual word separation
def separateWords(text):
    return text.split()

# Unique word identification
def identifyUniqueWords(text):
    uniqueWords = []
    for word in text:
        if word not in uniqueWords:
            uniqueWords.append(word)
    return uniqueWords

# Testing --------------------------------------------------------------

"""testingKey = 17  # 0-17

0: .txt, 1: .csv, 2: .json, 3: .yaml, 4: .xml, 5: .md, 6: .html, 7: .py, 
8: .js, 9: .java, 10: .c, 11: .cpp, 12: .rb, 13: .sh, 14: .docx, 
15: .xlsx, 16: .pptx, 17: .pdf

fileFormats = ['.txt', '.csv', '.json', '.yaml', '.xml', '.md',
               '.html', '.py', '.js', '.java', '.c', '.cpp', '.rb', '.sh',
               '.docx', '.xlsx', '.pptx', '.pdf']

# Extract and print the text
filePath = 'testFiles/test' + fileFormats[testingKey]
print(f"Testing extraction from: {filePath}")
print("=" * 60)

extractedText = textExtraction.chooseExtractionMethod(filePath)
print(extractedText[:500])

# Clean extracted text
print("\nCleaned text")
print("=" * 60)

cleanedText = cleanText(extractedText)
print(cleanedText[:500])

# Separate individual words
print("\nSeparated text")
print("=" * 60)

separatedText = separateWords(cleanedText)
print(separatedText[:500])

# Print unique words
print("\nSeparated text")
print("=" * 60)

uniqueWords = identifyUniqueWords(separatedText)
print(uniqueWords)"""