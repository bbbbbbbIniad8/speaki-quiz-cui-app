class CUIApp:
    def __init__(self):
        self.line = "=" * 80

    def title(self, text):
        print(f"{self.line}\n{text}\n{self.line}")
    
    def input_option(self, option_lst):
        for index, text in enumerate(option_lst, start=1):
            print(f"[{index}: {text}]")
        print(f"\n数字を選んでください")
        user_input = input(": ")
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
