from PyPDF2 import PdfReader
import os


def process_pdf(file_path):
    # Creating a pdf reader object
    reader = PdfReader(file_path)

    # Printing the number of pages in the pdf file
    print(len(reader.pages))

    # Getting a specific page from the pdf file
    page = reader.pages[0]

    # Extracting text from the page
    text = page.extract_text()
    print(text)

    # Save the extracted text to a file
    with open("decoded_html.txt", "w") as f:
        f.write(text)

    return text

def process_upload_files(request):    
    UPLOAD_FOLDER = 'Test_Files'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    uploaded_files = []

    # Check if the 'instagramLink' field exists in the request
    if 'instagramLink' in request.files:
        instagram_link_file = request.files['instagramLink']
        instagram_link_file.save(os.path.join(UPLOAD_FOLDER, instagram_link_file.filename))
        print("Instagram Link File:", instagram_link_file.filename)
        uploaded_files.append(instagram_link_file.filename)

    # Check if the 'facebookLink' field exists in the request
    if 'facebookLink' in request.files:
        facebook_link_file = request.files['facebookLink']
        facebook_link_file.save(os.path.join(UPLOAD_FOLDER, facebook_link_file.filename))
        print("Facebook Link File:", facebook_link_file.filename)
        uploaded_files.append(facebook_link_file.filename)

    return uploaded_files
