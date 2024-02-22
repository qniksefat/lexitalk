import streamlit as st
import pandas as pd
from typing import List

from llama_index.schema import MetadataMode, NodeWithScore

from core.st_config import example_questions, welcome_messages
from core.utils import convert_timestamp_str_to_seconds, parse_timestamp


def generate_sources_df(
    source_nodes: List[NodeWithScore]) -> pd.DataFrame:
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


def display_videos(df_sources: pd.DataFrame):    
        ratio_columns = [2, 1]

        for episode_number, episode_group in df_sources.groupby("episode_number"):
            col1, col2 = st.columns(ratio_columns)
            
            # take the first row of the group to get the episode info
            source_node = episode_group.iloc[0]
            
            guest_names = source_node["guest_names"]
            episode_title = source_node["episode_title"]
            col1.markdown(f"#### {guest_names} | {episode_title}")
                
            timestamp_str = source_node["timestamp"]
            timestamp_str_striped = timestamp_str.lstrip("0:")
            episode_with_timestamp = f"E{episode_number} at {timestamp_str_striped}"
            
            url = source_node["url"]
            url_timed = f"{url}&t={str(convert_timestamp_str_to_seconds(timestamp_str))}"
            
            text = source_node["text"]
            
            col1.markdown(f"**[{episode_with_timestamp}]({url_timed})**")
            col1.write(text)
            
            col2.write("\n")
            col2.video(url, start_time=convert_timestamp_str_to_seconds(timestamp_str))
            
            if len(episode_group) > 1:
                for _, source_node in episode_group.iloc[1:].iterrows():
                    timestamp_str = source_node["timestamp"]
                    timestamp_str_striped = timestamp_str.lstrip("0:")
                    episode_with_timestamp = f"E{episode_number} at {timestamp_str_striped}"
                    
                    url_timed = f"{url}&t={str(convert_timestamp_str_to_seconds(timestamp_str))}"
                    
                    text = source_node["text"]
                    
                    col1.markdown(f"**[{episode_with_timestamp}]({url_timed})**")
                    col1.write(text)
                    
        return None


def st_welcome():
    for message in welcome_messages:
        st.write(message)

def st_example_question_buttons():
    left_col, mid_col, _ = st.columns([1, 4, 1])
    left_col.markdown("**Example Questions:**")
    cols = mid_col.columns(len(example_questions))
    
    for i, question in enumerate(example_questions):
        with cols[i]:
            if st.button(question):
                st.session_state.messages.append({"role": "user", "content": question})

def input_user_question():
    prompt = st.chat_input("Your question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

def display_chat_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def st_response(chat_engine, prompt):
    with st.chat_message("assistant"):
        with st.spinner("This may take a few seconds..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)

            if response.source_nodes:
                st.info(("Click on the links if video is disabled to show outside of"
                         " YouTube, or it doesn't play from the right time."), icon="🎥")
                df_sources = generate_sources_df(response.source_nodes)
                
                display_videos(df_sources)
                with st.expander("Extra Info 📚"):
                    st.dataframe(df_sources)
                
            st.warning("If you want to change the topic, consider refreshing the page.")
            
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)

def st_initialize_chat_messages():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me about any topic!"}
        ]

def st_initialize_chat_engine(chat_engine):
    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = chat_engine
