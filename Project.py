# -*- coding: utf-8 -*-
import requests
from pprint import pprint
import os
import pandas as pd
import numpy as np
from flair.data import Sentence
from flair.models import SequenceTagger
import json
import re
import random
from tqdm import tqdm
import spacy
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import itertools

stopWords = set(stopwords.words('french'))
stemmer = SnowballStemmer(language='french')


nlp = spacy.load("fr_core_news_sm")


# mount my Google Drive on the VM

#from google.colab import drive
#drive.mount('/gdrive')

DIR_PROJECT = '/Tous les Codes'
DIR_LEXICON = os.path.join(DIR_PROJECT,'Code Sentiment Analysis/French-NRC-EmoLex.txt')

stopWords.add("n'")
stopWords.add("l'")
stopWords.add("c'")

#takes a sentence as a uniq string, returns a list of words without the stopwords
def cleaning_sentence(sentence):
  clean =[]
  for token in nlp(sentence):
    if token.text not in stopWords:
        clean.append(token.text)
  return clean

  #Supposé réduire les mots à leur racine marche approximativement
def racine(sentence):
    return [stemmer.stem(X.text) for X in nlp(sentence)]

    #classifie par type grammatical
def gramm(sentence):
    return [(X, X.pos_) for X in nlp(sentence)]

    #prends une phrase, vire les stopwords, renvoie la racine et le type des mots restant (note: si le mot est un nom propre, racine et type seront erronés)
def extract_racines(sentence):
  nl = nlp(sentence)
  clean =[]
  for token in nlp(sentence):
    if token.text not in stopWords:
        clean.append(token)
  #return [(stemmer.stem(X.text),X.pos_) for X in clean]
  return [(X.text,X.pos_) for X in clean]

  #trie le resultat de extract_racines pour ne garder que les noms et adjectifs
def filter_words(list_words):
  ret = []
  for words in list_words:
    if words[1] in ['ADJ','PROPN','NOUN']:
       ret.append(words[0])
  return ret



tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")

def Retrieve_NER(sentence_string):
    """
    Retrieve Named Entities from a given sentence using Flair NER.

    Parameters:
    - sentence_string (str): The input sentence.

    Returns:
    - dict: A dictionary containing lists of entities for each NER category.
    """
    sentence = Sentence(sentence_string)

    # Predict entities
    tagger.predict(sentence)

    # Initialize a dictionary for storing unique entities for each category
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
  #TEST:
test = "Mélodie raconte une histoire, qui a eu lieu en 2013, sur son chien, Rex. Elle essaye depuis des années de publier son livre Rainbow, en Europe, plus partiuclièrement en France. C'est vrai qu'elle adore son chien. Elle aime la France du fond du coeur. Mais elle cherche aussi à devenir une star comme Macron."
filter_words(extract_racines(test))
text_to_NER= "Mélodie raconte une histoire, qui a eu lieu en 2013, sur son chien, Rex. Elle essaye depuis des années de publier son livre Rainbow, en Europe, plus partiuclièrement en France. C'est vrai qu'elle adore son chien. Elle aime la France du fond du coeur. Mais elle cherche aussi à devenir une star comme Macron."
NER_to_algebra = Retrieve_NER(text_to_NER)

NER_to_algebra

def Load_NR_Emotio_Lexicon():
    # METHODE 1
    #print('DIR_LEXICON =', DIR_LEXICON)
    #lexicon = pd.read_csv(DIR_LEXICON, sep='\t')

    # METHODE 2
    url = 'https://drive.google.com/file/d/1NGU4J7mhlqdJplLuVpjQJdq5OD5QTYGd/view?usp=sharing'
    file_id = url.split('/')[-2]
    read_url='https://drive.google.com/uc?id=' + file_id
    # read the data
    lexicon = pd.read_csv(read_url)

    # Create an instance of the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    return (analyzer,lexicon)

# Define a function to perform sentiment analysis using VADER
def get_sentiment(tweet):
    analyzer = Load_NR_Emotio_Lexicon()[0]
    sentiment = analyzer.polarity_scores(tweet)
    compound_score = sentiment['compound']
    return compound_score

# Define a function to categorize sentiment based on VADER score
def categorize_sentiment(score):
    if score < 0:
        return 'negative'
    elif score > 0:
        return 'positive'
    else:
        return 'neutral'

# Define a function to perform emotion detection using the lexicon
def detect_emotion(tweet):

    emotions = {'anger': 0, 'anticipation': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0, 'trust': 0}

    words = tweet.lower().split()
    emotion_col = set(emotions.keys())
    lexicon = Load_NR_Emotio_Lexicon()[0]
    for word in words:
        matches = lexicon[(lexicon['French Word'] == word)]
        if not matches.empty:
          for emotion in emotion_col:
            emotions[emotion] += matches[emotion].iloc[0]

    # Check if all emotion values are still zero
    if all(value == 0 for value in emotions.values()):
        return None

    # Determine the predominant emotion
    predominant_emotion = max(emotions, key=emotions.get)

    return predominant_emotion

    #Returns a list of positive sentences from a list of sentences
def from_text_to_positive_sentences(list_sentences):
  positive_sentences = []
  for sentence in list_sentences:
    if get_sentiment(sentence)>0:
      positive_sentences.append(sentence)
  return positive_sentences

def occurrences_NER(list_sentences):
    rows = []
    NER_glob = pd.DataFrame(columns=['CARDINAL','DATE','EVENT','FAC','GPE','LANGUAGE','LAW','LOC','MONEY','NORP','ORDINAL','ORG','PERCENT','PERSON','PRODUCT','QUANTITY','TIME','WORK_OF_ART'])
    for sentence in list_sentences:
        NER = Retrieve_NER(sentence)
        for key, word_list in NER.items():
            for word in word_list:
                new_row = pd.Series(index=NER_glob.columns)
                new_row[key] = word
                rows.append(new_row)
    NER_glob = pd.DataFrame(rows, columns=NER_glob.columns)
    return NER_glob

def decompose():
        #First decompose in sentences
    list_sentences = tokenize.sent_tokenize(input)

    #Second NER directly

    NER_neutral = occurrences_NER(list_sentences)

    #Third Positive processing, only keep positive sentences
    list_positive_sentences = from_text_to_positive_sentences(list_sentences)

    #Fourth NLP process to get nouns, adj
    list_words_NLP =[]
    for sentence in list_positive_sentences:
        list_words_NLP.append(filter_words(extract_racines(sentence)))

    #Five second NER on the positive sentences
    NER_positive = occurrences_NER(list_positive_sentences)

    #Add every result in a biiig dataframe and concacenate similar occurences, count them
    NER_tot = pd.concat([NER_neutral, NER_positive], ignore_index=True)

    #We have the dataframe NER_tot of words by NER category and the list_words_NLP of words

    #here we do a quick data squeezing to add every words from both sets in a new dataframe where there is also the number of occurences.

    # Initialize df_words with word, occurrences, and NER_category columns
    df_words = pd.DataFrame(columns=['word','NER_category','occurrences']) #TASNIM : added the ner_category
    word_counts = pd.Series(list_words_NLP).value_counts()

    # Step 1: Extract words and their occurrences from list_words_NLP
    for word_list in list_words_NLP:
        word_list = [word.lower() for word in word_list]
        word_counts = pd.Series(word_list).value_counts()
        new_df = pd.DataFrame({'word': word_counts.index, 'occurrences': word_counts.values})
        new_df['NER_category'] = 'N/A'  #TASNIM :  Initialize NER category as 'N/A'
        df_words = pd.concat([df_words, new_df], ignore_index=True)

    # TASNIM

    # Step 2: Update NER category for words from NER results in NER_tot
    for idx, row in NER_tot.iterrows():
        for col in NER_tot.columns[1:]:  # Exclude the first column 'NER TOT'
            word = row[col]
            if pd.notnull(word):
                word = word.lower()
                # Update NER category for the corresponding word in df_words
                df_words.loc[df_words['word'] == word, 'NER_category'] = col

    # Step 3: Group by word and NER_category and sum the occurrences
    df_words = df_words.groupby(['word', 'NER_category'], as_index=False)['occurrences'].sum()

    # Step 4: Sort by occurrences in descending order
    df_words = df_words.sort_values(by='occurrences', ascending=False)

    # Step 5: Reset index
    df_words.reset_index(drop=True, inplace=True)

    return (df_words,NER_neutral)


    # MERLIN

    #word_counts = NER_tot.apply(lambda row: row.dropna().iloc[0], axis=1).value_counts()
    #new_df = pd.DataFrame({'word': word_counts.index, 'occurrences': word_counts.values})
    #df_words = pd.concat([df_words, new_df.groupby('word')['occurrences'].sum().reset_index()], ignore_index=True)
    #sum duplicates
    #df_words = df_words.groupby('word', as_index=False)['occurrences'].sum()
    #df_words = df_words.sort_values(by='occurrences', ascending=False)
    #df_words

#Filter df to only allwoed tags
def filter_df_tags(df_words, allowed_tags):
    tag_dict = {tag: [] for tag in allowed_tags}  # Initialize dictionary with allowed tags

    # Iterate over each row in df_words
    for idx, row in df_words.iterrows():
        word = row['word']
        NER_category = row['NER_category']

        # Check if NER category is allowed
        if NER_category in allowed_tags:
            # Append word to the corresponding category in the dictionary
            tag_dict[NER_category].append(word)

    # Remove duplicates from each list
    for tag in tag_dict:
        tag_dict[tag] = list(set(tag_dict[tag]))

    return tag_dict
 
#Filter neutral ner to only allowed tags
def filter_ner_neutral_tags(ner_neutral, allowed_tags):
    tag_dict = {tag: [] for tag in allowed_tags}  # Initialize dictionary with allowed tags

    # Iterate over each row in NER_neutral
    for idx, row in ner_neutral.iterrows():
        for col in ner_neutral.columns:
            word = row[col]
            if pd.notnull(word):
                # Check if NER category is allowed
                if col in allowed_tags:
                    # Append word to the corresponding category in the dictionary
                    tag_dict[col].append(word)

    # Remove duplicates from each list
    for tag in tag_dict:
        tag_dict[tag] = list(set(tag_dict[tag]))

    return tag_dict
 




def generate_passwords(filtered_ner_neutral,filtered_df_words):
    string_dict={}
    string_dict['Name'] = list(set(filtered_ner_neutral.get('PERSON', [])) & set(filtered_df_words.get('PERSON', [])))
    string_dict
    #Create dictionaries
    string_dict = {
        'Name': list(set(filtered_ner_neutral.get('PERSON', [])) & set(filtered_df_words.get('PERSON', []))),
        'Article': ['I', 'my', 'the', 'it', 'we', 'you'],
        'City': list(set(filtered_ner_neutral.get('GPE', [])) & set(filtered_df_words.get('GPE', [])))
        + list(set(filtered_ner_neutral.get('LOC', [])) & set(filtered_df_words.get('LOC', []))),
        'Keyboard': ['qwerty', 'qwe', 'abc', 'asd'],
        'Prepositions': ['to', 'in'],
    }

    digit_dict = {
        'Number': list(set(filtered_ner_neutral.get('CARDINAL', [])) & set(filtered_df_words.get('CARDINAL', [])))
        + [str(i) for i in range(10)],
        'Common': ['123456', '123', '123456789', '12345', '1234', '11', '13', '12345678', '01', '10'],
        'Year': [date[-4:] for date in list(set(filtered_ner_neutral.get('DATE', [])) & set(filtered_df_words.get('DATE', []))) if date[-4:].isdigit()],
    }

    special_dict = {
        'Simple': ['.', '_', '!', '@', '-', ':', '#', '*', '$', ' ', '&', '+', '?', ',', '/'],
        'Combined': ['!!', '.:', '&#', '**', '…', ':', '$$', '__'],
    }

    # Create lists for each dictionary
    string_list = list(itertools.chain.from_iterable(string_dict.values()))
    digit_list = list(itertools.chain.from_iterable(digit_dict.values()))
    special_list = list(itertools.chain.from_iterable(special_dict.values()))
    all_combinations = []

    # Generate combinations of string + special + digits
    combo1 = itertools.product(string_list, special_list, digit_list)
    all_combinations.extend(''.join(comb) for comb in combo1)

    # Generate combinations of string + digits + special
    combo2 = itertools.product(string_list, digit_list, special_list)
    all_combinations.extend(''.join(comb) for comb in combo2)

    # Filter combinations with length >= 8
    valid_passwords = [password for password in all_combinations if len(password) >= 8]

    
   # print("Generated Password Combinations:")
   # i = 0
    #for password in valid_passwords:
     #   print(i , ' : ' , password)
      #  i+=1
        
    return valid_passwords

 


#TEST:
#test = "Mélodie raconte une histoire, qui a eu lieu en 2013, sur son chien, Rex. Elle essaye depuis des années de publier son livre Rainbow, en Europe, plus partiuclièrement en France. C'est vrai qu'elle adore son chien. Elle aime la France du fond du coeur. Mais elle cherche aussi à devenir une star comme Macron."
#filter_words(extract_racines(test))
# Example sentence
#example_sentence = "Fais chier, il pleut. Hier j'ai acheté une baguette. Elle était bonne. Sacré journée que nous avons eu là ! J'aime beaucoup les croissants. Je souffre jour après jour, mais on fait avec. Mes rhumatismes ne vont pas mieux mais merci de t'en soucier. Va crever ! Je suis allé courir ce matin. Il fait tellement chaud, on se croirait au printemps. "
#example_sentence2 = "Mélodie raconte une histoire, qui a eu lieu en 2013, sur son chien, Rex. Elle essaye depuis des années de publier son livre Rainbow, en Europe, plus partiuclièrement en France. C'est vrai qu'elle adore son chien. Elle aime la France du fond du coeur. Mais elle cherche aussi à devenir une star comme Macron."
#list_sentences = tokenize.sent_tokenize(example_sentence)
#list_sentences2 = tokenize.sent_tokenize(example_sentence2)

#from_text_to_positive_sentences(list_sentences)
#from_text_to_positive_sentences(list_sentences2)
##
input = "Georges est un homme de taille moyenne, de poids moyen, de visage banal, et à vrai dire, il ne présente aucun signe distinctif qui justifierais qu’on l’évoque ici, si ce n’est que d’après le commissaire, il était charmant. Georges est camionneur de profession, mais avant tout de passion, passion qui l’a même poussé à arrêter ses études de mathématiques, lorsqu’il a découvert qu’un mathématicien était rarement amené à conduire des camions. Il aime également beaucoup les chiffres et les choses symétriques, comme nous avons pu le constater précédemment. Cette passion l’a même poussé par le passé à acheter des choses dont il n’avait absolument pas besoin, juste pour satisfaire la symétrie de son appartement. Georges vit donc dans un appartement, modeste loft positionné au plein centre de Toulouse, hérité de ses parents, décédés d’un accident de chasse il y a de cela des années. Pour ce qui est de l’héritage, Georges n’aura pas eu à se battre, étant fils unique, et voilà donc pourquoi il habite là, malgré un salaire de camionneur qui ne lui permettrais pas d’acheter pareil endroit. Georges est un homme de goût, et en tant qu’homme de goût, il aime manger son pâté de campagne sur un pain de mie Harrys (celui aux céréales). C’est en revenant de ses courses que l’accident est arrivé. L’accident, en lui-même, n’avait que peu d’importance et n’allait pas impacter la vie de Georges outre mesure, si ce n’est pour le doux souvenir d’avoir mangé un excellent aligot."
#df_words = decompose()[0]
#EXAMPLE
allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]
#filtered_df_words = filter_df_tags(df_words, allowed_tags)
#print(filtered_df_words)
#NER_neutral = decompose()[1]
#EXAMPLE
#print("ok")
#allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]
#filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
#print(filtered_ner_neutral)

#generate_passwords(filtered_ner_neutral)
##
# importing required modules 
from PyPDF2 import PdfReader 
 
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
  return render_template('front.html')

@app.route('/upload', methods=['POST'])
def upload():
    nom = request.form['nom']
    prenom = request.form['prenom']
    date_of_birth = request.form['dateOfBirth']
    age = request.form['age']
    
    UPLOAD_FOLDER = 'Test_Files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



    
     # Check if the 'instagramLink' field exists in the request
    if 'instagramLink' in request.files:
        instagram_link_file = request.files['instagramLink']
        # Save and process the Instagram link file as needed
        UPLOAD_FOLDER = 'Test_Files'
        instagram_link_file.save(os.path.join(UPLOAD_FOLDER, instagram_link_file.filename))
        print("Instagram Link File:", instagram_link_file.filename)
    else:
        print("No Instagram link file provided")
    print("------------")
    # Check if the 'facebookLink' field exists in the request
    if 'facebookLink' in request.files:
        facebook_link_file = request.files['facebookLink']
           
        # Save and process the Facebook link file as needed
        facebook_link_file.save(os.path.join(UPLOAD_FOLDER, facebook_link_file.filename))
        print("Facebook Link File:", facebook_link_file.filename)
    else:
        print("No Facebook link file provided")
    
     
    # creating a pdf reader object 
    reader = PdfReader('cv.pdf') 
    
    # printing number of pages in pdf file 
    print(len(reader.pages)) 
    
    # getting a specific page from the pdf file 
    page = reader.pages[0] 
    
    # extracting text from page 
    text = page.extract_text() 
    print(text) 
    # Redirect or render a response as needed
    
    
    with open("decoded_html.txt", "w",) as f:
        f.write(text)
        
    return redirect('/my-link/')



@app.route('/my-link/')
def my_link():
   
    
    input = "Georges est un homme de taille moyenne, de poids moyen, de visage banal, et à vrai dire, il ne présente aucun signe distinctif qui justifierais qu’on l’évoque ici, si ce n’est que d’après le commissaire, il était charmant. Georges est camionneur de profession, mais avant tout de passion, passion qui l’a même poussé à arrêter ses études de mathématiques, lorsqu’il a découvert qu’un mathématicien était rarement amené à conduire des camions. Il aime également beaucoup les chiffres et les choses symétriques, comme nous avons pu le constater précédemment. Cette passion l’a même poussé par le passé à acheter des choses dont il n’avait absolument pas besoin, juste pour satisfaire la symétrie de son appartement. Georges vit donc dans un appartement, modeste loft positionné au plein centre de Toulouse, hérité de ses parents, décédés d’un accident de chasse il y a de cela des années. Pour ce qui est de l’héritage, Georges n’aura pas eu à se battre, étant fils unique, et voilà donc pourquoi il habite là, malgré un salaire de camionneur qui ne lui permettrais pas d’acheter pareil endroit. Georges est un homme de goût, et en tant qu’homme de goût, il aime manger son pâté de campagne sur un pain de mie Harrys (celui aux céréales). C’est en revenant de ses courses que l’accident est arrivé. L’accident, en lui-même, n’avait que peu d’importance et n’allait pas impacter la vie de Georges outre mesure, si ce n’est pour le doux souvenir d’avoir mangé un excellent aligot."

    allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]

    NER_neutral = decompose()[1]

    allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]
    filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
    
    df_words = decompose()[0]
    filtered_df_words = filter_df_tags(df_words, allowed_tags)

    result = generate_passwords(filtered_ner_neutral,filtered_df_words)

    return result

if __name__ == '__main__':
  app.run(debug=True)