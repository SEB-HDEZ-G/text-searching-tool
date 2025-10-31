"""
cleaning properties:
- convert text to lowercase
- remove punctuation and special characters
- remove extra whitespaces

"""

# imports ------------------------------------------------------------

import textExtraction
import re
"""
regex module for text cleaning
 - provides tools to search, match, split and replace text base on
 patterns
"""

# functions ------------------------------------------------------------

def cleanText(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text