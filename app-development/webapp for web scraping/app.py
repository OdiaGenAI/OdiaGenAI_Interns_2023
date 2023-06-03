# installed pip packages
# pip install streamlit
# pip install beautifulsoup4
# pip install docx2txt
# pip install pypdf2
# pip install pdfplumber

import streamlit as st

# File Processing pkgs
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
import docx2txt
# import textract
from PyPDF2 import PdfFileReader
import pdfplumber


# ---- LOAD ASSETS ----
img_page_icon = Image.open("images/web_icon.jpeg")

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="OdiaGenAI ", page_icon=img_page_icon, layout="wide")

# Load CSS file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS file
load_css('styles.css')



# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, username :wave:")
    st.write("##")
    st.markdown("<h5 class='text'>OdiaGenAI is a collaborative initiative that conducts research on </h5>",
                unsafe_allow_html=True)
    st.markdown("<h5>Generative AI and LLM for the Odia Language.</h5>", unsafe_allow_html=True)
    # st.title("Odia Generative AI")

    st.markdown("<h1 class='title'>Odia Generative AI</h1>", unsafe_allow_html=True)



# ---- BODY SECTION ----
with st.container():
    st.subheader("Collecting monolingual data (Odia or any Indic Languages)")

    # ----- FUNCTIONS ----
    # function to get the text from pdf using PyPDF2
    def read_pdf(file):
        pdfReader = PdfFileReader(file)
        count = pdfReader.numPages
        # all_page_text = ""
        # for i in range(count):
        #     page = pdfReader.getPage(i)
        #     all_page_text += page.extractText()
        #
        # return all_page_text
        return count

    # function to run the enter button
    def run_function(url , documents):
        news = ""
        # Check if the user has provided a URL
        if url:
            try:
                # Make a GET request to the URL and extract the text content
                response = requests.get(url)
                if response.status_code == 200:
                    text_content = response.text

                    soup = BeautifulSoup(text_content, 'html.parser')

                    # Extracting the header
                    # Extracting the script tag which includes the heading
                    heading = soup.find('script', type='application/ld+json')

                    # Extract the JSON data from the script tag
                    json_data_heading = heading.string

                    # Load the JSON data into a Python dictionary
                    data = json.loads(json_data_heading)
                    headline = data['headline']

                    body = soup.find('div', class_='oi-article-lt')
                    # Find all <p> tags within the div_tag
                    p_tags = body.find_all('p')

                    # Extract the text content from each <p> tag
                    paragraphs = [p.get_text(strip=True) for p in p_tags]
                    paragraphs = '\n'.join(paragraphs)

                    news = news + (headline + '\n\n' + paragraphs)

                    # Display the extracted text content from url
                    st.text_area("Extracted Text", value=news, height=200)

                else:
                    st.error("Error: Unable to fetch content from the provided URL.")
            except requests.exceptions.RequestException as e:
                st.error("Error: An exception occurred while fetching content from the URL.")

        # Check if the user has provided a document
        elif documents is not None:
            for document in documents:
                document_details = {
                    "filename":document.name,
                    "filetype":document.type,
                    "filesize":document.size
                }
                st.write(document_details)

                # Extract content from the txt file
                if document.type == "text/plain":
                    # Read as bytes
                    news += str(document.read(), "utf-8")

                # Extract content from the pdf file
                elif document.type == "application/pdf":
                    # using PyPDF2
                    # news += read_pdf(document)

                    # using pdfplumber
                    try:
                        with pdfplumber.open(document) as pdf:
                            all_text = ""
                            for page in pdf.pages:
                                text = page.extract_text()
                                all_text += text + "\n"
                            news += all_text
                    except:
                        st.write("None")

                # Extract content from the docx file
                else:
                    news += docx2txt.process(document)

            # Display the extracted text content from file
            st.text_area("Extracted Text", value=news, height=200)
        else:
            st.error("Error: An error occurred while fetching content .")



    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col1:
        url = st.text_input(label='', placeholder="Enter URL")

    with col2:
        documents = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf", "txt", "docx"], accept_multiple_files=True)

    with col3:
        b = st.button("Enter")

    if b:
        run_function(url, documents)
