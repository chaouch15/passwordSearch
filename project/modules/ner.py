from flair.data import Sentence
from flair.models import SequenceTagger

# Load Flair NER model
tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")

# Function to retrieve Named Entities from a sentence using Flair NER
def retrieve_ner(sentence_string):
    sentence = Sentence(sentence_string)

    # Predict entities
    tagger.predict(sentence)

    # Initialize a dictionary for storing unique entities for each NER category
    predicted_map = {
        'CARDINAL': set(),
        'DATE': set(),
        'EVENT': set(),
        'FAC': set(),
        'GPE': set(),
        'LANGUAGE': set(),
        'LAW': set(),
        'LOC': set(),
        'MONEY': set(),
        'NORP': set(),
        'ORDINAL': set(),
        'ORG': set(),
        'PERCENT': set(),
        'PERSON': set(),
        'PRODUCT': set(),
        'QUANTITY': set(),
        'TIME': set(),
        'WORK_OF_ART': set()
    }

    # Populate the dictionary with unique entities
    for entity in sentence.get_spans('ner'):
        text = entity.text.lower()
        predicted_map[entity.tag].add(text)

    return predicted_map
