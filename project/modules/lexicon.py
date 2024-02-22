import pandas as pd
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

# Function to load NRC Emotion Lexicon and VADER sentiment analyzer
def load_nrc_emotion_lexicon():
    url = 'https://drive.google.com/file/d/1NGU4J7mhlqdJplLuVpjQJdq5OD5QTYGd/view?usp=sharing'
    file_id = url.split('/')[-2]
    read_url = 'https://drive.google.com/uc?id=' + file_id

    lexicon = pd.read_csv(read_url)
    analyzer = SentimentIntensityAnalyzer()

    return (analyzer, lexicon)

# Function to perform sentiment analysis using VADER
def get_sentiment(tweet):
    analyzer = load_nrc_emotion_lexicon()[0]
    sentiment = analyzer.polarity_scores(tweet)
    compound_score = sentiment['compound']
    return compound_score

# Function to categorize sentiment based on VADER score
def categorize_sentiment(score):
    if score < 0:
        return 'negative'
    elif score > 0:
        return 'positive'
    else:
        return 'neutral'

# Function to perform emotion detection using the lexicon
def detect_emotion(tweet):
    emotions = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0, 'trust': 0}

    words = tweet.lower().split()
    emotion_col = set(emotions.keys())
    lexicon = load_nrc_emotion_lexicon()[0]
    for word in words:
        matches = lexicon[(lexicon['French Word'] == word)]
        if not matches.empty:
            for emotion in emotion_col:
                emotions[emotion] += matches[emotion].iloc[0]

    if all(value == 0 for value in emotions.values()):
        return None

    predominant_emotion = max(emotions, key=emotions.get)

    return predominant_emotion

# Function to extract positive sentences from a list of sentences based on sentiment
def from_text_to_positive_sentences(list_sentences):
    positive_sentences = []
    for sentence in list_sentences:
        if get_sentiment(sentence) >= 0:
            positive_sentences.append(sentence)
    return positive_sentences
