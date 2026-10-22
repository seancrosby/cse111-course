"""
CSE 111
Lesson 6 Practice 2 - Debugging a Pong game

This program is a small single-player Pong game. Use the left and right
arrow keys to move the paddle and keep the ball from reaching the bottom
of the screen.
"""

import tkinter as tk


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 14
PADDLE_Y_OFFSET = 28
BALL_SIZE = 16
PADDLE_STEP = 24
START_SPEED = 2.5
SPEEDUP_RATE = 0.25
MAX_SPEED = 10.0


def move_paddle(paddle_x, amount, screen_width=SCREEN_WIDTH,
                paddle_width=PADDLE_WIDTH):
    """Return a paddle position that remains inside the screen."""
    new_x = paddle_x + amount
    return max(0, min(screen_width - paddle_width, new_x))


def next_score(score):
    """Return the score after the player earns one point."""
    return (score + 1) % 10


def ball_hits_paddle(ball_x, ball_y, paddle_x, paddle_y,
                     ball_size=BALL_SIZE, paddle_width=PADDLE_WIDTH,
                     paddle_height=PADDLE_HEIGHT):
    """Return True when the ball overlaps the paddle."""
    overlaps_horizontally = (
        ball_x + ball_size >= paddle_x
        and ball_x <= paddle_x + paddle_width / 2
    )
    overlaps_vertically = (
        ball_y + ball_size >= paddle_y
        and ball_y <= paddle_y + paddle_height
    )
    return overlaps_horizontally and overlaps_vertically


def hits_right_wall(ball_x, ball_size=BALL_SIZE,
                    screen_width=SCREEN_WIDTH):
    """Return True when the ball reaches the right edge of the screen."""
    return ball_x + ball_size >= screen_width


def update_speed(current_speed, paddle_hit, speedup_rate=SPEEDUP_RATE,
                 max_speed=MAX_SPEED):
    """Return the speed after one game update."""
    current_speed += speedup_rate
    if current_speed > max_speed:
        current_speed = max_speed
    return current_speed


def reset_round_speed(current_speed):
    """Return the speed that a new round should use."""
    return current_speed


root = None
canvas = None
paddle_x = 0
paddle_y = 0
ball_x = 0
ball_y = 0
ball_dx = 1
ball_dy = 1
score = 0
speed = START_SPEED
running = False
left_pressed = False
right_pressed = False
score_id = None
paddle_id = None
ball_id = None
prompt_id = None


def move_left(event=None):
    """Move the paddle left."""
    global paddle_x
    paddle_x = move_paddle(paddle_x, -PADDLE_STEP)


def move_right(event=None):
    """Move the paddle right."""
    global paddle_x
    paddle_x = move_paddle(paddle_x, PADDLE_STEP)


def press_left(event=None):
    """Remember that the left arrow key is being held."""
    global left_pressed
    left_pressed = True


def release_left(event=None):
    """Remember that the left arrow key was released."""
    global left_pressed
    left_pressed = False


def press_right(event=None):
    """Remember that the right arrow key is being held."""
    global right_pressed
    right_pressed = True


def release_right(event=None):
    """Remember that the right arrow key was released."""
    global right_pressed
    right_pressed = False


def reset_ball():
    """Place the ball back in the middle after it reaches the bottom."""
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = SCREEN_WIDTH / 2
    ball_y = SCREEN_HEIGHT / 2
    ball_dx = -1
    ball_dy = -1


def start_round(event=None):
    """Start a round when the player presses Space or clicks."""
    global running, speed
    if running:
        return
    running = True
    speed = reset_round_speed(speed)
    reset_ball()
    canvas.itemconfigure(prompt_id, state="hidden")
    update()


def setup_game(window):
    """Create the game canvas, shapes, and event bindings."""
    global root, canvas, paddle_x, paddle_y, ball_x, ball_y
    global score, score_id, paddle_id, ball_id, prompt_id

    root = window
    canvas = tk.Canvas(
        root,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        background="black"
    )
    canvas.pack()

    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) / 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET
    ball_x = SCREEN_WIDTH / 2
    ball_y = SCREEN_HEIGHT / 2
    score = 0

    canvas.create_text(
        SCREEN_WIDTH / 2,
        24,
        text="PONG",
        fill="white",
        font=("TkDefaultFont", 18, "bold")
    )
    score_id = canvas.create_text(
        SCREEN_WIDTH / 2,
        52,
        text="Score: 0",
        fill="white",
        font=("TkDefaultFont", 14)
    )
    paddle_id = canvas.create_rectangle(
        paddle_x,
        paddle_y,
        paddle_x + PADDLE_WIDTH,
        paddle_y + PADDLE_HEIGHT,
        fill="white",
        outline=""
    )
    ball_id = canvas.create_oval(
        ball_x,
        ball_y,
        ball_x + BALL_SIZE,
        ball_y + BALL_SIZE,
        fill="white",
        outline=""
    )
    prompt_id = canvas.create_text(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2 - 40,
        text="Press Space or click to start",
        fill="white",
        font=("TkDefaultFont", 16)
    )

    root.bind("<KeyPress-Left>", press_left)
    root.bind("<KeyRelease-Left>", release_left)
    root.bind("<KeyPress-Right>", press_right)
    root.bind("<KeyRelease-Right>", release_right)
    root.bind("<space>", start_round)
    root.bind("<Button-1>", start_round)


def update():
    """Advance the game by one frame and schedule the next frame."""
    global ball_x, ball_y, ball_dx, ball_dy, score, speed, running

    if not running:
        return

    if left_pressed and not right_pressed:
        move_left()
    elif right_pressed and not left_pressed:
        move_right()

    paddle_hit = False
    ball_x += ball_dx * speed
    ball_y += ball_dy * speed

    if ball_x <= 0:
        ball_x = 0
        ball_dx = abs(ball_dx)
    elif hits_right_wall(ball_x):
        ball_x = SCREEN_WIDTH - BALL_SIZE
        ball_dx = -abs(ball_dx)

    if ball_y <= 0:
        ball_y = 0
        ball_dy = abs(ball_dy)
    elif (
            ball_dy > 0
            and ball_hits_paddle(
                ball_x,
                ball_y,
                paddle_x,
                paddle_y
            )
    ):
        ball_y = paddle_y - BALL_SIZE
        ball_dy = -abs(ball_dy)
        score = next_score(score)
        paddle_hit = True
    elif ball_y > SCREEN_HEIGHT:
        running = False
        reset_ball()
        canvas.itemconfigure(prompt_id, state="normal")

    speed = update_speed(speed, paddle_hit)

    canvas.coords(
        paddle_id,
        paddle_x,
        paddle_y,
        paddle_x + PADDLE_WIDTH,
        paddle_y + PADDLE_HEIGHT
    )
    canvas.coords(
        ball_id,
        ball_x,
        ball_y,
        ball_x + BALL_SIZE,
        ball_y + BALL_SIZE
    )
    canvas.itemconfigure(score_id, text=f"Score: {score}")
    if running:
        root.after(16, update)


def main():
    """Create the game window and start the Tkinter event loop."""
    window = tk.Tk()
    window.title("Pong")
    setup_game(window)
    window.mainloop()


if __name__ == "__main__":
    main()
