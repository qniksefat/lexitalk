from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
import pandas as pd

from llama_index.schema import MetadataMode, NodeWithScore


# UI constants

filename_sample_questions = "data/sample_questions.txt"

with open(filename_sample_questions, "r") as file:
    all_sample_questions = file.readlines()
    all_sample_questions = [question.strip() for question in all_sample_questions]
    
ascii_art_welcome = """
  _                  _____ _           _     _ 
 | |                / ____| |         | |   | |
 | |     _____  __ | |    | |__   __ _| |_  | |
 | |    / _ \ \/ / | |    | '_ \ / _` | __| | |
 | |___|  __/>  <  | |____| | | | (_| | |_  |_|
 |______\___/_/\_\  \_____|_| |_|\__,_|\__| (_)
                                               
"""

MAX_MESSAGE_LENGTH = 1000


# UI abstract classes

class View(ABC):
    @abstractmethod
    def input_user_question(self):
        pass
    
    @abstractmethod
    def display_response_and_sources(self, response):
        pass


class Controller(ABC):
    def __init__(self, view, chat_engine):
        self.view = view
        self.chat_engine = chat_engine
    
    @abstractmethod
    def run(self):
        pass
    
    def process_user_input(self, user_input):
        
        if len(user_input) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message length exceeds {MAX_MESSAGE_LENGTH} characters.")
                
        response = self.chat_engine.stream_chat(user_input)
        return response


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
    df['episode_top_relevance'] = df.groupby("episode_number")['score'].transform('max')
    df = df.sort_values(['episode_top_relevance', 'timestamp'], ascending=[False, True])
    df["timestamp"] = df["timestamp"].apply(lambda x: x.strftime("%H:%M:%S"))
    return df
