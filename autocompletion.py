"""
Benefits of using a Trie for autocompletion:
- Efficient prefix matching
- Returns matches quickly
- Less operations than binary search on an ordered list

"""

# Classes & Functions --------------------------------------------------

class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.isEndOfWord = True

    def collectWords(self, node, currentWord, suggestions, limit):
        if len(suggestions) >= limit:
            return
        if node.isEndOfWord:
            suggestions.append(currentWord)
        for char, childNode in node.children.items():
            self.collectWords(childNode, currentWord + char, 
                              suggestions, limit)
            
    def getSuggestions(self, prefix, limit=10, fuzzy=False, maxErrors=1):
        # Handle empty prefix
        if not prefix:
            return []
        
        if fuzzy:
            # Use fuzzy matching with error tolerance
            suggestions = []
            self.fuzzySearch(self.root, prefix, "", maxErrors, suggestions, limit)
            return suggestions[:limit]
        else:
            # Exact prefix matching (original behavior)
            node = self.root
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
            suggestions = []
            self.collectWords(node, prefix, suggestions, limit)
            return suggestions[:limit]
    
    def fuzzySearch(self, node, target, current, maxErrors, suggestions, limit):
        if len(suggestions) >= limit:
            return
        
        # If current word is complete and close enough to target
        if node.isEndOfWord and len(current) > 0:
            distance = self.editDistance(current, target)
            if distance <= maxErrors:
                suggestions.append((current, distance))
        
        # Explore all children
        for char, childNode in node.children.items():
            self.fuzzySearch(childNode, target, current + char, 
                           maxErrors, suggestions, limit)
    
    def editDistance(self, word1, word2):
        # Calculate Levenshtein distance (minimum edits to transform word1 to word2).

        m, n = len(word1), len(word2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all chars from word1
        for j in range(n + 1):
            dp[0][j] = j  # Insert all chars from word2
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]  # No operation needed
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # Delete from word1
                        dp[i][j-1],      # Insert into word1
                        dp[i-1][j-1]     # Substitute
                    )
        return dp[m][n]