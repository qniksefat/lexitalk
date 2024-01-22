import streamlit as st
import pandas as pd
from llama_index.schema import MetadataMode

def display_sources(source_nodes) -> None:
    with st.expander("Sources"):
        if len(source_nodes) > 0:
            sources_df_list = []
            for text_node in source_nodes:
                sources_df_list.append(
                    {
                        "Episode Number": text_node.metadata["episode_number"],
                        "Timestamp": text_node.metadata["timestamp"],
                        "Text": text_node.node.get_content(
                            metadata_mode=MetadataMode.NONE),
                    }
                )
            sources_df = pd.DataFrame(sources_df_list)
            st.dataframe(sources_df)
