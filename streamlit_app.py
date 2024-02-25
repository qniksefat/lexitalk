import streamlit as st

# To stream the responses in Streamlit, we need to use nest_asyncio
import nest_asyncio
nest_asyncio.apply()
import time

from core import build_chat_engine

from ui_utils import (
    View,
    Controller,
    convert_timestamp_seconds, 
    nodes_to_sorted_dataframe,
    example_questions,
)


class StreamlitView(View):
    def init_view(self):
        self._st_page_config()
        st.title("Chat with Lex Fridman's Guests 💬")
        st.write("\n")
        self._st_display_welcome()
        st.write("\n")

    def input_user_question(self):
        self._st_display_question_buttons()
        prompt = st.chat_input("Your question")
        if prompt:
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

    def display_chat_messages(self, messages):
        for message in messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def display_response_and_sources(self, response):
        self._st_display_response(response)


    @staticmethod
    def _st_page_config():
        st.set_page_config(
            page_title="LexChat 💬",
            page_icon="🎙️",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                "About": "This is a Streamlit app for conversing with Lex Fridman's guests.",
                "Report a bug": "https://github.com/qniksefat/lexitalk/issues/new",
                "Get help": "https://github.com/qniksefat/lexitalk/",
            }
        )
        
    @staticmethod
    def _st_display_welcome():
        with st.expander((
            "Welcome aboard our AI-driven magic carpet! Ask your question, click on the examples, or click here"
            " to know more."),
                         expanded=False):
            st.success((
                "This is a conversational AI that has been trained on the transcripts of the [Lex Fridman"
                " Podcast](https://lexfridman.com/podcast)."
                "\n\nIt looks for the most relevant part of the podcast where the question is discussed and"
                " provides a link to the video."),
                       icon="💡")
            st.warning((
                "The search engine is not up-to-date with the latest episodes. It is trained on the"
                " episodes up to **#325** excluding #84 and #100 due to deletion of the original videos."
                "\n\nThe videos are from the [Lex Fridman YouTube](https://www.youtube.com/c/LexFridman)."
                " and the transcripts are from the project [Lexicap](https://karpathy.ai/lexicap/) by"
                " Andrej Karpathy using OpenAI's [Whisper](https://openai.com/research/whisper)."),
                       icon="📁")
            st.info(("You can click on the videos to watch them from the moment the topic is discussed. If this"
                     " is a _**video unavailable**_, click on the blue link to watch it directly on YouTube."),
                        icon="🎥")
            st.error("Similar to ChatGPT, it gets confused if the topic is changed. Consider refreshing the page.",
                        icon="🔄")
    
    @staticmethod
    def _st_display_question_buttons():
        left_col, mid_col, _ = st.columns([1, 4, 1])
        left_col.write("\n")
        left_col.markdown("**Example Questions:**")
        cols = mid_col.columns(len(example_questions))
        for i, question in enumerate(example_questions):
            with cols[i]:
                if st.button(question):
                    st.session_state.messages.append({"role": "user", "content": question})
    
    
    def _st_display_response(self, response, streaming=True):
        self._display_generated_response(response, streaming)

        if response.source_nodes:
            st.write("\n")
            st.info(("Click on the links if video is disabled to show outside of"
                        " YouTube, or it doesn't play from the right time."), icon="🎥")
            df_sources = nodes_to_sorted_dataframe(response.source_nodes)
            self._display_source_videos(df_sources, streaming)
            
            with st.expander("Sources 📚", expanded=False):
                df_sources = df_sources.drop(columns=["url", "episode_top_relevance"])
                st.dataframe(df_sources)
        
        st.warning("If you want to change the topic, consider refreshing the page.")


    def _display_generated_response(self, response, streaming):
        if streaming:
            st.write_stream(response.response_gen)
        else:
            st.write(response.response)
        
        message = {"role": "assistant", "content": response.response}
        st.session_state.messages.append(message)
        
        
    def _display_source_videos(self, df_sources, streaming):
        ratio_columns = [2, 1]
        
        # we keep the top relevance of each episode
        df_grouped = df_sources.groupby(['episode_top_relevance', 'episode_number'])
        # we want to iterate over episodes in the order of the top_relevance
        df_grouped = sorted(df_grouped, key=lambda x: x[0][0], reverse=True)

        for (episdoepisode_top_relevance, episode_number), episode_group in df_grouped:
            if streaming:
                time.sleep(0.5)
            st.write("\n")
            
            col_text, col_video = st.columns(ratio_columns)
            
            # Display episode information
            first_source_node = episode_group.iloc[0]
            guest_names = first_source_node["guest_names"]
            episode_title = first_source_node["episode_title"]
            col_text.markdown(f"#### {guest_names} | {episode_title}")
            
            # Display the video for the first node
            self._display_one_source_node(first_source_node, col_text, col_video, show_video=True, show_url=True)
            
            prev_timestamp = convert_timestamp_seconds(first_source_node["timestamp"])
            
            # Iterate over the rest of the nodes in the episode group
            for _, source_node in episode_group.iloc[1:].iterrows():
                timestamp = convert_timestamp_seconds(source_node["timestamp"])
                show_url = (timestamp - prev_timestamp) > 120
                prev_timestamp = timestamp
                
                self._display_one_source_node(source_node, col_text, col_video,
                                              show_video=False, show_url=show_url)


    @staticmethod
    def _display_one_source_node(source_node,
                                 col_text, col_video, 
                                 show_video: bool,
                                 show_url: bool):
        
        episode_number = source_node["episode_number"]
        timestamp_str = source_node["timestamp"]
        
        # If the timestamp is not at the start or at the first minute, remove leading "0:"
        timestamp_str_striped = timestamp_str.lstrip("0:") if timestamp_str not in ["00:00:00", "00:00"] else "00:00"
            
        episode_with_timestamp = f"E{episode_number} at {timestamp_str_striped}"
        
        url = source_node["url"]
        url_timed = f"{url}&t={str(convert_timestamp_seconds(timestamp_str))}"
        

        if show_url:
            col_text.markdown(f"**[{episode_with_timestamp}]({url_timed})**")            
        
        text = source_node["text"]
        col_text.write(text)
        
        if show_video:
            col_video.write("\n")
            col_video.video(url_timed)    
    

class StreamlitController(Controller):
    def __init__(self, view: StreamlitView, chat_engine):
        super().__init__(view, chat_engine)
        self.init_chat_engine()
        self.init_chat_messages()

    def run(self):
        self.view.init_view()
        self.view.input_user_question()
        self.view.display_chat_messages(st.session_state.messages)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner(" 🔍 🤖 Searching and Thinking..."):
                        
                    user_input = st.session_state.messages[-1]["content"]
                    response = self.process_user_input(user_input)
                    self.view.display_response_and_sources(response)
        
    def init_chat_engine(self):
        if "chat_engine" not in st.session_state.keys():
            st.session_state.chat_engine = self.chat_engine
        
    def get_chat_engine(self):
        return st.session_state.chat_engine
    
    def init_chat_messages(self):
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! Ask me anything."}]


if __name__ == "__main__":
    view = StreamlitView()
    chat_engine = build_chat_engine()
    controller = StreamlitController(view, chat_engine)
    controller.run()
