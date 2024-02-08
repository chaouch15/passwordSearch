from modules.preprocessing import cleaning_sentence, racine, gramm, extract_racines, filter_words
from modules.ner import retrieve_ner
from modules.lexicon import get_sentiment, categorize_sentiment, detect_emotion, from_text_to_positive_sentences
from modules.assemble_and_filter import filter_df_tags, filter_ner_neutral_tags, occurrences_ner, decompose

#No impact on load time
from modules.password_generator import generate_passwords, generate_personal_passwords
from modules.effort_estimator import estimate_effort
from modules.pdf_reader import process_pdf, process_upload_files
from flask import Flask, render_template, request, redirect
import os

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
    
    global SURNAME
    global NAME
    global BIRTHDAY
    SURNAME = request.form['nom']
    NAME = request.form['prenom']
    BIRTHDAY = request.form['dateOfBirth']
    age = request.form['age']
    
    UPLOAD_FOLDER = 'Test_Files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # Process uploaded files
#    uploaded_files = process_upload_files(request)

    # Process PDF file if provided
#    if 'pdf' in request.files:
#        pdf_file = request.files['pdf']
#        pdf_file.save(os.path.join(UPLOAD_FOLDER, pdf_file.filename))
#        print("PDF File:", pdf_file.filename)
#        pdf_text = process_pdf(os.path.join(UPLOAD_FOLDER, pdf_file.filename))
    
    return redirect('/my-link/')

@app.route('/my-link/')
def my_link():
        
    # Example input
    input_text = "Georges est un homme de taille moyenne, de poids moyen, de visage banal, et à vrai dire, il ne présente aucun signe distinctif qui justifierais qu’on l’évoque ici, si ce n’est que d’après le commissaire, il était charmant. Georges est camionneur de profession, mais avant tout de passion, passion qui l’a même poussé à arrêter ses études de mathématiques, lorsqu’il a découvert qu’un mathématicien était rarement amené à conduire des camions. Il aime également beaucoup les chiffres et les choses symétriques, comme nous avons pu le constater précédemment. Cette passion l’a même poussé par le passé à acheter des choses dont il n’avait absolument pas besoin, juste pour satisfaire la symétrie de son appartement. Georges vit donc dans un appartement, modeste loft positionné au plein centre de Toulouse, hérité de ses parents, décédés d’un accident de chasse il y a de cela des années. Pour ce qui est de l’héritage, Georges n’aura pas eu à se battre, étant fils unique, et voilà donc pourquoi il habite là, malgré un salaire de camionneur qui ne lui permettrais pas d’acheter pareil endroit. Georges est un homme de goût, et en tant qu’homme de goût, il aime manger son pâté de campagne sur un pain de mie Harrys (celui aux céréales). C’est en revenant de ses courses que l’accident est arrivé. L’accident, en lui-même, n’avait que peu d’importance et n’allait pas impacter la vie de Georges outre mesure, si ce n’est pour le doux souvenir d’avoir mangé un excellent aligot."

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
    
#    return str(result)
    return estimation
    

if __name__ == '__main__':
    app.run(debug=True)
