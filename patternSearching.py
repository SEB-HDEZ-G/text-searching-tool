"""
Steps for text searching:
- Extract text
- Pass extracted text for cleaning
- Pass cleaned text to Pattern Matching function
- Search for text and show:
    - Occurences
    - Exact word positions

"""

# Imports ------------------------------------------------------------

import textExtraction
import textCleaning
import autocompletion
import time

# Functions ------------------------------------------------------------

def zFunction(S):
    n = len(S)
    right, left = 0, 0
    z = [0] * n
    
    for i in range(1, n - 1):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and S[z[i]] == S[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left = i
            right = i + z[i]
    return z

def findOccurrences(pattern, text):
    m = len(pattern)
    concatenated = pattern + "$" + text
    z = zFunction(concatenated)
    occurrences = []
    for i in range(m + 1, len(concatenated)):
        if z[i] == m:
            occurrences.append(i - m - 1)
    return occurrences

def calculateLPS(pattern):
    prefixes = [0] * len(pattern)
    j = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            prefixes[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                prefixes[i] = 0
                i += 1
            else:
                j = prefixes[j - 1]
    return prefixes

def kmp(pattern, text):
    lps = calculateLPS(pattern)
    m, n = len(pattern), len(text)
    i = j = 0
    occurrences = []
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            # Match found
            occurrences.append(i - j)
            # Continue searching for more occurrences
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j == 0:
                i += 1
            else:
                j = lps[j - 1]
    return occurrences

def searchText(filePath, pattern, algoritmSelected=1):
    extractedText = textExtraction.chooseExtractionMethod(filePath)
    cleanedText = textCleaning.cleanText(extractedText)
    cleanedPattern = textCleaning.cleanText(pattern).strip()
    
    # Validate cleaned pattern is not empty
    if not cleanedPattern:
        return [], 0.0, []  # Return empty results for invalid pattern
    
    indexes = []
        
    startTime = time.perf_counter()
    if algoritmSelected == 0:
        occurrences = findOccurrences(cleanedPattern, cleanedText)
    else:
        occurrences = kmp(cleanedPattern, cleanedText)
    endTime = time.perf_counter()
    executionTime = (endTime - startTime) * 1000  # Milliseconds

    if len(occurrences) != 0:
        for i, position in enumerate(occurrences):
            indexes.append(position)

    return occurrences, executionTime, indexes    

def buildTrieFromFile(filePath):
    extractedText = textExtraction.chooseExtractionMethod(filePath)
    cleanedText = textCleaning.cleanText(extractedText)
    words = textCleaning.separateWords(cleanedText)
    uniqueWords = textCleaning.identifyUniqueWords(words)
    
    trie = autocompletion.Trie()
    for word in uniqueWords:
        trie.insert(word)
    
    return trie

# Testing --------------------------------------------------------------

"""testingKey = 1  # 0-17


0: .txt, 1: .csv, 2: .json, 3: .yaml, 4: .xml, 5: .md, 6: .html, 7: .py, 
8: .js, 9: .java, 10: .c, 11: .cpp, 12: .rb, 13: .sh, 14: .docx, 
15: .xlsx, 16: .pptx, 17: .pdf

fileFormats = ['.txt', '.csv', '.json', '.yaml', '.xml', '.md',
               '.html', '.py', '.js', '.java', '.c', '.cpp', '.rb', '.sh',
               '.docx', '.xlsx', '.pptx', '.pdf']

# Extract and print the text
filePath = 'testFiles/test' + fileFormats[testingKey]
print(f"Testing word searching in: {filePath}")
print("=" * 60)

extractedText = textExtraction.chooseExtractionMethod(filePath)
cleanedText = textCleaning.cleanText(extractedText)

pattern = input("\nSearch for word: ")
cleanedPattern = textCleaning.cleanText(pattern).strip()

startTime = time.perf_counter()
occurences = findOccurrences(cleanedPattern, cleanedText)
endTime = time.perf_counter()
executionTime = (endTime - startTime) * 1000  # Milliseconds

if len(occurences) != 0:
    print(f"\n{len(occurences)} matches.")
    print(f"Execution time: {executionTime:.2f} ms")
    print("At positions:")
    for i, position in enumerate(occurences):
        textSection = cleanedText[position:position + 10]
        print(f"Index {position}: {textSection}")
else:
    print("No matches.")"""