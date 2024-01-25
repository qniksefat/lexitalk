# lexitalk

## Overview
The "LexiTalk" project is a chatbot application designed to engage users in discussions by analyzing various perspectives from conversation transcripts of the Lex Fridman Podcast. The chatbot aims to provide balanced responses by considering all sides of an argument. The project is built using Python and integrates with Streamlit for the web interface, Weaviate for vector search, and OpenAI for natural language processing.

## Project Usage
Users interact with the chatbot through a Streamlit interface, where they can ask questions related to the Lex Fridman Podcast. The chatbot uses the vector index to retrieve relevant information and generate responses that consider different perspectives.

### Live Demo
The project is currently up and running on [lexitalk.streamlit.app](https://lexitalk.streamlit.app).

### Data Source
Please note that videos #84 and #100 are no longer available. The index "Lexi325" on Weaviate is designated for the first 325 videos.

## Dependencies
The project relies on a variety of external libraries and APIs to implement its features:

- **llama-index:** The main library used to build a Retrieval Augmented Generation (RAG) system, enhancing the chatbot's capabilities.
- **weaviate:** Employed as the online vector database for efficient vector search functionality.
- **openai and anthropic:** Utilized for Large Language Model (LLM) integration behind the chatbot, enhancing natural language processing.
- **cohere:** Used for reranking the retrieved context to effectively answer user questions.
- **streamlit:** Facilitates the creation of the web interface, enabling users to interact seamlessly with the chatbot.
- **pandas:** Essential for data manipulation tasks within the project.

## Setup and Execution
To run the project, one would need to set up the appropriate environment with the necessary dependencies installed. The main application can be started by running `streamlit run main.py`, which will launch the Streamlit web interface for user interaction.
