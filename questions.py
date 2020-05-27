import nltk
import sys
import os
import string
import math

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
    mapping_directory = dict()


    
    path = os.path.join(os.path.abspath(os.getcwd()), directory)
    file_dir = os.listdir(path)
    for filename in file_dir:
        with open(os.path.join(path, filename), encoding="utf8") as f:
            s = f.read()
            mapping_directory[filename] = s

    return mapping_directory

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words_list = list()
    
    words_list_temp = ([
        word.lower() for word in
        nltk.word_tokenize(document)
        if any(c.isalpha() for c in word)
    ])

    for word in words_list_temp:
        if word not in nltk.corpus.stopwords.words("english"):
            words_list.append(word)

    return words_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_values = dict()
    combined_list = list()
    word_counter = 0

    for key, value in documents.items():
        word_counter += len(value)
        for x in value:
            if x not in combined_list:
                combined_list.append(x)
    

    for word in combined_list:
        counter = 0
        for key in documents:
            if word in documents[key]:
                counter += 1
        idf_values[word] = math.log(len(documents.values()) / counter)

    return idf_values

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    result_list = list()

    for filename in files:
        score = 0
        for word in query:
            if word in idfs:
                counter = 0
                for w in files[filename]:
                    if w == word:
                        counter =+ 1
                        
                score += idfs[word] * counter / len(files[filename])
        result_list.append((filename, score))

    result_list.sort(key=lambda x: -x[1])
    result = list()
    for i in range(n):
        result.append(result_list[i][0])

    return result


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    result_list = list()
    for sentence in sentences:
        idf_value = 0
        density = 0
        for word in query:
            if word in sentences[sentence]:
                idf_value += idfs[word]
            score = 0
            for w in sentences[sentence]:
                if w == word:
                    score += 1
            density = score / len(sentences[sentence])    
        result_list.append((sentence, idf_value, density))
        
    result_list = sorted(result_list, key=lambda x: x[2], reverse=True)
    result_list = sorted(result_list, key=lambda x: x[1], reverse=True)

    result = list()
    for i in range(n):
        result.append(result_list[i][0])
    
        return result


if __name__ == "__main__":
    main()
