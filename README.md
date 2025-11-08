# Seb's Text Searching Tool (Version 1.4.0)
A **Tkinter-based** tool GUI that allows for searching text across various types of files.

## Table of Contents
- [Features](#features)
  - [Supported File Formats](#supported-file-formats)
  - [File Upload](#file-upload)
  - [Text Searching](#text-searching)
  - [Autocompletion & Suggestions](#autocompletion--suggestions)
- [Technologies used](#technologies-used)
  - [Programming language](#programming-language)
  - [Libraries](#libraries)
- [Installation](#installation)
- [Additional Links](#additional-links)

## Features
### Supported File Formats
Supports various types of files:
- PDF files
  > .pdf
- Office documents
  > .docx, .xlsx, .pptx
- Plain & structured text
  > .txt, .csv, .json, .yaml, .xml, .md
- Programming & script files.
  > .html, .py, .js, .java, .c, .cpp, .rb, .sh
### File Upload
- Instant browsing for File Explorer
- **Drag & Drop** functionality for file upload
- Display of basic details for uploaded files
  - File Name
  - File Path
  - File Extension
  - File Size
### Text Searching
- Quick search for short and large files
- Optimized through **linear-time pattern matching** algorithms
  > Z-Algorithm, Knuth–Morris–Pratt (KMP) algorithm
- Algorithm selection setting available at any time
### Autocompletion & Suggestions
- Automatic display of suggestion list for **real-time text input**
- Text input autocompletion (when selecting from suggestion list)
- Optimized with a **Trie (Prefix Tree)** data structure
- Integrated error tolerance with **Fuzzy matching** (edit distance algorithm)
## Technologies used
### Programming language
> Python 3.13.0 (or higher)
### Libraries
- **openpyxl** - Excel spreadsheet (.xlsx) processing
- **os** - File path operations
- **pdfplumber** - PDF text extraction
- **python-docx** - Word document (.docx) processing
- **python-pptx** - PowerPoint presentation (.pptx) processing
- **time** - Performance timing (execution time measurement)
- **tkinter** - Built-in Python GUI toolkit
- **tkinterdnd2** - Drag-and-drop functionality for Tkinter
- **re** - Regular expressions for text cleaning
- **unicodedata** - Unicode character normalization (accent removal)
## Installation
> os, time, tkinter, re and unicodedata are built-in and don't need to be installed separately
Install the required dependencies with a single command:
```bash
pip install openpyxl pdfplumber python-docx python-pptx tkinterdnd2
```
Or install the dependencies one by one:
```bash
pip install openpyxl
```
```bash
pip install pdfplumber
```
```bash
pip install python-docx
```
```bash
pip install python-pptx
```
```bash
pip install pytesseract
```
```bash
pip install tkinterdnd2
```
#### For Linux users
> While many Linux distributions include Tkinter with their default Python installations, some might require the installation of a separate package for it.
> Visit https://stackoverflow.com/questions/4783810/install-tkinter-for-python if you run into issues with TKinter.

## Additional links
- [Z-Algorithm Overview by GeeksForGeeks](https://www.geeksforgeeks.org/dsa/z-algorithm-linear-time-pattern-searching-algorithm/)
- [KMP Algorithm Overview by GeeksForGeeks](https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/)
- [Z-Algorithm and KMP Algorithm Comparison by Medium](https://medium.com/@whyamit404/z-algorithm-vs-kmp-knuth-morris-pratt-f856b4ab062d)
- [Python TKinter Overview](https://www.geeksforgeeks.org/python/python-gui-tkinter/)
- [Fuzzy Matching Algorithms Lecture by Medium](https://medium.com/@m.nath/fuzzy-matching-algorithms-81914b1bc498)
- [Introduction to Levenshtein distance by GeeksForGeeks](https://www.geeksforgeeks.org/dsa/introduction-to-levenshtein-distance/)
