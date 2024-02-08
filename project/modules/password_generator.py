import itertools


# Function to generate passwords based on named entities and words
def generate_passwords(filtered_ner_neutral, filtered_df_words):
    # Create dictionaries for different types of strings
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

    return valid_passwords


# Function to generate passwords based on named entities and words
def generate_personal_passwords(filtered_ner_neutral, filtered_df_words,surname,name,birthday):
    #Create dictionaries
    personal_string_dict = {
        'Name': list(set(filtered_ner_neutral.get('PERSON', [])).union(filtered_df_words.get('PERSON', []))),
        'City': list(set(filtered_ner_neutral.get('GPE', [])).union(filtered_df_words.get('GPE', [])))
        + list(set(filtered_ner_neutral.get('LOC', [])).union(filtered_df_words.get('LOC', []))),
    }

    personal_digit_dict = {
        'Number': list(set(filtered_ner_neutral.get('CARDINAL', [])).union(filtered_df_words.get('CARDINAL', [])))
        + [str(i) for i in range(10)],
        'Year': [date[-4:] for date in list(set(filtered_ner_neutral.get('DATE', [])).union(filtered_df_words.get('DATE', []))) if date[-4:].isdigit()],
    }

    personal_special_dict = {
        'Simple': ['.', '_', '!', '@', '-', ':', '#', '*', '$', ' ', '&', '+', '?', ',', '/'],
        'Combined': ['!!', '.:', '&#', '**', '…', ':', '$$', '__'],
    }

    # Create lists for each dictionary
    personal_string_list = list(itertools.chain.from_iterable(personal_string_dict.values()))
    personal_digit_list = list(itertools.chain.from_iterable(personal_digit_dict.values()))
    personal_special_list = list(itertools.chain.from_iterable(personal_special_dict.values()))

    # Adding profile
    personal_string_list=[name,surname] + personal_string_list
    personal_digit_list =[birthday[:4]] + personal_digit_list 

    all_combinations = []

    # Generate combinations of string + special + digits
    combo1 = itertools.product(personal_string_list, personal_special_list, personal_digit_list)
    all_combinations.extend(''.join(comb) for comb in combo1)

    # Generate combinations of string + digits + special
    combo2 = itertools.product(personal_string_list, personal_digit_list, personal_special_list)
    all_combinations.extend(''.join(comb) for comb in combo2)

    # Filter combinations with length >= 8
    valid_passwords = [password for password in all_combinations if len(password) >= 8]

    return valid_passwords