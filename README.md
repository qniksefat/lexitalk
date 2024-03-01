# LexChat

<p align="center">
  <img src="data/lexitalk-logo.png" alt="Logo" align="middle" width="30%">
</p>

LexChat is a chatbot designed to guide you through discussions and analyze various perspectives from conversation transcripts of the [Lex Fridman Podcast](https://lexfridman.com/podcast). It shows the moments where a topic is discussed and helps you watch it from that time stamp. The chatbot aims to provide balanced responses by considering all sides of an argument. The project is built using Python and integrates with Streamlit for the web interface, Weaviate for vector search, and OpenAI for natural language processing.

## Motivation
I usually find myself diving deep (a true DFS) into the internet, trying to research on my questions. But, the noise is louder than the signal drowning out the nuggets of wisdom that I seek. Finding the high-influential individuals or profound books on a particular subject feels like hunting for a golden needle in a haystack.

This chatbot searches through thousands of hours of talks with brilliant minds. Not just an idea, but its opposing ideas that were discussed during other episodes. Not just transcripts, but the exact timestamps of when an idea was discussed for convenient listening or watching. I can tap into a collective wisdom of the internet with ease.

## Quick Start

You can quickly start using the chatbot by visiting the [lexchat.streamlit.app](https://lexchat.streamlit.app) website. The chatbot will be available for interaction, and you can ask your questions.

<p align="center">
  <video width="85%" controls>
    <source src="https://drive.google.com/uc?export=download&id=1f_-_O5v--c2_SV-Gj3h-dZv4kkaAIZV3" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>

## Usage

You can also run the chatbot locally by following the setup and execution instructions below.

```bash
git clone https://github.com/qniksefat/lexitalk.git
cd lexitalk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Web Interface

From this point, you can run the chatbot through web interface using the following command which will launch a it on your localhost:

```bash
streamlit run streamlit_app.py
```

### Command Line Interface

You can also run the chatbot through the command line interface using the following command:

```bash
python cli_app.py
```

<!-- attach gif how cli works -->

## Dependencies
The project relies on a variety of external libraries and APIs to implement its features:

- **llama-index:** The main library used to build a Retrieval Augmented Generation (RAG) system, enhancing the chatbot's capabilities.
- **pymongo:** Used to store the transcripts and metadata of the podcast episodes.
- **openai and anthropic:** Utilized for Large Language Model (LLM) integration behind the chatbot, enhancing natural language processing.
- **cohere:** Used for reranking the retrieved context to effectively answer user questions.
- **streamlit:** Facilitates the creation of the web interface, enabling users to interact seamlessly with the chatbot.
- **pandas:** Simple data manipulation tasks within the project.

## Data

### Raw Transcripts
Please note that episdoes are not up to date containing up to episode #325 excluding episodes #84 and #100. The transcripts are available in the `data/raw/all` directory. The transcripts were provided in [Lexicap](https://karpathy.ai/lexicap/) by Andrej Karpathy using Whisper.

### Metadata

### Vector Store Index

The vector store index is built in MongoDB Atlas with the following schema:

```json
{
  "mappings": {
    "dynamic": true,
    "fields": [
      {
        "numDimensions": 1536,
        "path": "embedding",
        "similarity": "cosine",
        "type": "vector"
      },
      {
        "path": "metadata.views",
        "type": "filter"
      }
    ]
  }
}
```
## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or ideas for improvement.
