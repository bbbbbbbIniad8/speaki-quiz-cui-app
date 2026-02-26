class CUIApp:
    def __init__(self):
        self.line = "=" * 80

    def title(self, text):
        print(f"{self.line}\n{text}\n{self.line}")
    
    def input_option(self, option_lst, sentence="", index=1):
        print(sentence)
        for index, text in enumerate(option_lst, start=index):
            print(f"[{index}: {text}]")
        user_input = input(": ")
        self.print_one_line()
        return user_input.strip()
    
    def print_header(self, text):
        print(f"{self.line}\n{text}\n{self.line}\n")

    def input_Yn(self, query):
        user_answer = input(query).strip()
        return True if user_answer == "Y" else False
    
    def input_mod(self, text):
        user_input = input(f"{text}")
        return user_input.strip()
    
    def print_one_line(self):
        print(f"\n{self.line}\n")
