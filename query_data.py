from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
You can assume the question about Internet development.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assistant for answering questions about Internet development based on IETF RFCs.
You are given the following extracted parts of a RFCs and a question. Provide a conversational answer.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not related to Internet development or IETF RFCs, politely inform them that you are tuned to only answer questions about the most recent state of the union.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])



def get_chain(vectorstore):
    #Change the temperature to 0, if you want it to be super accurate.
    #Change the model_name to "gpt-3.5-turbo" for a faster response time and less credit consumption
    #Attention gpt-3.5-turbo may not have enough tokens to answer your question
    llm = OpenAI(temperature=0.1, model_name="gpt-4-0314", timeout=120)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )
    return qa_chain
