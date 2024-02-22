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
    input_text = "Aujourd'hui j'ai acheté du pain. Il faisait beau ! J'adore les croissants, je n'ai pas pu m'empêcher d'en acheter 5! Regardez cette photo de mon chat Patrice, n'est-il pas mignon ? Joyeux anniversaire Catherine ! Bravo à mon petit-fils qui vient d'avoir le bac ! Patrice n'aime pas sa pâté... Une dernière vidéo de chat, ils sont tout mignons. Patrice fête ses un ans aujourd'hui.Une journée bien remplie aujourd'hui ! J'ai fait un saut à la boulangerie pour du pain frais sous ce beau soleil ! Et devinez quoi ? Les croissants étaient irrésistibles, j'en ai pris 5 ! Regardez qui est de retour pour vous faire sourire ! Patrice, mon adorable petit chat, vous envoie des câlins et des ronrons ! \#ChatAdorable. Un joyeux anniversaire à Catherine, une personne merveilleuse qui apporte de la joie à tous ceux qui l'entourent ! C'est avec une immense fierté que je félicite mon petit-fils pour son succès au bac ! Bravo pour tout ton travail acharné \#FierGrandParent. Il semblerait que Patrice soit un fin gourmet... Il boudine sa pâté aujourd'hui ! \#ChatCapricieux. Besoin d'une dose de mignonnerie pour égayer votre journée ? Ne cherchez pas plus loin ! Voici une dernière vidéo adorable de nos amis à quatre pattes ! \#ChatonsMignons. Mon Patrice chéri fête ses un an aujourd'hui ! Comment le temps passe vite ! Joyeux anniversaire à mon petit rayon de soleil ! Aujourd'hui, j'ai exploré un nouveau sentier de randonnée dans les montagnes. La vue était à couper le souffle ! Je viens de terminer un nouveau livre fascinant. Recommanderiez-vous une lecture captivante ? Quelqu'un a des conseils pour améliorer mes compétences en cuisine ? J'ai envie d'essayer de nouvelles recettes ce week-end ! J'ai assisté à un concert incroyable hier soir. La musique live a vraiment le pouvoir de transporter ! Je suis tombé sur un vieux album photo et j'ai été submergé par les souvenirs. Quels sont vos moments préférés à revivre en photos ? J'ai récemment commencé à apprendre une nouvelle langue. C'est un défi stimulant mais tellement enrichissant ! Après des mois de travail acharné, j'ai enfin terminé mon projet artistique. C'est une sensation incroyable de voir son travail aboutir ! J'ai découvert une nouvelle série sur Netflix et je suis déjà accro ! Des recommandations de séries à regarder ? Je suis impressionné par les progrès technologiques récents. Quelles innovations vous ont le plus marqué récemment ? Hier, j'ai visité une exposition d'art moderne. C'était une expérience vraiment inspirante ! Quel est l'art qui vous touche le plus ? Je suis en train de planifier mes prochaines vacances. Des destinations de voyage à recommander ? J'ai eu une discussion fascinante avec un ami sur l'avenir de l'humanité dans l'espace. Quelles sont vos réflexions sur l'exploration spatiale ?"
    
    # Define allowed NER tags
    allowed_tags = ["GPE", "LOC", "PERSON", "CARDINAL", "DATE"]

    # Perform NER and data decomposition
    print("########  DECONPOSITION  ########")
    df_words, NER_neutral = decompose(input_text)
    
    print("DF: ", df_words)
    print("NER_neutral: ", NER_neutral)

    # Filter NER neutral and df_words to allowed tags
    print("########  FILTER NER  ########")
    filtered_ner_neutral = filter_ner_neutral_tags(NER_neutral, allowed_tags)
    print("filtered NER: ",filtered_ner_neutral)
    
    print("########  FILTER DF  ########")
    filtered_df_words = filter_df_tags(df_words, allowed_tags)
    print("filtered DF: ", filtered_df_words)

    # Generate passwords based on filtered NER and df_words
    #result = generate_passwords(filtered_ner_neutral, filtered_df_words)
    print("########  ENTRY GENERATION  ########")
    result, estimation = generate_personal_passwords(filtered_ner_neutral, filtered_df_words,SURNAME,NAME,BIRTHDAY)
    
#    return str(result)
    return estimation


if __name__ == '__main__':
    app.run(debug=True)
