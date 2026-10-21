"""
CSE 111
Lesson 6 Practice 2 - Debugging a Pong game
Author: [Your Name Here]

This program is a small single-player Pong game. Use the left and right
arrow keys to move the paddle and keep the ball from reaching the bottom
of the screen.
"""

import time
import tkinter as tk


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 14
PADDLE_Y_OFFSET = 28
BALL_SIZE = 16
PADDLE_STEP = 24
START_SPEED = 4.0
SPEEDUP_RATE = 0.25
MAX_SPEED = 10.0
BOTTOM_WALL_BUG_HITS = 5


def move_paddle(paddle_x, amount, screen_width=SCREEN_WIDTH,
                paddle_width=PADDLE_WIDTH):
    """Return a paddle position that remains inside the screen."""
    new_x = paddle_x + amount
    return max(0, min(screen_width - paddle_width, new_x))


def next_score(score):
    """Return the score after the player earns one point."""
    return (score + 1) % 100


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
    return ball_x + ball_size >= screen_width - 2


def ball_speed(elapsed_seconds, base_speed=START_SPEED,
               speedup_rate=SPEEDUP_RATE, max_speed=MAX_SPEED):
    """Return the ball speed based on how long the game has run."""
    speed = base_speed + elapsed_seconds * speedup_rate
    return min(speed, max_speed)


def bottom_wall_deflects(paddle_hits):
    """Return whether the bottom wall incorrectly deflects the ball."""
    return paddle_hits >= BOTTOM_WALL_BUG_HITS


class PongGame:
    """A small Tkinter window containing a single-player Pong game."""

    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(
            root,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            background="black"
        )
        self.canvas.pack()

        self.paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) / 2
        self.paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET
        self.ball_x = SCREEN_WIDTH / 2
        self.ball_y = SCREEN_HEIGHT / 2
        self.ball_dx = 1
        self.ball_dy = 1
        self.score = 0
        self.paddle_hits = 0
        self.started_at = time.monotonic()
        self.running = False

        self.canvas.create_text(
            SCREEN_WIDTH / 2,
            24,
            text="PONG",
            fill="white",
            font=("TkDefaultFont", 18, "bold")
        )
        self.score_id = self.canvas.create_text(
            SCREEN_WIDTH / 2,
            52,
            text="Score: 0",
            fill="white",
            font=("TkDefaultFont", 14)
        )
        self.paddle_id = self.canvas.create_rectangle(
            self.paddle_x,
            self.paddle_y,
            self.paddle_x + PADDLE_WIDTH,
            self.paddle_y + PADDLE_HEIGHT,
            fill="white",
            outline=""
        )
        self.ball_id = self.canvas.create_oval(
            self.ball_x,
            self.ball_y,
            self.ball_x + BALL_SIZE,
            self.ball_y + BALL_SIZE,
            fill="white",
            outline=""
        )
        self.prompt_id = self.canvas.create_text(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            text="Press Space or click to start",
            fill="white",
            font=("TkDefaultFont", 16)
        )

        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        root.bind("<space>", self.start_round)
        root.bind("<Button-1>", self.start_round)

    def move_left(self, event=None):
        """Move the paddle left."""
        self.paddle_x = move_paddle(self.paddle_x, -PADDLE_STEP)

    def move_right(self, event=None):
        """Move the paddle right."""
        self.paddle_x = move_paddle(self.paddle_x, PADDLE_STEP)

    def reset_ball(self):
        """Place the ball back in the middle after it reaches the bottom."""
        self.ball_x = SCREEN_WIDTH / 2
        self.ball_y = SCREEN_HEIGHT / 2
        self.ball_dx = -1
        self.ball_dy = -1

    def start_round(self, event=None):
        """Start a round when the player presses Space or clicks."""
        if self.running:
            return
        self.running = True
        self.started_at = time.monotonic()
        self.paddle_hits = 0
        self.reset_ball()
        self.canvas.itemconfigure(self.prompt_id, state="hidden")
        self.update()

    def update(self):
        """Advance the game by one frame and schedule the next frame."""
        if not self.running:
            return

        elapsed = time.monotonic() - self.started_at
        speed = ball_speed(elapsed)
        self.ball_x += self.ball_dx * speed
        self.ball_y += self.ball_dy * speed

        if self.ball_x <= 0:
            self.ball_x = 0
            self.ball_dx = abs(self.ball_dx)
        elif hits_right_wall(self.ball_x):
            self.ball_x = SCREEN_WIDTH - BALL_SIZE
            self.ball_dx = -abs(self.ball_dx)

        if self.ball_y <= 0:
            self.ball_y = 0
            self.ball_dy = abs(self.ball_dy)
        elif (
                self.ball_dy > 0
                and ball_hits_paddle(
                    self.ball_x,
                    self.ball_y,
                    self.paddle_x,
                    self.paddle_y
                )
        ):
            self.ball_y = self.paddle_y - BALL_SIZE
            self.ball_dy = -abs(self.ball_dy)
            self.score = next_score(self.score)
            self.paddle_hits += 1
        elif self.ball_y > SCREEN_HEIGHT:
            if bottom_wall_deflects(self.paddle_hits):
                self.ball_y = SCREEN_HEIGHT - BALL_SIZE
                self.ball_dy = -abs(self.ball_dy)
            else:
                self.running = False
                self.reset_ball()
                self.canvas.itemconfigure(self.prompt_id, state="normal")

        self.canvas.coords(
            self.paddle_id,
            self.paddle_x,
            self.paddle_y,
            self.paddle_x + PADDLE_WIDTH,
            self.paddle_y + PADDLE_HEIGHT
        )
        self.canvas.coords(
            self.ball_id,
            self.ball_x,
            self.ball_y,
            self.ball_x + BALL_SIZE,
            self.ball_y + BALL_SIZE
        )
        self.canvas.itemconfigure(self.score_id, text=f"Score: {self.score}")
        if self.running:
            self.root.after(16, self.update)


def main():
    """Create the game window and start the Tkinter event loop."""
    root = tk.Tk()
    root.title("Pong")
    PongGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
