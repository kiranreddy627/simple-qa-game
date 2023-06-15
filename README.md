# simple-qa-game
this is a simple computer questions and answers game

code:

import html
import json
import pprint
import random

import requests

endgame=""
correct=0
wrong=0
url="https://opentdb.com/api.php?amount=1&category=18&difficulty=easy&type=multiple"
r=requests.get(url)
while endgame!="quit":
    if r.status_code!=200:
        input("sorry,we are unable to process the question.please click enter to continue or type 'quit'")
    else:
        data=json.loads(r.text)
        question=data["results"][0]["question"]
        answers=data["results"][0]["incorrect_answers"]
        correct_answer=data["results"][0]["correct_answer"]
        answers.append(correct_answer)
        random.shuffle(answers)
        print(html.unescape(question))
        k=1
        for i in answers:
            print(str(k)+"-"+i)
            k += 1
        ans=int(input("enter your choice: "))
        if(ans>0 and ans<5):
            if(answers[ans-1]==correct_answer):
                correct += 1
                print("congratulations!your answer is correct")
            else:
                wrong += 1
                print("sorry!Your answer is wrng.the correct answer is "+correct_answer)
            score=correct*4-wrong
            print("score: ")
            print(score)
            print("correct answers: ")
            print(correct)
            print("wrong answers: ")
            print(wrong)
        else:
            print("invalid input")
            print("click enter to continue or type 'quit' to stop playing")
        endgame=input("click on enter to continue or type 'quit' to quit the game").lower()
        r=requests.get(url)
else:
    print("thank you for playing the game")
