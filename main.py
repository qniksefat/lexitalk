# main.py
import streamlit as st

def main():
    st.title("Simple Streamlit App")

    # Get user input
    user_input = st.text_input("Enter text:")

    # Display the input when the button is pressed
    if st.button("Echo"):
        st.write(f"You entered: {user_input}")

if __name__ == "__main__":
    main()
