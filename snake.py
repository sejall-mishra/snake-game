import turtle
import time
import random
import os
import tkinter

# ---------- Settings ----------
LEVELS = {"Easy": 0.15, "Medium": 0.10, "Hard": 0.06}
level_name = "Medium"
delay = LEVELS[level_name]
paused = False

HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)


# ---------- High score file ----------
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE) as f:
                return int(f.read())
        except ValueError:
            return 0
    return 0


def save_high_score():
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(high_score))


score = 0
high_score = load_high_score()

# ---------- Screen ----------
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# ---------- Snake head ----------
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ---------- Food ----------
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# ---------- Score display ----------
pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, 260)

# ---------- Help text ----------
help_pen = turtle.Turtle()
help_pen.hideturtle()
help_pen.color("gray")
help_pen.penup()
help_pen.goto(0, -285)
help_pen.write("1 Easy   2 Medium   3 Hard   Space = Pause",
               align="center", font=("Courier", 10, "normal"))


def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High: {high_score}  Level: {level_name}",
              align="center", font=("Courier", 14, "normal"))


update_score()


# ---------- Direction functions ----------
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


# ---------- Difficulty and pause ----------
def set_level(name):
    global delay, level_name
    level_name = name
    delay = LEVELS[name]
    update_score()


def set_easy():
    set_level("Easy")


def set_medium():
    set_level("Medium")


def set_hard():
    set_level("Hard")


def toggle_pause():
    global paused
    paused = not paused


# ---------- Movement ----------
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)


# ---------- Reset after game over ----------
def reset_game():
    global score
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    update_score()


# ---------- Keyboard ----------
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(set_easy, "1")
screen.onkeypress(set_medium, "2")
screen.onkeypress(set_hard, "3")
screen.onkeypress(toggle_pause, "space")


# ---------- Game loop ----------
try:
    while True:
        screen.update()

        if paused:
            time.sleep(0.1)
            continue

        # Eating food
        if head.distance(food) < 20:
            x = random.randint(-280, 280)
            y = random.randint(-280, 280)
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.shape("square")
            new_segment.color("light green")
            new_segment.penup()
            new_segment.goto(1000, 1000)
            segments.append(new_segment)

            score += 10
            if score > high_score:
                high_score = score
                save_high_score()
            update_score()

        # Move the tail
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Wall collision
        if (head.xcor() > 290 or head.xcor() < -290
                or head.ycor() > 290 or head.ycor() < -290):
            reset_game()

        # Tail collision
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game()
                break

        time.sleep(delay)

except (turtle.Terminator, tkinter.TclError):
    pass