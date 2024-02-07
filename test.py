from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

import chardet

import html2text

# importing required modules 
from PyPDF2 import PdfReader 
  
# creating a pdf reader object 
reader = PdfReader('cv.pdf') 
  
# printing number of pages in pdf file 
print(len(reader.pages)) 
  
# getting a specific page from the pdf file 
page = reader.pages[0] 
  
# extracting text from page 
text = page.extract_text() 
print(text) 

# Open the HTML file in binary mode and read its contents
with open("Test_files/SarraKouki.html", 'rb') as f:
    # Detect the encoding of the file
    encoding = chardet.detect(f.read())['encoding']
print('--')
# Reopen the file with the detected encoding and read its contents
with open("Test_files/SarraKouki.html", 'r', encoding=encoding) as f:
    html = f.read()

# Now you can proceed with parsing the HTML using BeautifulSoup or any other library

print(html2text.html2text(html))
      
text =  ' '.join(BeautifulSoup(html, "html.parser").stripped_strings)

print(text)
soup = BeautifulSoup(html)

for script in soup(["script", "style"]):
    script.decompose()



strips = list(soup.stripped_strings)
print(strips[:5])



# Open the HTML file in binary mode and read its contents
with open("Test_files/Sarra.html", 'rb') as f:
    # Detect the encoding of the file
    encoding = chardet.detect(f.read())['encoding']
print('--')
# Reopen the file with the detected encoding and read its contents
with open("Test_files/Sarra.html", 'r', encoding=encoding) as f:
    html = f.read()

# Now you can proceed with parsing the HTML using BeautifulSoup or any other library



soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

# Decode the HTML content using the detected encoding
html_decoded = html.encode(encoding).decode('utf-8', 'ignore')

with open("decoded_html.txt", "w", encoding="utf-8") as f:
    f.write(html_decoded)
# Now you can print the decoded HTML content
print(html_decoded)
print('hey')
print(text)
print('--')