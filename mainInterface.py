# Imports --------------------------------------------------------------

import textExtraction
import textCleaning
import patternSearching

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

# GUI ------------------------------------------------------------------

class TextSearchingToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Searching Tool")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        self.currentFilePath = None
        self.trie = None  # Store Trie for autocomplete
        self.suggestionListbox = None  # Store autocomplete listbox reference
        self.createWidgets()

    def createWidgets(self):
        # Main title
        titleFrame = tk.Frame(self.root, bg='#f0f0f0')
        titleFrame.pack(pady=10)
        
        titleLabel = tk.Label(titleFrame, text="Text Searching Tool", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titleLabel.pack()

        subtitleLabel = tk.Label(titleFrame, text="Find any word occurences in various types of files.", 
                                 font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        subtitleLabel.pack()
        
        secondarySubtitleLabel = tk.Label(titleFrame, 
                                          text="(Supports .pdf, .docx, .xlsx, .pptx, .txt, .csv, .json, .yaml, .xml, .md, .html, .py, .js, .java, .c, .cpp, .rb, .sh)",
                                          font=('Arial', 8), bg='#f0f0f0', fg='#7f8c8d')
        secondarySubtitleLabel.pack()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # File tab
        self.fileFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.fileFrame, text="File")
        self.createFileTab()
        
        # Searching tab
        self.searchFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.searchFrame, text="Text Search")
        self.createSearchTab()

        """# Help tab
        self.helpFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.helpFrame, text="Help")
        self.createHelpTab()"""
        
    def createFileTab(self):
        # Main frame
        mainFrame = ttk.Frame(self.fileFrame)
        mainFrame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Instructions
        instructionLabel = ttk.Label(mainFrame, 
                                     text="Select a file to start search.",
                                     font=('Arial', 12))
        instructionLabel.pack(anchor='w', pady=(5, 0))
        
        # File selection frame
        fileFrame = ttk.Frame(mainFrame)
        fileFrame.pack(fill='x', pady=10)
        
        # Browse button
        browseButton = ttk.Button(fileFrame,
                                  text="Browse File",
                                  command=self.browseFile)
        browseButton.pack(side='left', padx=(0, 10))
        
        # Drag & Drop
        dropFrame = tk.Frame(mainFrame, 
                            bg='#ecf0f1', 
                            relief='ridge', 
                            borderwidth=2)
        dropFrame.pack(fill='x', pady=(0, 10))
        
        dropLabel = tk.Label(dropFrame, 
                            text="📁 Or drag & drop a file here.\n",
                            font=('Arial', 11),
                            bg='#ecf0f1',
                            fg='#7f8c8d',
                            height=0)
        dropLabel.pack(pady=10)
        
        # Register drag & drop
        dropFrame.drop_target_register(DND_FILES)
        dropFrame.dnd_bind('<<Drop>>', self.handleDrop)
        
        # Selected file path display
        self.filePathLabel = ttk.Label(fileFrame,
                                        text="No file selected.",
                                        font=('Arial', 10),
                                        foreground='#7f8c8d',
                                        background='#ecf0f1',
                                        anchor='w')
        self.filePathLabel.pack(side='left', fill='x', expand=True)
        infoFrame = ttk.LabelFrame(mainFrame, text="File Information", padding=10)
        infoFrame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.fileInfoText = scrolledtext.ScrolledText(infoFrame, 
                                                    height=15, 
                                                    font=('Courier', 9),
                                                    wrap=tk.WORD)
        self.fileInfoText.pack(fill='both', expand=True)
        self.fileInfoText.insert('1.0', "Select a file to view its information...")
        self.fileInfoText.config(state='disabled')
        
    def browseFile(self):
        fileTypes = [("All Supported Files", 
                      "*.txt *.csv *.json *.yaml *.xml *.md *.html *.py *.js *.java *.c *.cpp *.rb *.sh *.docx *.xlsx *.pptx *.pdf"),
                     ("Document Files", "*.docx *.xlsx *.pptx *.pdf"),
                     ("Text Files", "*.txt *.md"),
                     ("Code Files", "*.py *.js *.java *.c *.cpp *.rb *.sh *.html"),
                     ("All Files", "*.*")]
        
        # Open file dialog
        filePath = filedialog.askopenfilename(
            title="Select a File",
            filetypes=fileTypes,
            initialdir="." # Start in current directory
        )
        
        if filePath:
            self.currentFilePath = filePath
            self.filePathLabel.config(text=filePath, foreground="#00a105", font=('Arial', 10))
            self.displayFileInfo(filePath)
            self.buildTrie()  # Build Trie when file is loaded
            self.refreshSearchTab()  # Rebuild search tab
            messagebox.showinfo("Success.", f"Selected file:\n{filePath}")
            
    def displayFileInfo(self, filePath):
        self.fileInfoText.config(state='normal')
        self.fileInfoText.delete('1.0', tk.END)
        
        try:
            fileSize = os.path.getsize(filePath)
            fileName = os.path.basename(filePath)
            fileExtension = os.path.splitext(fileName)[1]
            
            info = f"File Name: {fileName}\n"
            info += f"File Path: {filePath}\n"
            info += f"File Extension: {fileExtension}\n"
            info += f"File Size: {fileSize/1024:.2f} KB\n\n"
            
            self.fileInfoText.insert('1.0', info)
        except Exception as e:
            self.fileInfoText.insert('1.0', f"Could not retrieve file information:\n{str(e)}")
        
        self.fileInfoText.config(state='disabled')
        
    def handleDrop(self, event):
        # Remove curly braces (tkinterdnd2 format)
        filePath = event.data.strip('{}').strip()

        # Handle multiple files (takes only the first one)
        if '} {' in event.data:
            filePath = event.data.split('} {')[0].strip('{}').strip()
        
        # Validate that file exists
        if not os.path.exists(filePath):
            messagebox.showerror("Error", 
                                 f"File not found:\n{filePath}")
            return
            
        supportedExtensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', 
                               '.csv', '.json', '.yaml', '.xml', '.md', 
                               '.html', '.py', '.js', '.java', '.c', 
                               '.cpp', '.rb', '.sh']

        fileExtension = os.path.splitext(filePath)[1].lower()
        print(fileExtension)

        if fileExtension not in supportedExtensions:
            messagebox.showerror("Error", 
                                 f"Unsupported file type.")
            return
        
        # Processing
        self.currentFilePath = filePath
        self.filePathLabel.config(text=filePath, foreground="#00a105", font=('Arial', 10))
        self.displayFileInfo(filePath)
        self.buildTrie()  # Build Trie when file is loaded
        self.refreshSearchTab()  # Rebuild search tab
        messagebox.showinfo("Success.", f"Selected file:\n{os.path.basename(filePath)}")
    
    def buildTrie(self):
        if not self.currentFilePath:
            return
        
        try:
            self.trie = patternSearching.buildTrieFromFile(self.currentFilePath)
            print(f"Trie built successfully for {self.currentFilePath}")
        except Exception as e:
            print(f"Error building Trie: {str(e)}")
            self.trie = None
    
    def createSearchTab(self):
        # Main frame
        mainFrame = ttk.Frame(self.searchFrame)
        mainFrame.pack(fill='both', expand=True, padx=20, pady=20)

        if not self.currentFilePath:
            warningLabel = tk.Label(mainFrame,
                                    text="No file selected. Please select a file in the 'File' tab to start searching.",
                                    font=('Arial', 11),
                                    fg="#282828",
                                    justify='center')
            warningLabel.pack(pady=40)
            return

        # Current file display
        fileLabel = ttk.Label(mainFrame, 
                             text=f"Searching in: {os.path.basename(self.currentFilePath)}",
                             font=('Arial', 10, 'bold'))
        fileLabel.pack(anchor='w', pady=(0, 10))
        
        # Select algorithm for searching
        algorithmFrame = ttk.Frame(mainFrame)
        algorithmFrame.pack(fill='x', pady=(0, 10))
        algorithmSelectionLabel = ttk.Label(algorithmFrame, text="Selected Algorithm")
        algorithmSelectionLabel.pack(side='left', anchor='w')

        self.algorithm_var = tk.StringVar(value="1")  # Default KMP
        algorithmOptions = [
            ("KMP", "1"),
            ("Z-Function", "0")
        ]
        for text, value in algorithmOptions:
            ttk.Radiobutton(algorithmFrame, text=text, variable=self.algorithm_var, value=value).pack(side='left')

        # Text input
        inputLabel = ttk.Label(mainFrame, text="Find in file:")
        inputLabel.pack(anchor='w')
        
        # Entry with autocomplete container
        entryFrame = ttk.Frame(mainFrame)
        entryFrame.pack(fill='x', pady=(5, 10))
        
        self.key_entry = ttk.Entry(entryFrame, font=('Arial', 12))
        self.key_entry.pack(fill='x')
        
        # Bind key release event for autocomplete
        self.key_entry.bind('<KeyRelease>', self.onKeyRelease)
        self.key_entry.bind('<Return>', lambda e: self.searchText())  # Search on Enter
        
        # Autocomplete suggestions listbox (hidden by default)
        self.suggestionListbox = tk.Listbox(entryFrame, 
                                            height=6,
                                            font=('Arial', 10))
        self.suggestionListbox.bind('<<ListboxSelect>>', self.onSuggestionSelect)
        self.suggestionListbox.bind('<Return>', self.onSuggestionSelect)
        
        # Search button
        searchButton = ttk.Button(mainFrame, 
                                 text="Search", 
                                 command=self.searchText)
        searchButton.pack(anchor='w', pady=(0, 10))
        
        # Results area
        resultsFrame = ttk.LabelFrame(mainFrame, text="Search Results", padding=10)
        resultsFrame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.resultsText = scrolledtext.ScrolledText(resultsFrame, 
                                                     height=20, 
                                                     font=('Courier', 9),
                                                     wrap=tk.WORD)
        self.resultsText.pack(fill='both', expand=True)
        self.resultsText.insert('1.0', "Enter text and click 'Search' to find occurrences...")
        self.resultsText.config(state='disabled')
    
    def refreshSearchTab(self):
        # Clear all widgets in search frame
        for widget in self.searchFrame.winfo_children():
            widget.destroy()
        
        # Rebuild the tab
        self.createSearchTab()
        
    def searchText(self):
        if not self.currentFilePath:
            messagebox.showwarning("No file selected.", "Please select a file in the 'File' tab.")
            return
        
        query = self.key_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Empty Query", "Please enter text to search.")
            return
        
        # Update results text
        self.resultsText.config(state='normal')
        self.resultsText.delete('1.0', tk.END)
        self.resultsText.insert('1.0', f"Searching for '{query}'...\n\n")
        
        try:
            occurrences, executionTime, indexes = patternSearching.searchText(self.currentFilePath, query)

            # Check if pattern is invalid
            if occurrences == [] and executionTime == 0.0 and indexes == []:
                self.resultsText.insert(tk.END, 
                    "Invalid search query.\n\n"
                    "The query only contains special characters or symbols\n"
                    "that are removed during text cleaning.\n\n"
                    "For proper text searching, please use queries containing letters or numbers.\n\n"
                    "Examples: 'hello', 'world123', 'a'\n"
                    "Invalid: '$', '@#!', '---'")
            elif len(occurrences) != 0:
                self.resultsText.insert(tk.END, f"{len(occurrences)} matches.\n")
                self.resultsText.insert(tk.END, f"Execution time: {executionTime:.2f} ms\n")
                self.resultsText.insert(tk.END, "At positions:\n")
                for i, position in enumerate(occurrences):
                    self.resultsText.insert(tk.END, f" - {position}\n")
            else:
                self.resultsText.insert(tk.END, "No matches.")
                
        except Exception as e:
            self.resultsText.insert(tk.END, f"Error: {str(e)}")
        
        self.resultsText.config(state='disabled')
    
    def onKeyRelease(self, event):
        # Ignore special keys
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 
                           'Shift_L', 'Shift_R', 'Control_L', 'Control_R'):
            return
        
        if not self.trie:
            return
        
        # Get current text
        text = self.key_entry.get().strip().lower()
        
        # Hide suggestions if text is empty
        if not text:
            self.hideSuggestions()
            return
        
        # Try exact matching
        suggestions = self.trie.getSuggestions(text, limit=6, fuzzy=False)
        
        # Try fuzzy matching (if no exact match exists)
        if not suggestions and len(text) >= 3:
            fuzzy_results = self.trie.getSuggestions(text, limit=6, fuzzy=True, maxErrors=1)
            # Sort by edit distance (lower distance = better match)
            if fuzzy_results:
                fuzzy_results.sort(key=lambda x: x[1])  # x[1] is the distance
                suggestions = [word for word, dist in fuzzy_results]  # Extract just the word
        
        if suggestions:
            self.showSuggestions(suggestions)
        else:
            self.hideSuggestions()
    
    def showSuggestions(self, suggestions):
        self.suggestionListbox.delete(0, tk.END)
        
        for suggestion in suggestions:
            self.suggestionListbox.insert(tk.END, suggestion)
        
        # Show the listbox
        if not self.suggestionListbox.winfo_ismapped():
            self.suggestionListbox.pack(fill='x', pady=(0, 10))
    
    def hideSuggestions(self):
        if self.suggestionListbox and self.suggestionListbox.winfo_ismapped():
            self.suggestionListbox.pack_forget()
    
    def onSuggestionSelect(self, event):
        if not self.suggestionListbox.curselection():
            return
        
        # Get selected suggestion
        index = self.suggestionListbox.curselection()[0]
        selected = self.suggestionListbox.get(index)
        
        # Update entry
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, selected)
        
        # Hide suggestions
        self.hideSuggestions()
        
        # Focus back to entry
        self.key_entry.focus_set()

# Main -----------------------------------------------------------------

window = TkinterDnD.Tk()

app = TextSearchingToolGUI(window)

# Center window
window.update_idletasks()
x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
window.geometry(f"+{x}+{y}")

window.mainloop()
