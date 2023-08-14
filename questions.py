import nltk
import sys,os
from collections import defaultdict
import string,math

nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as f:
                data[filename] = f.read()
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = word_tokenize(document.lower())
    return [word for word in tokens if word not in string.punctuation and word not in stopwords.words("english")]



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_documents = len(documents)
    idfs = defaultdict(float)
    words_in_docs = defaultdict(set)

    for doc, words in documents.items():
        for word in words:
            words_in_docs[word].add(doc)
    
    for word, docs_containing_word in words_in_docs.items():
        idfs[word] = math.log(total_documents / len(docs_containing_word))
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = defaultdict(float)
    for filename, words in files.items():
        for word in query:
            tf = words.count(word)
            tf_idfs[filename] += tf * idfs[word]

    sorted_files = sorted(tf_idfs.keys(), key=lambda x: tf_idfs[x], reverse=True)
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = defaultdict(float)
    for sentence, words in sentences.items():
        word_set = set(words)
        for word in query:
            if word in word_set:
                scores[sentence] += idfs[word]
        
        # Calculate the "Query Term Density" for tie-breaking
        count = sum(1 for word in words if word in query)
        scores[sentence] += count / len(words)

    sorted_sentences = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return sorted_sentences[:n]


if __name__ == "__main__":
    main()
