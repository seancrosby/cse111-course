"""Tests for the logic in pong_game.py."""

import pytest

from pong_game import (
    BALL_SIZE,
    MAX_SPEED,
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    ball_hits_paddle,
    hits_right_wall,
    move_paddle,
    next_score,
    reset_round_speed,
    update_speed,
)


def test_move_paddle_stays_inside_screen():
    assert move_paddle(10, -30) == 0
    assert move_paddle(500, 200) == 540


def test_next_score_increases_score():
    assert next_score(0) == 1
    assert next_score(8) == 9


def test_score_rolls_over_after_9():
    assert next_score(9) == 0


def test_ball_hits_left_side_of_paddle():
    paddle_y = 350
    assert ball_hits_paddle(
        100,
        paddle_y - BALL_SIZE + 1,
        100,
        paddle_y
    )


def test_ball_hits_right_side_of_paddle():
    paddle_x = 100
    paddle_y = 350
    ball_x = paddle_x + PADDLE_WIDTH - BALL_SIZE
    assert ball_hits_paddle(
        ball_x,
        paddle_y - BALL_SIZE + 1,
        paddle_x,
        paddle_y
    )


def test_ball_does_not_hit_paddle_when_it_is_above():
    assert not ball_hits_paddle(100, 300, 100, 350)


def test_ball_reaches_right_wall_at_screen_edge():
    screen_width = 640
    ball_x = screen_width - BALL_SIZE
    assert hits_right_wall(ball_x, BALL_SIZE, screen_width)


def test_ball_does_not_hit_right_wall_before_edge():
    screen_width = 640
    ball_x = screen_width - BALL_SIZE - 1
    assert not hits_right_wall(ball_x, BALL_SIZE, screen_width)


def test_ball_speed_increases_after_paddle_hit():
    assert update_speed(2.5, True) == pytest.approx(2.75)


def test_ball_speed_stops_at_maximum():
    assert update_speed(9.9, True) == pytest.approx(MAX_SPEED)


def test_speed_does_not_change_without_paddle_hit():
    assert update_speed(2.5, False) == pytest.approx(2.5)


def test_new_round_starts_at_starting_speed():
    assert reset_round_speed(8.0) == pytest.approx(2.5)


pytest.main(["-v", "--tb=line", "-rN", __file__])
