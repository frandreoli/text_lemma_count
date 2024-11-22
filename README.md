# Introduction

This project consists of two Python modules and a Jupyter Notebook designed to process text extracted from PDF files. The workflow involves importing and reading text from PDFs, analyzing the text, and counting word lemmas. The provided modules ensure flexibility, modularity, and compatibility with popular Python libraries such as `pypdf`, `pandas`, and `simplemma`.

## Overview of the problem

Automated text analysis from PDFs often involves challenges such as:
1. Extracting structured text efficiently from multi-page documents.
2. Processing and analyzing the text, including tokenization, lemmatization, and counting unique lemmas.
3. Handling diverse languages and noisy data with modular design.

The two modules, **`pdf_local_module`** and **`text_local_module`**, address these challenges. The workflow is exemplified in the accompanying Jupyter Notebook, enabling on-the-spot exploration and integration.

---

# Module: `pdf_local_module`

### Overview

The **`pdf_local_module`** provides a class `pdf_analyzer` to facilitate text extraction from PDF files. It uses the `pypdf` library for reading and processing the documents.

### Class: `pdf_analyzer`

#### Initialization

```python
pdf_analyzer(path: str, verbose: bool = True)
```

-
-

Upon initialization:
- The PDF file is read using `pypdf`.
- Metadata, such as the number of pages, is stored.

### Properties

- **`file_path`** *(read-only)*: Path to the input PDF file.
- **`n_pages`** *(read-only)*: Total number of pages in the document.

### Method: `extract`

```python
extract(i_start=None, j_end=None, *, force=False, merge=False)
```

- **`i_start`**, **`j_end`**: Indices (1-based) for page extraction. If omitted, extracts all pages.
- **`force`**: Forces re-extraction of pages even if already cached.
- **`merge`**: Combines extracted pages into a single text string.

**Returns**:
- List of extracted text (default) or a single merged string (if `merge=True`).

**Example**:
```python
analyzer = pdf_analyzer("example.pdf")
text = analyzer.extract(1, 3, merge=True)
```

---

### Overview of `text_local_module`

The **`text_local_module`** provides a class `text_analyzer` for processing and analyzing text. It supports:
1. Text cleaning and tokenization.
2. Language detection.
3. Lemmatization.
4. Word and lemma counting.

### Class: `text_analyzer`

#### Initialization

```python
text_analyzer(text: str, language=None, *, verbose: bool = True)
```

- **`text`**: Raw text for analysis.
- **`language`**: Optional language specifier for lemmatization. Auto-detection if omitted.
- **`verbose`**: Logs messages during processing.

#### Properties

- **`text_raw`** *(read-only)*: Original input text.
- **`languages`** *(read-only)*: List of supported languages.

#### Key Methods

1. **`text_process`**: Cleans and normalizes text (e.g., removes punctuation).
2. **`words_split`**: Splits text into tokens.
3. **`word_count`**:
   - Counts occurrences of each word.
   - Returns results as a dictionary or `pandas` DataFrame.
4. **`language_detect`**:
   - Detects the language of the input text.
5. **`lemmatize`**:
   - Lemmatizes the words and returns a DataFrame with raw words, lemmas, and counts.
6. **`lemma_count`**:
   - Aggregates and counts unique lemmas, returning a DataFrame.

**Example**:
```python
analyzer = text_analyzer("Sample text goes here.")
analyzer.language_detect()
lemmas = analyzer.lemmatize()
```


