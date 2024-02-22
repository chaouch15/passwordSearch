from modules.preprocessing import cleaning_sentence, racine, gramm, extract_racines, filter_words
from modules.ner import retrieve_ner
from modules.lexicon import get_sentiment, categorize_sentiment, detect_emotion, from_text_to_positive_sentences
from modules.assemble_and_filter import filter_df_tags, filter_ner_neutral_tags, occurrences_ner, decompose
from modules.upload_info import upload_infos
#No impact on load time
from modules.password_generator import generate_passwords, generate_personal_passwords
from modules.effort_estimator import estimate_effort
from modules.pdf_reader import process_pdf, process_upload_files
from flask import Flask, render_template, request, redirect, session
import os
from PyPDF2 import PdfReader 
 
from flask import Flask, render_template, request, redirect
from flask import flash, redirect
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#GLOBAL VARIABLES
SURNAME=''
NAME=''
BIRTHDAY=''

@app.route('/')
def index():
    return render_template('web-tool.html')

@app.route('/upload', methods=['POST'])
def upload():
    

    upload_infos()
    action = request.form['action']
    if action == 'my-link':
        return redirect('/my-link/')
    elif action == 'my-link-bis':
        return redirect('/my-link-bis/')
 

  
    

   

@app.route('/my-link/')
def my_link():
 
    with open('pdf_file.txt', 'r') as file:
    # Read the entire content of the file
        file_content = file.read()
    # Example input
    input_text = file_content
    # Define allowed NER tags
    allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]

    # Perform NER and data decomposition
    df_words, NER_neutral = decompose(input_text)

    # Filter NER neutral and df_words to allowed tags
    filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
    filtered_df_words = filter_df_tags(df_words, allowed_tags)

    # Generate passwords based on filtered NER and df_words
    #result = generate_passwords(filtered_ner_neutral, filtered_df_words)
    result, estimation = generate_personal_passwords(filtered_ner_neutral, filtered_df_words,SURNAME,NAME,BIRTHDAY)
    #estimation_data = [(category, values) for category, values in estimation.items()]

    # Render the template with the estimation data
    return render_template('estimation_results.html', estimation=estimation)

    #return render_template('web-tool-with-table.html', estimation=estimation)
#    return str(result)
   # return estimation
    
  

@app.route('/my-link-bis/')
def my_link_bis():
 
    with open('pdf_file.txt', 'r') as file:
    # Read the entire content of the file
        file_content = file.read()
    # Example input
    input_text = file_content
    # Define allowed NER tags
    allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]

    # Perform NER and data decomposition
    df_words, NER_neutral = decompose(input_text)

    # Filter NER neutral and df_words to allowed tags
    filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
    filtered_df_words = filter_df_tags(df_words, allowed_tags)

    # Generate passwords based on filtered NER and df_words
    #result = generate_passwords(filtered_ner_neutral, filtered_df_words)
    result = generate_passwords(filtered_ner_neutral,filtered_df_words)
    #estimation_data = [(category, values) for category, values in estimation.items()]

    # Render the template with the estimation data
    return render_template('passwords_list.html', words=result)
    #return render_template('web-tool-with-table.html', estimation=estimation)
#    return str(result)
   # return estimation
    


if __name__ == '__main__':
    app.run(debug=True)
