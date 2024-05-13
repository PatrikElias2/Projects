from turtle import Turtle, Screen
import time
import random


# Variables
score = 0
best_score = 0

screen = Screen()
screen.bgcolor("green")
screen.title("Welcome to the Snake game")
screen.setup(width=600, height=600)
screen.tracer(False)

# Snake´s head
head = Turtle("square")
head.color("black")
head.speed(0)
head.penup()
head.goto(0,0)
head.direction = "stop"


# Apple
apple = Turtle("circle")
apple.color("red")
apple.penup()
apple.goto(100, 100)


# Body
body_parts = []

# Score
score_sign = Turtle("square")
score_sign.speed(0)
score_sign.color("white")
score_sign.penup()
score_sign.hideturtle()
score_sign.goto(0, 265)
score_sign.write("Score: 0   Best score: 0", align="center", font=("Arial", 18))


# Functions
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


def move_up():
    if head.direction != "down":
        head.direction = "up"

def move_down():
    if head.direction != "up":
        head.direction = "down"

def move_left():
    if head.direction != "right":
        head.direction = "left"

def move_right():
    if head.direction != "left":
        head.direction = "right"


# Click on keys
screen.listen()
screen.onkeypress(move_up, "w")
screen.onkeypress(move_down, "s")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")


# Main cycle
while True:
    screen.update()
    
    # Collision with canvas
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(2)
        head.goto(0, 0)
        head.direction = "stop"
        
        # Hidding body parts
        for one_body_part in body_parts:
            one_body_part.goto(2000, 2000)

        # Emptying list with body parts (grey squares)
        body_parts.clear()

        # Reseting score
        score = 0
        score_sign.clear()
        score_sign.write(f"Score: {score}   Best score: {best_score}", align="center", font=("Arial", 18))


    # Generating food and checking collision with head
    if head.distance(apple) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        apple.goto(x, y)

        # Add new body parts
        new_body_part = Turtle("square")
        new_body_part.speed(0)
        new_body_part.color("grey")
        new_body_part.penup()
        body_parts.append(new_body_part)

        # Increasing score
        score += 10

        if score > best_score:
            best_score = score

        score_sign.clear()
        score_sign.write(f"Score: {score}   Best score: {best_score}", align="center", font=("Arial", 18))


    # adding first body part
    if len(body_parts) > 0:
        x = head.xcor()
        y = head.ycor()
        body_parts[0].goto(x,y)

    # adding other body parts
    for index in range(len(body_parts) - 1, 0, -1):
        x = body_parts[index - 1].xcor()
        y = body_parts[index - 1].ycor()
        body_parts[index].goto(x,y)

    move()

    # Collision with body
    for one_body_part in body_parts:
        if one_body_part.distance(head) < 20:
            time.sleep(2)
            head.goto(0, 0)
            head.direction = "stop"
        
            # Hidding body parts
            for one_body_part in body_parts:
                one_body_part.goto(2000, 2000)

            # Emptying list with body parts (grey squares)
            body_parts.clear()

            # Reseting score
            score = 0
            score_sign.clear()
            score_sign.write(f"Score: {score}   Best score: {best_score}", align="center", font=("Arial", 18))
            
    time.sleep(0.1)
    



screen.exitonclick()