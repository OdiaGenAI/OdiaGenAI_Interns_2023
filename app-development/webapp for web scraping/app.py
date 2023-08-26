# installed pip packages
# pip install streamlit
# pip install beautifulsoup4
# pip install docx2txt
# pip install pypdf2
# pip install pdfplumber
# pip install justext

import os

# import json
import docx2txt
import justext
import pdfplumber
import requests
import streamlit as st

# import xml.dom.minidom
from bs4 import BeautifulSoup
from lxml import etree

# File Processing pkgs
from PIL import Image

# import textract
from PyPDF2 import PdfFileReader

# import streamlit.components.v1 as components


# ---- LOAD ASSETS ----
img_page_icon = Image.open("images/web_icon.jpeg")

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="OdiaGenAI ", page_icon=img_page_icon, layout="wide")


def load_css(file_path):
    """load_css

    Load CSS file
    """
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load CSS file
load_css("styles2.css")


def check_sitemap(url):
    """check_sitemap

    function to check whether the url is a sitemap or not
    """
    # Check the URL's ending
    if url.lower().endswith(("sitemap.xml", "sitemap_index.xml", "sitemap")):
        try:
            # Parse the content as XML
            response = requests.get(url)
            xml_content = etree.fromstring(response.content)
            # Check for sitemap-specific elements
            if xml_content.tag == "urlset" or xml_content.tag == "sitemapindex":
                return True
        except etree.XMLSyntaxError:
            pass

    # Additional conditions for identifying sitemaps
    if "sitemap" in url.lower():
        # Perform additional checks specific to the website's structure or naming conventions
        return True

    return False


def extract_urls_from_sitemaps(xml_url):
    """extract_urls_from_sitemaps

    function to get urls from the site map and extract those data
    """
    # Make a GET request to the URL and extract the xml content
    response = requests.get(xml_url)

    soup = BeautifulSoup(response.text, "xml")
    extracted_urls = []

    # check if the sitemap contains nested sitemaps
    sitemap_tags = soup.find_all("sitemap")
    if sitemap_tags:
        # Process nested sitemaps
        for sitemap_tag in sitemap_tags:
            print("sitemap_tags:" + sitemap_tag)
            nested_url = sitemap_tag.find("loc").text
            print("nested_url:", nested_url)
            nested_urls = extract_urls_from_sitemaps(nested_url)
            extracted_urls.extend(nested_urls)
    else:
        # Extract URLs from the current sitemap
        loc_tags = soup.find_all("loc")
        for loc_tag in loc_tags:
            # if loc_tag.parent.name != 'image':
            url = loc_tag.text
            if url.endswith(".pdf") or url.endswith(".jpg") or url.endswith(".jpeg"):
                print(f"url skipped because it is a {url.split('.')[-1]}")
            else:
                print("url:", url)
                extracted_urls.append(url)

    return extracted_urls


def valid_url(url):
    """valid_url

    function to check whether the entered url is valid
    """
    try:
        # Make a GET request to the URL and extract the text content
        response = requests.get(url)
        if response.status_code == 200:
            return True

    except requests.exceptions.RequestException as e:
        print(e)
        return False


def custom_stoplist():
    """custom_stoplist

    function to create a custom stoplist for justext
    """
    odia_stopwords = [
        "ଏହି",
        "ଏକ",
        "ଏକାଉଣଟ",
        "ମୁଁ",
        "ମୋର",
        "ମୁଁ ନିଜେ",
        "ଆମେ",
        "ଆମର",
        "ଆମର",
        "ଆମେ ନିଜେ",
        "ତୁମେ",
        "ତୁମର",
        "ତୁମର",
        "ନିଜେ",
        "ନିଜେ",
        "ସେ",
        "ତାଙ୍କୁ",
        "ତାଙ୍କର",
        "ନିଜେ",
        "ସେ",
        "ତାଙ୍କୁ",
        "ତାଙ୍କର",
        "ନିଜେ",
        "ଏହା",
        "ଏହାର",
        "ନିଜେ |",
        "ସେମାନେ",
        "ସେଗୁଡିକ",
        "ସେମାନଙ୍କର",
        "ସେମାନଙ୍କର",
        "ନିଜେ |",
        "କଣ",
        "ଯାହା",
        "କିଏ",
        "କାହାକୁ",
        "ଏହା",
        "ତାହା",
        "ଏଗୁଡ଼ିକ",
        "ସେଗୁଡ଼ିକ",
        "ମୁଁ",
        "ହେଉଛି",
        "ହେଉଛି |",
        "ଥିଲା",
        "ଥିଲା |",
        "ହୁଅ",
        "ହୋଇସାରିଛି |",
        "ହେବା",
        "ଅଛି",
        "ଅଛି",
        "ଥିଲା",
        "ଅଛି",
        "କର",
        "କରେ |",
        "କରିଛନ୍ତି",
        "କରିବା",
        "ଏବଂ",
        "କିନ୍ତୁ",
        "ଯଦି",
        "କିମ୍ବା",
        "କାରଣ",
        "ଯେପରି",
        "ପର୍ଯ୍ୟନ୍ତ",
        "ଯେତେବେଳେ",
        "ର",
        "ପାଇଁ",
        "ସହିତ",
        "ବିଷୟରେ",
        "ବିପକ୍ଷରେ",
        "ମଧ୍ୟରେ",
        "ଭିତରକୁ",
        "ମାଧ୍ୟମରେ",
        "ସମୟରେ",
        "ପୂର୍ବରୁ",
        "ପରେ",
        "ଉପରେ",
        "ନିମ୍ନରେ |",
        "କୁ",
        "ଠାରୁ",
        "ଅପ୍",
        "ତଳକୁ",
        "ଭିତରେ",
        "ବାହାରେ",
        "ଉପରେ",
        "ବନ୍ଦ",
        "ସମାପ୍ତ",
        "ତଳେ |",
        "ପୁନର୍ବାର",
        "ଆଗକୁ",
        "ତାପରେ",
        "ଥରେ |",
        "ଏଠାରେ",
        "ସେଠାରେ",
        "କେବେ",
        "କେଉଁଠାରେ",
        "କିପରି",
        "ସମସ୍ତ",
        "ଉଭୟ",
        "ପ୍ରତ୍ୟେକ",
        "ଅଳ୍ପ",
        "ଅଧିକ",
        "ଅଧିକାଂଶ",
        "ଅନ୍ୟ",
        "କେତେକ",
        "ଏହିପରି",
        "ନୁହେଁ |",
        "କେବଳ",
        "ନିଜର",
        "ସମାନ",
        "ତେଣୁ",
        "ଅପେକ୍ଷା",
        "ମଧ୍ୟ",
        "ବହୁତ",
        "କରିପାରିବେ |",
        "ଇଚ୍ଛା",
        "କେବଳ",
        "କରିବା ଉଚିତ",
        "ବର୍ତ୍ତମାନ",
    ]
    return frozenset(odia_stopwords)


def extract_data_from_url_(url):
    """extract_data_from_url_

    function to extract data from url using justext
    """
    response = requests.get(url)
    response.raise_for_status()
    page = response.content

    data_url = ""
    para = ""
    paragraphs = justext.justext(
        page, custom_stoplist(), 70, 140, 0.0, 0.02, 0.5, 150, False
    )
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            para = para + "\n" + paragraph.text

    data_url = "\n\nFrom url:" + url + "\n" + para + "\n"

    return data_url


sitemap_data = ""


def read_pdf(file):
    """read_pdf

    function to get the text from pdf using PyPDF2
    """
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    # all_page_text = ""
    # for i in range(count):
    #     page = pdfReader.getPage(i)
    #     all_page_text += page.extractText()
    #
    # return all_page_text
    return count


def run_function(url, documents):
    """run_function

    function to run the enter button
    """
    data = ""
    # Check if the user has provided a URL
    if url:
        if valid_url(url):
            data = extract_data_from_url_(url)
            st.text_area("Extracted Text", value=data, height=200)
            # return extract status, and the data extracted
            return True, data
        else:
            return False, data

    # Check if the user has provided a document
    elif documents is not None:
        for document in documents:
            document_details = {
                "filename": document.name,
                "filetype": document.type,
                "filesize": document.size,
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
                    print(e)
                    st.write("None")

            # Extract content from the docx file
            elif (
                document.type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                data += docx2txt.process(document)

        # Display the extracted text content from file
        st.write("attached")
        st.text_area("Extracted Text", value=data, height=200)
        # return extract status, and the data extracted
        return True, data

    else:
        st.error("Error: An error occurred while fetching content.")
        # return extract status, and the data extracted
        return False, data


def main():
    """main"""
    # ---- HEADER SECTION ----
    with st.container():
        st.subheader("Hi!! :wave:")
        st.write("##")
        st.markdown(
            "<h5 class='text'>OdiaGenAI is a collaborative initiative that conducts research on </h5>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h5>Generative AI and LLM for the Odia Language.</h5>",
            unsafe_allow_html=True,
        )
        # st.title("Odia Generative AI")

        st.markdown("<h1 class='title'>Odia Generative AI</h1>", unsafe_allow_html=True)

    # ---- BODY SECTION ----
    with st.container():
        st.subheader("Collecting monolingual data (Odia or any Indic Languages)")

        # dividing the body section into 3 columns for url, attach button and enter button
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        # url/xml
        with col1:
            url_or_xml = st.text_input(label="", placeholder="Enter URL")
            is_a_sitemap = check_sitemap(url_or_xml)

        # attached files
        with col2:
            documents = st.file_uploader(
                "", type=["pdf", "txt", "docx"], accept_multiple_files=True
            )
            if not documents:
                documents = None
            else:
                for doc in documents:
                    if doc.name.split(".")[-1].lower() not in ["pdf", "txt", "docx"]:
                        # if documents is not the relevant type
                        st.error("Unsupported file: " + doc.name)

        # Initialize state of button Enter
        with col3:
            st.write("##")
            if "button_enter" not in st.session_state:
                st.session_state.button_enter = False

            if st.button("Enter"):
                st.session_state.button_enter = True
                # st.write("session state true")

        if "extracted" not in st.session_state:
            st.session_state.extracted = False
        data = ""

        # the enter button
        if st.session_state.button_enter:
            # check if it is a sitemap or not
            if is_a_sitemap:
                if "Initial" not in st.session_state:
                    st.session_state.Initial = True
                # check whether its the initial state
                if st.session_state.Initial is True:
                    # print("\n\n\n\n1)Initial State", st.session_state.Initial, "\n\n\n\n\n")
                    xml = url_or_xml
                    st.write("It is a sitemap")
                    stored_sitemap_urls = extract_urls_from_sitemaps(xml)
                    print("\nno. of urls: ", len(stored_sitemap_urls))

                    if stored_sitemap_urls:
                        print(stored_sitemap_urls)
                        for sitemap_url in stored_sitemap_urls:
                            if valid_url(sitemap_url):
                                print(sitemap_url)
                                # using justext to extract data
                                data = data + extract_data_from_url_(sitemap_url)
                            else:
                                st.error("Couldnt extract data from " + sitemap_url)

                        if "sitemap_data" not in st.session_state:
                            st.session_state.sitemap_data = data
                        # print("\n\n\nst.session.data ", st.session_state.sitemap_data)
                        # print("\n\n\n\nRUNNING \n\n\n\n")
                        st.session_state.Initial = False
                        print(
                            "\n\n\n\n2)Initial State",
                            st.session_state.Initial,
                            "\n\n\n\n\n",
                        )
                        st.session_state.extracted = True
                        # st.text_area("Extracted Text", value=st.session_state.sitemap_data, height=300)

                    else:
                        st.error("Error: Invalid sitemap.")

            else:
                url = url_or_xml
                st.session_state.extracted, data = run_function(url, documents)

            if st.session_state.extracted:
                if is_a_sitemap:
                    st.text_area(
                        "Extracted Text",
                        value=st.session_state.sitemap_data,
                        height=300,
                    )
                col1, col2 = st.columns([0.5, 0.5])

                with col1:
                    saved_button = False
                    if st.button("Save", key="b_save"):
                        file_name = "output.txt"

                        # Define the folder path
                        folder_path = "extracted data"

                        # Create the folder if it doesn't exist
                        os.makedirs(folder_path, exist_ok=True)

                        # Define the file path
                        file_path = os.path.join(folder_path, file_name)
                        if is_a_sitemap:
                            saved_data = st.session_state.sitemap_data
                            # Save string variable to file
                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(saved_data)
                        else:
                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(data)
                        saved_button = True

                with col2:
                    if st.button("Clear"):
                        st.session_state.button_enter = False
                        st.session_state.Initial = True
                        st.session_state.extracted = False
                        if "sitemap_data" in st.session_state:
                            del st.session_state["sitemap_data"]
                        st.session_state.button_enter = False
                        st.experimental_rerun()

                if saved_button:
                    # Confirmation message
                    st.success(f"File saved as {file_name} in the current directory.")

            else:
                st.warning("Data not extracted")


if __name__ == "__main__":
    main()
