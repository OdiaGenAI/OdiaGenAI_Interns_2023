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
# import json
import docx2txt
# import textract
from PyPDF2 import PdfFileReader
import pdfplumber
import os
# from streamlit.runtime.state import SessionState

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
def run_function(url, documents):
    data = ""
    # Check if the user has provided a URL
    if url:
        try:
            # Make a GET request to the URL and extract the text content
            response = requests.get(url)
            if response.status_code == 200:
                text_content = response.text
                # st.write(text_content)

                soup = BeautifulSoup(text_content, 'html.parser')

                # Extracting the header
                h1_tags = soup.find_all("h1")
                headline = [h1.get_text(strip=True) for h1 in h1_tags]
                headline = '\n'.join(headline)

                # Extracting the p p_tags
                p_tags = soup.find_all("p")

                # Extract the text content from each <p> tag
                paragraphs = [p.get_text(strip=True) for p in p_tags]
                paragraphs = '\n'.join(paragraphs)

                data = data + (headline + '\n\n' + paragraphs)

                # Display the extracted text content from url
                st.text_area("Extracted Text", value=data, height=200)
                return True, data

        except requests.exceptions.RequestException as e:
            st.error("Error: An exception occurred while fetching content from the URL.")
            return False, data

    # Check if the user has provided a document
    elif documents is not None:
        for document in documents:
            document_details = {
                "filename": document.name,
                "filetype": document.type,
                "filesize": document.size
            }
            st.write(document_details)

            # Extract content from the txt file
            if document.type == "text/plain":
                # Read as bytes
                data += str(document.read(), "utf-8")

            # Extract content from the pdf file
            elif document.type == "application/pdf":
                # using PyPDF2
                # data += read_pdf(document)

                # using pdfplumber
                try:
                    with pdfplumber.open(document) as pdf:
                        all_text = ""
                        for page in pdf.pages:
                            text = page.extract_text()
                            all_text += text + "\n"
                        data += all_text
                except requests.exceptions.RequestException as e:
                    st.write("None")

            # Extract content from the docx file
            elif document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                data += docx2txt.process(document)

        # Display the extracted text content from file
        st.write("attached")
        st.text_area("Extracted Text", value=data, height=200)
        return True, data

    else:
        st.error("Error: An error occurred while fetching content.")
        return False, data


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

    # dividing the body section into 3 columns for url, attach button and enter button
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    # url
    with col1:
        url = st.text_input(label='', placeholder="Enter URL")
    # attached button
    with col2:
        documents = st.file_uploader("", type=["pdf", "txt", "docx"], accept_multiple_files=True)
        if not documents:
            documents = None
        else:
            for doc in documents:
                if doc.name.split(".")[-1].lower() not in ["pdf", "txt", "docx"]:
                    st.error("Unsupported file: " + doc.name)
    # enter button
    with col3:
        # Initialize state of button Enter
        if "button_enter" not in st.session_state:
            st.session_state.button_enter = False

        if st.button("Enter"):
            st.session_state.button_enter = True

    extracted = False

    if st.session_state.button_enter:
        extracted, data = run_function(url, documents)

        if extracted:
            col1, col2 = st.columns([0.5, 0.5])

            with col1:
                saved_button = False
                if st.button("Save",key="b_save"):
                    file_name = "output.txt"

                    # Define the folder path
                    folder_path = "extracted data"

                    # Create the folder if it doesn't exist
                    os.makedirs(folder_path, exist_ok=True)

                    # Define the file path
                    file_path = os.path.join(folder_path, file_name)
                    # Save string variable to file
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(data)
                    saved_button = True

            with col2:
                if st.button("Double click to Clear"):
                    st.session_state.button_enter = False

            if saved_button:
                # Confirmation message
                st.success(f"File saved as {file_name} in the current directory.")

