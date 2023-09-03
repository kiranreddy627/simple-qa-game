import tkinter as tk
from tkinter import messagebox
import html
import json
import random
import requests
import sys

def fetch_question():
    global correct, wrong, current_question_correct_answer, answer_buttons, correct_answer_label
    url = "https://opentdb.com/api.php?amount=1&category=18&difficulty=easy&type=multiple"
    r = requests.get(url)

    if r.status_code != 200:
        messagebox.showerror("Error", "Sorry, we are unable to process the question. Click OK to quit.")
        sys.exit()  # Terminate the entire process
    else:
        data = json.loads(r.text)
        question = html.unescape(data["results"][0]["question"])
        answers = data["results"][0]["incorrect_answers"]
        correct_answer = data["results"][0]["correct_answer"]
        answers.append(correct_answer)
        random.shuffle(answers)
        
        question_label.config(text=question, wraplength=400)
        for i, answer in enumerate(answers):
            answer_buttons[i].config(text=answer, state=tk.NORMAL, wraplength=400)

        # Update the correct answer for the current question
        current_question_correct_answer = correct_answer

def check_answer(selected_answer):
    global correct, wrong, answer_buttons, correct_answer_label
    correct_answer = current_question_correct_answer
    correct_answer_label.config(text=f"Correct Answer: {correct_answer}")
    
    if selected_answer == correct_answer:
        correct += 1
        result_label.config(text="Correct!", fg="green")
    else:
        wrong += 1
        result_label.config(text="Wrong!", fg="red")

    score.set(f"Score: {correct * 4 - wrong}")
    correct_answers.set(f"Correct Answers: {correct}")
    wrong_answers.set(f"Wrong Answers: {wrong}")

    for button in answer_buttons:
        button.config(state=tk.DISABLED)

    next_button.config(state=tk.NORMAL)
    quit_button.config(state=tk.NORMAL)

def next_question():
    global answer_buttons, correct_answer_label
    for button in answer_buttons:
        button.config(state=tk.NORMAL)
    result_label.config(text="")
    correct_answer_label.config(text="")
    next_button.config(state=tk.DISABLED)
    quit_button.config(state=tk.DISABLED)
    fetch_question()

def quit_game():
    result_label.config(text="")
    correct_answer_label.config(text="")
    message = f"Thank you for playing!\nCorrect Answers: {correct}\nWrong Answers: {wrong}\nScore: {correct * 4 - wrong}"
    messagebox.showinfo("Game Over", message)
    root.quit()

def start_game():
    global correct, wrong, current_question_correct_answer, answer_buttons, correct_answer_label
    correct = 0
    wrong = 0
    current_question_correct_answer = None
    fetch_question()
    for button in answer_buttons:
        button.config(state=tk.NORMAL)
    result_label.config(text="")
    correct_answer_label.config(text="")
    start_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Trivia Quiz Game")

# Initialize variables
correct = 0
wrong = 0
current_question_correct_answer = None

# Create GUI elements
question_label = tk.Label(root, text="", wraplength=400, justify="center")
question_label.pack(pady=20)

answer_buttons = []
for i in range(4):
    answer_button = tk.Button(root, text="", width=40, command=lambda i=i: check_answer(answer_buttons[i]['text']), state=tk.DISABLED, wraplength=400)
    answer_buttons.append(answer_button)
    answer_button.pack(pady=5)

result_label = tk.Label(root, text="", fg="green", font=("Arial", 16))
result_label.pack(pady=10)

correct_answer_label = tk.Label(root, text="", fg="blue")
correct_answer_label.pack(pady=5)

score = tk.StringVar()
correct_answers = tk.StringVar()
wrong_answers = tk.StringVar()

score_label = tk.Label(root, textvariable=score)
correct_answers_label = tk.Label(root, textvariable=correct_answers)
wrong_answers_label = tk.Label(root, textvariable=wrong_answers)

score_label.pack()
correct_answers_label.pack()
wrong_answers_label.pack()

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

next_button = tk.Button(root, text="Next", command=next_question, state=tk.DISABLED)
next_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_game, state=tk.DISABLED)
quit_button.pack(pady=10)

root.mainloop()