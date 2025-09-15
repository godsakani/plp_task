#Here are some fun and beginner-friendly project ideas you can try at this stage:

#1. Personalized Greeting App 👋
#Create a program that asks for the user’s name and favorite color, then prints a personalized greeting like: “Hello, [Name]! Your favorite color, [Color], is awesome!”
name = input("What's your name? ")
color = input("What's your favorite color? ")
print(f"Hello, {name}! Your favorite color, {color}, is awesome!")
#2. Simple Quiz Game 🎮
#Create a multiple-choice quiz with questions about Python, movies, or any fun topic! Display scores at the end and allow the user to play again. 🏆
def quiz_game():
    questions = {
        "What is the capital of France?": "a",
        "What is 2 + 2?": "b",
        "What is the largest planet in our solar system?": "c"
    }
    options = [
        ["a) Paris", "b) London", "c) Berlin"],
        ["a) 3", "b) 4", "c) 5"],
        ["a) Earth", "b) Mars", "c) Jupiter"]
    ]
    
    score = 0
    for i, (question, answer) in enumerate(questions.items()):
        print(question)
        for option in options[i]:
            print(option)
        user_answer = input("Your answer: ")
        if user_answer.lower() == answer:
            score += 1
            print("Correct!")
        else:
            print("Wrong!")
    
    print(f"Your score: {score}/{len(questions)}")
#3. Random Joke Generator 🤣
#Build a program that stores a list of jokes and randomly selects one to display every time the user runs it. Add a fun twist with jokes about Python or programming! 🐍💡
import random   

def random_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why do Python programmers prefer snakes? Because they can’t handle the ‘byte’!",
        "What do you call a snake that works for the government? A civil serpent!"
    ]
    print(random.choice(jokes))