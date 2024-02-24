import pandas as pd
from modules.preprocessing import cleaning_sentence, racine, gramm, extract_racines, filter_words
from modules.ner import retrieve_ner
from modules.lexicon import get_sentiment, categorize_sentiment, detect_emotion, from_text_to_positive_sentences
from modules.assemble_and_filter import filter_df_tags, filter_ner_neutral_tags, occurrences_ner, decompose

#No impact on load time
from modules.password_generator import generate_passwords, generate_personal_passwords
from modules.effort_estimator import estimate_effort
from modules.pdf_reader import process_pdf, process_upload_files
import os
from PyPDF2 import PdfReader 
from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#GLOBAL VARIABLES
SURNAME=''
NAME=''
BIRTHDAY=''
ENTRIES=[]
ESTIMATIONS=[]

COMBINATIONS_COLS = ['string digit', 
                     'string', 'digit', 
                     'digit string', 
                     'string digit string', 
                     'digit string digit', 
                     'string special string', 
                     'string special digit', 
                     'string special', 
                     'string digit special']

@app.route('/')
def index():
    return render_template('web-tool.html')
 

def upload_infos():
    
    print("======================== START upload_infos ========================")
    
    global SURNAME
    global NAME
    global BIRTHDAY
    SURNAME = request.form['nom']
    NAME = request.form['prenom']
    BIRTHDAY = request.form['dateOfBirth']
    print("Profile : ", NAME.lower() ," ", SURNAME.lower(), " ", BIRTHDAY )
    
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
        # Check if the POST request has the file part
    if 'PDF_file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['PDF_file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Check if the file extension is allowed
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        # Save the file to the upload folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        #flash('File uploaded successfully')
        # Redirect to the page that displays the estimation results
        reader = PdfReader('uploads/'+file.filename ) 
       
        # printing number of pages in pdf file 
        print(len(reader.pages)) 
        
        # getting a specific page from the pdf file 
        page = reader.pages[0] 
        
        # extracting text from page 
        text = page.extract_text() 
        print(text) 
        # Redirect or render a response as needed
        with open("pdf_file.txt", "w",) as f:
            f.write(text)
    print("======================== END upload_infos ========================")
        
 
@app.route('/upload', methods=['POST'])
def upload():
    
    upload_infos()
    action = request.form['action']
    action == 'generator'
    return redirect('/generator/')
   
 

@app.route('/generator/')
def generator():
    
    print("======================== START GENERATOR ========================")

    # OUTPUT FILE
    with open('output.txt', 'w') as f:
    
        # Read the entire content of the file
        print("READING PDF",file=f)
        with open('pdf_file.txt', 'r') as file:
            file_content = file.read()
        input_text = file_content
        
        # Define allowed NER tags
        allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]

        # Perform NER and data decomposition
        print("DECOMPOSING",file=f)
        df_words, NER_neutral = decompose(input_text)
    
        pd.set_option('display.max_rows', 200)  
        pd.set_option('display.max_columns', 20) 
        
        print("DF WORDS    : ", df_words,file=f)
        print("NER Neutral : ", NER_neutral,file=f)

        # Filter NER neutral and df_words to allowed tags
        print("FILTERS",file=f)
        filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
        filtered_df_words = filter_df_tags(df_words, allowed_tags)

        print("Filtered DF WORDS    : ", filtered_df_words,file=f)
        print("Filtered NER Neutral : ", filtered_ner_neutral,file=f)

        # Generate passwords based on filtered NER and df_words
    #    result = generate_passwords(filtered_ner_neutral, filtered_df_words)

        # Generate PERSONAL passwords based on filtered NER and df_words
        print("GENERATION",file=f)
        global ENTRIES
        global ESTIMATIONS
        ENTRIES, ESTIMATIONS = generate_personal_passwords(filtered_ner_neutral, filtered_df_words,SURNAME,NAME,BIRTHDAY)
        
        print("Entries     : ", ENTRIES,file=f)
        print("Estimations : ", ESTIMATIONS,file=f)
        
    print("======================== END GENERATOR ========================")
    return render_template('choices.html')

@app.route('/choices', methods=['POST'])
def choices():
    action = request.form['action']
 
    if action == 'estimations':
        return render_template('estimation_results.html', estimation=ESTIMATIONS)
    elif action == 'entries':
        return render_template('passwords_list.html', words=ENTRIES)
    elif action == 'back':
        return redirect('/')

@app.route('/estimations/', methods=['POST'])
def estimations():
    action = request.form['action']
    # Render the template with the estimations data
    if action == 'back':
        return render_template('choices.html')
    elif action == 'home':
        return redirect('/')
   
    
  

@app.route('/entries/', methods=['POST'])
def entries():
    action = request.form['action']
 
    # Render the template with the entries data
    if action == 'back':
        return render_template('choices.html')
    elif action == 'home':
        return redirect('/')
    


if __name__ == '__main__':
    app.run(debug=True)
