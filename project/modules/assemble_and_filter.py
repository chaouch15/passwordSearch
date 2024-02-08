import pandas as pd
from .preprocessing import  filter_words, extract_racines
from .ner import retrieve_ner
from .lexicon import from_text_to_positive_sentences
from nltk import tokenize

def occurrences_ner(list_sentences):
    rows = []
    NER_glob = pd.DataFrame(columns=['CARDINAL','DATE','EVENT','FAC','GPE','LANGUAGE','LAW','LOC','MONEY','NORP','ORDINAL','ORG','PERCENT','PERSON','PRODUCT','QUANTITY','TIME','WORK_OF_ART'])
    for sentence in list_sentences:
        NER = retrieve_ner(sentence)
        for key, word_list in NER.items():
            for word in word_list:
                new_row = pd.Series(index=NER_glob.columns)
                new_row[key] = word
                rows.append(new_row)
    NER_glob = pd.DataFrame(rows, columns=NER_glob.columns)
    return NER_glob

def decompose(input_text):
    #First decompose in sentences
    list_sentences = tokenize.sent_tokenize(input_text)

    #Second NER directly
    NER_neutral = occurrences_ner(list_sentences)

    #Third Positive processing, only keep positive sentences
    list_positive_sentences = from_text_to_positive_sentences(list_sentences)

    #Fourth NLP process to get nouns, adj
    list_words_NLP =[]
    for sentence in list_positive_sentences:
        list_words_NLP.append(filter_words(extract_racines(sentence)))

    #Five second NER on the positive sentences
    NER_positive = occurrences_ner(list_positive_sentences)

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

    return (df_words, NER_neutral)

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
 
