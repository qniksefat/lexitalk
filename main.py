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


username = "qniksefat"
password = st.secrets["mongodb_password"]
url = st.secrets["mongodb_url"]
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBClient:
    def __init__(self, connection_uri, database_name, collection_name):
        self.client = MongoClient(connection_uri, server_api=ServerApi('1'))
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def ping_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

connection_uri = (f"mongodb+srv://{username}:{password}@{url}/?retryWrites=true&w=majority")
monngodb_client = MongoDBClient(connection_uri, 
                             database_name = 'default_db',
                             collection_name = 'default_collection')

st.write(
    monngodb_client.collection.find_one()
)