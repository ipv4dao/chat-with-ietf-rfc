from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import requests
import shutil
import zipfile
import os
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
import nltk
import certifi
import openai

def download_and_extract_rfcs(url, dest_folder, file_extension=".txt"):
    if os.path.exists(dest_folder):
        print(f"The destination folder '{dest_folder}' already exists.")
        return
    os.makedirs(destination_folder, exist_ok=True)
    # Download the ZIP file
    response = requests.get(url)
    zip_filename = os.path.join(dest_folder, "rfcs.zip")

    with open(zip_filename, "wb") as f:
        f.write(response.content)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(dest_folder)

    # Remove the downloaded ZIP file
    os.remove(zip_filename)

    # Remove unwanted subfolders and files
    for root, dirs, files in os.walk(dest_folder):
        for file in files:
            if not file.endswith(file_extension):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))


def remove_byte_sequence(directory, byte_sequence):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        with open(file_path, "rb") as file:
            content = file.read()

        if byte_sequence in content:
            print(f"Removing byte sequence from {file_path}")
            new_content = content.replace(byte_sequence, b'')

            with open(file_path, "wb") as file:
                file.write(new_content)


def remove_files_with_byte_sequence(directory, byte_sequence):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        with open(file_path, "rb") as file:
            content = file.read()

        if byte_sequence in content:
            print(f"Removing file {file_path} containing byte sequence")
            os.remove(file_path)


#Setting up the openai api key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
#Download and extract the All RFCs
#Attention: there may be a lot of files with byte sequencing errors. We'll remove them later.
#It can also consume a lot of your OpenAI credits as we'll use their embeddings model to vectorize the documents.
#rfcs_url = "https://www.rfc-editor.org/in-notes/tar/RFC-all.zip"
#Download the latest RFCs only:
rfcs_url = "https://www.rfc-editor.org/in-notes/tar/RFCs8501-latest.zip"
destination_folder = "./rfcs"
file_glob = "*.txt"
download_and_extract_rfcs(rfcs_url, destination_folder)
#clean the directory from incorrect byte sequences
#There's two ways of doing this: either you add  errors='ignore' to the open() function, or you remove the files with the invalid byte sequences.
#As we're only showcasing the use we'll stick to the last option.
invalid_byte_sequence = b'\xe9'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\xad'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\xc6'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\xe8'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\xc9'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\xe6'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
invalid_byte_sequence = b'\x93'
remove_files_with_byte_sequence(destination_folder, invalid_byte_sequence)
#Fixing SSL certificate error if any
cert_file = certifi.where()
os.environ["SSL_CERT_FILE"] = cert_file
#Downloading nltk punkt
nltk.download("punkt")
#Loading the files
loader = DirectoryLoader("./rfcs/", glob=file_glob, loader_cls=TextLoader)
docs = loader.load()
print(len(docs))
# Split text
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

# Load Data to vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Save vectorstore
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)