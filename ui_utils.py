from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
import pandas as pd

from llama_index.schema import MetadataMode, NodeWithScore


# UI constants

welcome_messages = [
    ("Welcome aboard our AI-driven magic carpet! Journey through the fascinating depths"
     " of minds from Lex Fridman Podcast [(link)](https://lexfridman.com/podcast)."),
    "Decide YOUR sources of truth. No reading required—just click and listen from the moment of discussion!",
]
example_questions = [
    "What is the meaning of life and everything?",
    "Is intelligence a gift in personal happiness?",
    "What inspired developing GAN in deep learning?",
    "Is there potential of AI in medicine, like cancer?",
]


# UI abstract classes

class View(ABC):
    @abstractmethod
    def init_view(self):
        pass
    
    @abstractmethod
    def input_user_question(self):
        pass
    
    @abstractmethod
    def display_chat_messages(self, messages):
        pass
    
    @abstractmethod
    def display_response(self, response):
        pass


class Controller(ABC):
    def __init__(self, view, chat_engine):
        self.view = view
        self.chat_engine = chat_engine
    
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def process_user_input(self, user_input):
        pass


# UI helper functions

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parses a timestamp string with or without milliseconds or hours into a datetime object.

    Args:
        timestamp_str (str): The timestamp string to be parsed.

    Returns:
        datetime: The parsed timestamp as a datetime object.
    """
    if "." in timestamp_str:
        # Has milliseconds in the end
        if len(timestamp_str.split(":")) == 3:
            # Has hours in the beginning
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')
        else:
            timestamp = datetime.strptime(timestamp_str, '%M:%S.%f')
    else:
        if len(timestamp_str.split(":")) == 3:
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')
        else:
            timestamp = datetime.strptime(timestamp_str, '%M:%S')
    return timestamp.time()     # No date is in the range of of a video

def convert_timestamp_seconds(timestamp_str: str) -> int:
    """Converts a timestamp string to number of total seconds.

    Returns:
        int: Number of seconds.
    """
    timestamp = parse_timestamp(timestamp_str)
    seconds = timedelta(
        hours=timestamp.hour,
        minutes=timestamp.minute,
        seconds=timestamp.second,
        microseconds=timestamp.microsecond).total_seconds()
    return int(seconds)


def nodes_to_sorted_dataframe(
    source_nodes: List[NodeWithScore]) -> pd.DataFrame:
    """
    Generate a pandas DataFrame from a list of source nodes.

    Args:
        source_nodes (List[NodeWithScore]): A list of source nodes.

    Returns:
        pd.DataFrame: A DataFrame containing the generated data.

    """
    sources_df_list = []
    for source_node in source_nodes:
        sources_df_list.append(
            {
                "score": source_node.score,
                "episode_number": source_node.metadata["episode_number"],
                "guest_names": source_node.metadata["guest_names"],
                "episode_title": source_node.metadata["episode_title"],
                "timestamp": source_node.metadata["timestamp"][:-4],
                "text": source_node.node.get_content(metadata_mode=MetadataMode.NONE),
                "url": source_node.metadata["url"],
            }
        )
    df = pd.DataFrame(sources_df_list)
    df['timestamp'] = df['timestamp'].apply(parse_timestamp)
    df['top_relevance'] = df.groupby("episode_number")['score'].transform('max')
    df = df.sort_values(['top_relevance', 'timestamp'], ascending=[False, True])
    df["timestamp"] = df["timestamp"].apply(lambda x: x.strftime("%H:%M:%S"))
    df = df.drop(columns=['top_relevance'])
    return df
