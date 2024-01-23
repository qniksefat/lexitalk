import streamlit as st
import pandas as pd
from llama_index.schema import MetadataMode


def display_sources(source_nodes) -> None:
    if not source_nodes:    return None

    sources_df_list = []
    for source_node in source_nodes:
        sources_df_list.append(
            {
                "Episode Num": source_node.metadata["episode_number"],
                "Guest": source_node.metadata["guest_names"],
                "Title": source_node.metadata["episode_title"],
                "Timestamp": source_node.metadata["timestamp"],
                "Text": source_node.node.get_content(
                    metadata_mode=MetadataMode.NONE),
                "URL": source_node.metadata["url"],
            }
        )
    sources_df = pd.DataFrame(sources_df_list)
    
    st.info("Click on the video to play it from the moment topic was discussed.", icon="🎥")
    
    for i, source_node in enumerate(source_nodes):
        col1, col2 = st.columns([1, 1])
        episode_number = source_node.metadata["episode_number"]
        timestamp = source_node.metadata["timestamp"]
        title_label = source_node.metadata["episode_title"]
        url = source_node.metadata["url"]
        target_url = f"{url}&t={str(convert_timestamp(timestamp))}"
        text = source_node.node.get_content(metadata_mode=MetadataMode.NONE)
        guest_names = source_node.metadata["guest_names"]
        
        col1.markdown(f"**Source {i+1} | "
                      f"E{episode_number} at {timestamp[:-4]} | "
                      f"{guest_names} | "
                      f"[{title_label}]({target_url}):**")
        col1.write(text)
        
        col2.video(url, start_time=convert_timestamp(timestamp))
        
    with st.expander("Extra Info 📚"):
        st.dataframe(sources_df)
            
            
def convert_timestamp(timestamp: str) -> int:
    """Converts a timestamp string to seconds.

    Args:
        timestamp (str): Timestamp string. It can be formatted as "HH:MM:SS.mmm" or "MM:SS.mmm".

    Returns:
        int: Number of seconds.
    """
    from datetime import datetime, timedelta
    try:
        time = datetime.strptime(timestamp, "%H:%M:%S.%f")
    except ValueError:
        time = datetime.strptime(timestamp, "%M:%S.%f")
    seconds = timedelta(
        hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond).total_seconds()
    return int(seconds)
