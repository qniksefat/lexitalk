import streamlit as st

from core import build_chat_engine

from ui_utils import (
    View,
    Controller,
    convert_timestamp_seconds, 
    nodes_to_sorted_dataframe,
    welcome_messages,
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

    def display_response(self, response):
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
        for message in welcome_messages:
            st.write(message)
    
    @staticmethod
    def _st_display_question_buttons():
        left_col, mid_col, _ = st.columns([1, 4, 1])
        left_col.markdown("**Example Questions:**")
        cols = mid_col.columns(len(example_questions))
        for i, question in enumerate(example_questions):
            with cols[i]:
                if st.button(question):
                    st.session_state.messages.append({"role": "user", "content": question})
    
    
    def _st_display_response(self, response):
        st.write(response.response)

        if response.source_nodes:
            st.info(("Click on the links if video is disabled to show outside of"
                        " YouTube, or it doesn't play from the right time."), icon="🎥")
            df_sources = nodes_to_sorted_dataframe(response.source_nodes)
            
            self._display_source_videos(df_sources)
            with st.expander("Extra Info 📚"):
                st.dataframe(df_sources)
            
        st.warning("If you want to change the topic, consider refreshing the page.", icon="🔄")
        
        message = {"role": "assistant", "content": response.response}
        st.session_state.messages.append(message)
        
    @staticmethod
    def _display_source_videos(df_sources):    
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
            url_timed = f"{url}&t={str(convert_timestamp_seconds(timestamp_str))}"
            
            text = source_node["text"]
            
            col1.markdown(f"**[{episode_with_timestamp}]({url_timed})**")
            col1.write(text)
            
            col2.write("\n")
            col2.video(url, start_time=convert_timestamp_seconds(timestamp_str))
            
            if len(episode_group) > 1:
                for _, source_node in episode_group.iloc[1:].iterrows():
                    timestamp_str = source_node["timestamp"]
                    timestamp_str_striped = timestamp_str.lstrip("0:")
                    episode_with_timestamp = f"E{episode_number} at {timestamp_str_striped}"
                    
                    url_timed = f"{url}&t={str(convert_timestamp_seconds(timestamp_str))}"
                    
                    text = source_node["text"]
                    
                    col1.markdown(f"**[{episode_with_timestamp}]({url_timed})**")
                    col1.write(text)



class StreamlitController(Controller):
    def __init__(self, view, chat_engine):
        super().__init__(view, chat_engine)
        self.init_chat_engine()
        self.init_chat_messages()

    def run(self):
        self.view.init_view()
        self.view.input_user_question()
        self.view.display_chat_messages(st.session_state.messages)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("This may take a few seconds..."):
                        
                    user_input = st.session_state.messages[-1]["content"]
                    response = self.process_user_input(user_input)
                    self.view.display_response(response)

    def process_user_input(self, user_input):
        response = self.get_chat_engine().chat(user_input)
        return response
    
    def init_chat_engine(self):
        if "chat_engine" not in st.session_state.keys():
            st.session_state.chat_engine = self.chat_engine
        
    def get_chat_engine(self):
        return st.session_state.chat_engine
    
    def init_chat_messages(self):
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me about any topic!"}]


if __name__ == "__main__":
    view = StreamlitView()
    chat_engine = build_chat_engine()
    controller = StreamlitController(view, chat_engine)
    controller.run()
