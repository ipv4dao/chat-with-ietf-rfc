import pickle
from query_data import get_chain
from dotenv import load_dotenv
import openai
import os
import warnings

if __name__ == "__main__":
    #There are some langchain erros that are not important, so we hide them
    warnings.filterwarnings("ignore")
    #loading the openai api key
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    #loading the vectorstore
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    qa_chain = get_chain(vectorstore)
    chat_history = []
    print("Chat with Internet Engineering Task Force!")
    while True:
        print("Human:")
        question = input()
        result = qa_chain({"question": question, "chat_history": chat_history})
        print(result)
        chat_history.append((question, result["answer"]))
        print("AI:")
        print(result["answer"])