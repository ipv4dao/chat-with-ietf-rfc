# IETF RFCs AI Assistant

This repository contains an AI assistant for answering questions about Internet development based on IETF RFCs (Internet Engineering Task Force Request for Comments). The assistant is built using OpenAI's GPT-4 and the langchain library for efficient document retrieval.

## Features

- Answers questions about Internet development and IETF RFCs
- Supports conversational context to maintain the flow of the conversation
- Efficiently searches through RFC documents using langchain's vectorstore

## Repository Structure

- `query_data.py`: Defines the prompts and chat chain for the AI assistant
- `ingest_rfc.py`: Contains functions for downloading, extracting, and preparing RFC documents
- `cli_app.py`: CLI application for interacting with the AI assistant

## Setup

1. Clone this repository
2. Install the required dependencies: `pip install langchain openai dotenv`
3. Set up your OpenAI API key in an `.env` file or as an environment variable (`OPENAI_API_KEY`)
4. Run `ingest_rfc.py` to download and process the RFC documents
5. Run `cli_app.py` to start the CLI application and chat with the AI assistant

## Usage

1. Run the CLI application: `python cli_app.py`
2. You will be greeted with the following message: "Chat with Internet Engineering Task Force!"
3. Enter your question related to Internet development or IETF RFCs
4. The AI will answer your question, maintaining the context of the conversation

## Notes

- Running `ingest_rfc.py` may take some time and consume OpenAI credits, as it uses their embeddings model to vectorize the documents
- If you encounter any SSL certificate errors, the `ingest_rfc.py` script includes a fix
