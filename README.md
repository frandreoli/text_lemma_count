# Introduction

This project consists of two Python modules and a Jupyter Notebook designed to process text extracted from PDF files. The code allows to import and read text from PDFs, to then analyze the text and count word lemmas. The provided modules rely on popular Python libraries such as `pypdf`, `pandas`, and `simplemma`.

## Overview of the problem

To design an automated text analysis from PDFs, we addressed the following checklist:
1. Extracting structured text efficiently from multi-page documents.
2. Processing and analyzing the text, including tokenization, lemmatization, and counting unique lemmas.
3. Handling diverse languages and noisy data with modular design.

These points are accomplished via the two modules, `pdf_local_module` and `text_local_module`, which can be directly used inside the Jupyter Notebook that is provided in the repository.

 
## Module: `pdf_local_module`

The `pdf_local_module` provides a class `pdf_analyzer` to facilitate text extraction from PDF files. It uses the `pypdf` library for reading and processing the documents.

### Initialization

The `pdf_analyzer` object can be initialized as follows:

```python
pdf_analyzer(path: str, *, verbose: bool = True)
```

The relevent arguments of the class are given by:
- `path`: The path to the PDF file.
- `verbose`: An optional flag for logging messages during initialization and operations.

Upon initialization the PDF file is read using `pypdf` and some metadata are stored, which can be retrieved via the attributes:

- `file_path` *(read-only)*: Path to the input PDF file.
- `n_pages` *(read-only)*: Total number of pages in the document.

### Method: `extract`

```python
extract(i_start=None, j_end=None, *, force=False, merge=False)
```

- `i_start`, `j_end`: Indices (1-based) for page extraction. If only the starting index `i_start` is provided, only one page is extracted, corresponding to its value. If both are omitted, the code extracts all pages. Moreover, `j_end` can take negative indexing, to count backwards from the last page (i.e. -1). Finally, is specific pages are needed for the extraction, one can feed the method with such a list of pages, e.g. `extract([1,6,8])`.
- `force`: If `True`, it forces re-extraction of pages even if they were already cached. Otherwise, cached pages are not extracted twice.
- `merge`: If `True`, it combines extracted pages into a single text string, which is returned as outcome. Otherwise, the outcome is a list of text strings, each corresponding to one extracted page.
 
The method returns either a list of page-wise extracted text (default), or a single merged string (if `merge=True`).

Example:

```python
analyzer = pdf_analyzer("example.pdf")
text = analyzer.extract(1, 3, merge=True)
```
 

## Module: `text_local_module`


The `text_local_module` provides a class `text_analyzer` for processing and analyzing text. It supports:
1. Text cleaning and tokenization.
2. Language detection.
3. Lemmatization.
4. Word and lemma counting.

### Initialization

The `text_analyzer` object can be initialized as follows:

```python
text_analyzer(text: str, language=None, *, verbose: bool = True)
```

The relevent arguments of the class are given by:

- `text`: The raw text that must be analyzed.
- `language`: An optional language specifier for lemmatization. Auto-detection if omitted.
- `verbose`: An optional flag for logging messages during initialization and operations.

Upon initialization the raw text is stored and can be accessed using:

- `text_raw` *(read-only)*: Original input text.
- `languages` *(read-only)*: Overall list of supported languages for lemmatization.

#### Key Methods

1. `text_process`: This method cleans and normalizes the text (e.g., removes punctuation).
2. `words_split`: This method splits text into tokens.
3. `word_count(key_word = None, *, dict = False)`:
   - It counts occurrences of each word if no argument `key_word` is provided. Otherwise, it counts the occurrence of only that specific word.
   - It returns the results as either a dictionary (if `dict = True`) or a `pandas` DataFrame (if `dict = False`).
4. `language_detect`:
   - It attempts to automatically detects the language of the input text. When this is done, the attribute `.language` is automatically updated with the language found. The method then returns a tuple with the language code, and a confidence value (between 0 and 1).
5. `lemmatize`:
   - Lemmatizes the words and returns a DataFrame with raw words, lemmas, and counts.
6. `lemma_count`:
   - Aggregates and counts unique lemmas, returning a DataFrame.

Example:

```python
analyzer = text_analyzer("Sample text goes here.")
analyzer.language_detect()
lemmas = analyzer.lemmatize()
```

---

# Notebook: `lemma_count.ipynb`

The Jupyter Notebook demonstrates how to integrate the modules for text analysis. It guides the user through:
1. Importing and using `pdf_local_module` to extract text from a PDF.
2. Analyzing the text with `text_local_module` to perform tokenization, lemmatization, and counting.

**Usage Example**:
- Load a PDF using `pdf_analyzer`.
- Extract text and analyze it using `text_analyzer`.
- Generate lemma counts and visualize results.

---

# References

For additional details, refer to:
- `pypdf` Documentation**: [pypdf](https://pypi.org/project/pypdf/)
- `simplemma` Documentation**: [simplemma](https://github.com/adbar/simplemma)
- `pandas` Documentation**: [pandas](https://pandas.pydata.org/)


