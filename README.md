# LexiTalk


<img src="data/lexitalk-logo.png" alt="Logo" align="middle" width="100">


LexiTalk is a chatbot designed to guide you through discussions and analyze various perspectives from conversation transcripts of the Lex Fridman Podcast [(link)](https://lexfridman.com/podcast). It shows the moments where a topic is discussed and helps you watch it from that time stamp. The chatbot aims to provide balanced responses by considering all sides of an argument. The project is built using Python and integrates with Streamlit for the web interface, Weaviate for vector search, and OpenAI for natural language processing.

## Motivation
I usually find myself diving deep (a true DFS) into the internet, trying to research on my questions. But, the noise is louder than the signal drowning out the nuggets of wisdom that I seek. Finding the high-influential individuals or profound books on a particular subject feels like hunting for a golden needle in a haystack.

This chatbot searches through thousands of hours of talks with brilliant minds. Not just an idea, but its opposing ideas that were discussed during other episodes. Not just transcripts, but the exact timestamps of when an idea was discussed for convenient listening or watching. I can tap into a collective wisdom of the internet with ease.

## Quick Start

You can quickly start using the chatbot by visiting the [lexitalk.streamlit.app](https://lexitalk.streamlit.app) website. The chatbot will be available for interaction, and you can ask your questions.

<img src="data/video-screen.gif" width="400" alt="Video Screen of the App">

## Usage

You can also run the chatbot locally by following the setup and execution instructions below.

```bash
git clone https://github.com/qniksefat/lexitalk.git
cd lexitalk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

It launches a web interface where you can interact with the chatbot.

## Dependencies
The project relies on a variety of external libraries and APIs to implement its features:

- **llama-index:** The main library used to build a Retrieval Augmented Generation (RAG) system, enhancing the chatbot's capabilities.
- **weaviate:** Employed as the online vector database for efficient vector search functionality.
- **openai and anthropic:** Utilized for Large Language Model (LLM) integration behind the chatbot, enhancing natural language processing.
- **cohere:** Used for reranking the retrieved context to effectively answer user questions.
- **streamlit:** Facilitates the creation of the web interface, enabling users to interact seamlessly with the chatbot.
- **pandas:** Simple data manipulation tasks within the project.

### Data Source
Please note that videos #84 and #100 are no longer available. The index "Lexi325" on Weaviate is designated for the first 325 videos in which their transcripts were provided [here](https://karpathy.ai/lexicap/) by Andrej Karpathy using Whisper. 

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or ideas for improvement.
