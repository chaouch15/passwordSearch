import spacy
import nltk

# Download NLTK resources if needed
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("fr_core_news_sm")

# Define stopwords and stemmer
stopWords = set(nltk.corpus.stopwords.words('french'))
stemmer = nltk.stem.snowball.SnowballStemmer(language='french')

# Function to clean sentence by removing stopwords
def cleaning_sentence(sentence):
    clean =[]
    for token in nlp(sentence):
        if token.text not in stopWords:
            clean.append(token.text)
    return clean

# Function to reduce words to their root (stemming)
def racine(sentence):
    return [stemmer.stem(X.text) for X in nlp(sentence)]

# Function to classify words by grammatical type
def gramm(sentence):
    return [(X, X.pos_) for X in nlp(sentence)]

# Function to extract roots and types of non-stopwords from a sentence
def extract_racines(sentence):
    nl = nlp(sentence)
    clean =[]
    for token in nlp(sentence):
        if token.text not in stopWords:
            clean.append(token)
    return [(X.text,X.pos_) for X in clean]

# Function to filter words and keep only nouns and adjectives
def filter_words(list_words):
    ret = []
    for words in list_words:
        if words[1] in ['ADJ','PROPN','NOUN']:
            ret.append(words[0])
    return ret
