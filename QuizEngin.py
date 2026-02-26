import random
import pandas as pd


class QuizEngin():
    def __init__(self, path, mode="nomal", answer_type="input"):
        self.path = path
        self.miss_lst = []
        self.df = pd.read_csv(path, sep=",", header=0)
        self.df.index.name = "index"
        if "index" in self.df.columns:
            self.df = self.df.drop(columns=["index"])
        all_data = self.df.reset_index().to_dict('records')
        self.quiz_lst = [item for item in all_data if item["miss"] == True] if mode == "miss" else all_data
        if "miss" not in self.df.columns:
            self.df.assign(miss=False)
    
    def prepare(self):
        random.shuffle(self.quiz_lst)
        self.miss_lst.clear()
    
    def marking(self, user_input, answer):
        peke = "     "
        peke2 = peke
        for input_char, answer_char in zip(user_input, answer):
            try:
                peke += "-" if input_char == answer_char else "^"
                peke2 += " " if input_char == answer_char else answer_char
            except:
                peke += "^"
                peke2 += " "
        print(peke)
        print(peke2)

    def create_select_ans(self, answer):
        select_lst = random.sample([d["answer"] for d in self.quiz_lst], 5)
        if answer not in select_lst:
            insert_index = random.randint(0, len(select_lst)-1)
            select_lst[insert_index] = answer
        return select_lst
        

    def check_answer(self, index, user_input, quiz, answer):
        if user_input == answer:
            self.df.at[index, "miss"] = False
            return True
        else:
            self.df.at[index, "miss"] = True
            self.miss_lst.append((answer, quiz))
            return False

    def save_csv(self):
        self.df.to_csv(self.path)
