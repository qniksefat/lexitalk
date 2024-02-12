import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import BulkWriteError


class MongoDBClient:
    def __init__(self, database_name, collection_name, index_name):
        self.index_name = index_name
        self.client = MongoClient(self.get_connection_uri(), server_api=ServerApi('1'))
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_many(self, data):
        try:
            self.collection.insert_many(data)
        except BulkWriteError as e:
            for error in e.details['writeErrors']:
                if error['code'] == 11000:  # Duplicate key error code
                    # Handle the duplicate error here
                    pass

    def count_documents(self):
        return self.collection.count_documents({})

    def get_connection_uri(self):
        username = st.secrets["mongodb_username"]
        password = st.secrets["mongodb_password"]
        url = st.secrets["mongodb_url"]
        connection_uri = (f"mongodb+srv://{username}:{password}@{url}/"
                          "?retryWrites=true&w=majority")
        return connection_uri
