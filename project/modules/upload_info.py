
from flask import Flask, render_template, request, redirect, session
from flask import Flask, render_template, request, redirect
from flask import flash, redirect

from werkzeug.utils import secure_filename
import os

from PyPDF2 import PdfReader 

def upload_infos():
    global SURNAME
    global NAME
    global BIRTHDAY
    SURNAME = request.form['nom']
    NAME = request.form['prenom']
    BIRTHDAY = request.form['dateOfBirth']
   
    
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
        