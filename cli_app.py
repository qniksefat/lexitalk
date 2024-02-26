from ui_utils import (
    View, 
    Controller,
    SAMPLE_QUESTIONS,
)

from core import build_chat_engine

class CLIView(View):
    def init_view(self):
        print("Chat with Lex Fridman's Guests!")
        print("Type 'exit' or 'quit' to end the conversation. Type 'help' for assistance.")

    def input_user_question(self):
        return input("\nYou: ")

    def display_response_and_sources(self, response):
        print("\nAssistant: ", end="")
        response.print_response_stream()
        print("\n")
        
    def display_help(self):
        print("\nHelp Guide:")
        print("Type your question directly and press Enter.")
        print("Example questions you can ask:")
        for question in self.get_sample_questions(4):
            print(f"- {question}")
        print("Type 'exit' to quit the application.\n")
        
    def get_sample_questions(self, n):
        return SAMPLE_QUESTIONS[:n]


class CLIController(Controller):
    def run(self):
        self.chat_engine.reset()
        self.view.init_view()
        
        while True:
            user_input = self.view.input_user_question()
            if user_input.lower() == 'help':
                self.view.display_help()
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            response = self.process_user_input(user_input)
            self.view.display_response_and_sources(response)


if __name__ == "__main__":
    chat_engine = build_chat_engine()
    view = CLIView()
    controller = CLIController(view, chat_engine)
    controller.run()
