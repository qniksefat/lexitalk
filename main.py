import streamlit as st

st.set_page_config(
    page_title="LexChat",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": ("LexiTalk guides you through [Lex Fridman Podcast](https://lexfridman.com/podcast) "
                  "first 325 episodes taking transcripts from [here](https://karpathy.ai/lexicap/) unraveling perspectives.")

    },
)

st.title("Chat with Lex Fridman's Guests 💬")

st.info("Welcome aboard our AI-driven magic carpet! Journey through the fascinating depths"
        " of minds from Lex Fridman Podcast [(link)](https://lexfridman.com/podcast). Decide YOUR"
        " sources of truth. No reading required—just click and listen from the moment of discussion!",
        icon="💡")


import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Failed to retrieve public IP"
    except requests.RequestException as e:
        return "Error: " + str(e)

public_ip = get_public_ip()
st.write("my public IP address is:", public_ip)
