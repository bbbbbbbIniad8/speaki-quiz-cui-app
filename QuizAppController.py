from CUIApp import CUIApp
from QuizEngin import QuizEngin
import random
import pygame
import time
import os
import threading
import pandas as pd


def play_audio(file_path, wait=False, duration=0):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    if wait == True:
        if duration == 0:
            while pygame.mixer.music.get_busy(): 
                time.sleep(0.1)
        else:
            time.sleep(duration)
        pygame.mixer.quit()


class QuizAppController():
    def __init__(self):
        self.ui = CUIApp()
        self.line = self.ui.line
        self.mode_dict = {"1":"nomal", "2":"miss"}
        self.history = []

    def set_quiz(self, path, mode="nomal"):
        self.quizEngin = QuizEngin(path, mode)
        self.quiz_lst = self.quizEngin.quiz_lst

    def play_audio_spk(self, name, wait=False, duration=0,):
        audio_file = {  "spk": "spk/speaki.mp3", 
                        "chuayo": "spk/chuayo.mp3",
                        "uaa": "spk/uaa.mp3",
                        "aau": "spk/aau.mp3",
                        "squash": "spk/squash.mp3",
                        "deruzibazeyo": "spk/deruzibazeyo.mp3",
                        "notviolence": "spk/notviolence.mp3",
                        "deruzzionly": "spk/deruzibazeyoonly.mp3"
                     }
        if wait == False:
            thread = threading.Thread(target=play_audio, args=(audio_file[name], False, duration))
            thread.daemon = True
            thread.start()
        else:
            play_audio(audio_file[name], True, duration)

    def read_history(self):
        self.history = pd.read_csv("history.csv", sep=",", header=0)
        self.history_lst = self.history.tail(5)["path"].tolist()

    def write_history(self):
        self.history.loc[len(self.history)] = [self.path]
        self.history.to_csv("history.csv")

    def processing_quiz(self):
        for i, element in enumerate(self.quiz_lst, start=1):
            index, quiz, answer = element["index"], element["quiz"], element["answer"]
            while True:
                print(f"{self.line}\n第{i}問\n{{Q}}".format(Q = f"以下の日本語を英語に直しなさい\n{quiz}"))
                self.play_audio_spk("spk")
                user_input = self.ui.input_mod("入力:")
                if user_input == "end":
                    self.retry()
                    continue
                correct = self.quizEngin.check_answer(index, user_input, quiz, answer)
                break
            if correct:
                self.ui.print_header("正解!!")
                self.play_audio_spk("chuayo", wait=True)
            else:
                self.quizEngin.marking(user_input, answer)
                print(f"不正解\n正解は{answer}")
                self.ui.print_one_line()
                if random.randint(0, 1) == 0:
                    self.play_audio_spk("aau", wait=True)
                else:
                    self.play_audio_spk("uaa", wait=True)
            

    def show_result(self):
        self.miss_lst = self.quizEngin.miss_lst
        quiz_count, miss_count = len(self.quiz_lst), len(self.miss_lst)
        if miss_count <= 0:
            self.ui.print_header("全問正解しました!!")
            self.play_audio_spk("squash")
        else:
            print(f"{self.line}\n{quiz_count}問中{miss_count}問間違えました。\n間違えた単語は以下の通りです。")
            if (miss_count / quiz_count) <= 0.75:
                self.play_audio_spk("deruzibazeyo")
            else:
                self.play_audio_spk("notviolence")
                
            for i in self.miss_lst:
                print(f"[{i[0]}:{i[1]}]")
            self.ui.print_one_line()
    
    def quiz(self):
        self.quizEngin.prepare()
        self.processing_quiz()
        self.quizEngin.save_csv()
        self.show_result()
        self.retry()

    def retry(self):
        if self.ui.input_Yn("再挑戦しますか(Y/n)?") == True:
            self.set_quiz(self.path, self.mode)
            self.quiz()
        else:
            exit()

    def run(self):
        main = CUIApp()
        main.title("Welcome To Speaki Quiz")
        self.play_audio_spk("squash", True, 2)
        self.play_audio_spk("spk")
        select = main.input_option(["quiz"], "")
        self.read_history()
        if select == "1":
            while True:
                self.play_audio_spk("spk")
                self.path = main.input_option(self.history_lst, "CSVファイルのパスを入力してください。")
                if os.path.exists(self.path) == True:
                    self.write_history()
                    break
                else:
                    try:
                        self.path = self.history_lst[int(self.path)-1]
                        if os.path.exists(self.path) == True:
                            break
                    except:
                        print("パスが間違っています。")
                        self.play_audio_spk("notviolence", True)
            
            print("ファイルの読み込みに成功しました。")
            self.play_audio_spk("chuayo", True)
            self.ui.print_one_line()
            print("モード選択")
            self.play_audio_spk("spk", True)
            self.mode = self.mode_dict[main.input_option(["nomal", "only_miss"], "数字入力でモードを選択してください。: ")]
            self.set_quiz(self.path, self.mode)
            self.play_audio_spk("chuayo", True)
            self.quiz()
