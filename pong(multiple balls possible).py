from drawing import Renderer

from typing import List
from math import sin, cos, radians, sqrt

import random
import keyboard
import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

BAT_OFFSET = SCREEN_WIDTH // 15
BAT_WIDTH = 6
BAT_HEIGHT = 150
BAT_SPEED = 15

BALL_SPEED = 15
BALL_SIZE = 15

COLLISION_FIX = BALL_SPEED - BAT_WIDTH if BALL_SPEED - BAT_WIDTH >= 0 else 0


class Game_Pong:
    def __init__(self, player_names: List[str], ball_speed: float, ball_size: int) -> None:
        self.player1 = Player(player_names[0])
        self.player2 = Player(player_names[1])

        self.bat_setup()

        self.balls = \
            [Ball(ball_speed, ball_size, random.randint(-60, 60) % 360)
             for _ in range(1)] + \
            [Ball(ball_speed, ball_size, random.randint(120, 240) % 360)
             for _ in range(0)]

        self.renderer = Renderer(1, (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0))

    def bat_setup(self):
        self.bat1 = Bat(BAT_WIDTH, BAT_HEIGHT, BAT_SPEED)
        self.bat1.xpos = BAT_OFFSET
        self.bat1.ypos = SCREEN_HEIGHT / 2 + BAT_HEIGHT / 2
        self.bat2 = Bat(BAT_WIDTH, BAT_HEIGHT, BAT_SPEED)
        self.bat2.xpos = SCREEN_WIDTH - BAT_OFFSET - BAT_WIDTH
        self.bat2.ypos = SCREEN_HEIGHT / 2 + BAT_HEIGHT / 2

    def simulate_tick(self):
        # move bats
        if keyboard.is_pressed('w'):
            self.bat1.move_up()
        if keyboard.is_pressed('s'):
            self.bat1.move_down()

        if keyboard.is_pressed('up'):
            self.bat2.move_up()
        if keyboard.is_pressed('down'):
            self.bat2.move_down()

    # ball movement
        for ball in self.balls:
            ball.direction %= 360
            # top edge
            if ball.ypos >= SCREEN_HEIGHT and ball.direction < 180:
                ball.direction = -ball.direction
            # bottom edge
            elif ball.ypos - ball.size <= 0 and 180 < ball.direction:
                ball.direction = -ball.direction
            # right bat - bat2
            elif self.bat2.xpos - ball.size <= ball.xpos <= self.bat2.xpos + self.bat2.width + COLLISION_FIX \
                    and self.bat2.ypos + ball.size >= ball.ypos >= self.bat2.ypos - self.bat2.height:
                if not ball.in_collision:
                    ball.direction = 0*(180 - ball.direction) + 180 - \
                        5 * my_sqrt(
                            ball.ypos - ball.size / 2 - (self.bat2.ypos-self.bat2.height / 2))
                    ball.in_collision = True
            # left bat - bat1
            elif self.bat1.xpos - COLLISION_FIX <= ball.xpos <= self.bat1.xpos + self.bat1.width \
                    and self.bat1.ypos + ball.size >= ball.ypos >= self.bat1.ypos - self.bat1.height:
                if not ball.in_collision:
                    ball.direction = 0*(180 - ball.direction) + \
                        5 * my_sqrt(
                            ball.ypos - ball.size / 2 - (self.bat1.ypos-self.bat1.height / 2))
                    ball.in_collision = True
            # right edge - player1 win
            elif SCREEN_WIDTH - ball.size <= ball.xpos:
                self.player1.score += 1
                self.balls.remove(ball)
                if len(self.balls) == 0:
                    self.balls.append(
                        Ball(ball.speed, ball.size, random.randint(-10, 10) % 360))
                    self.bat_setup()
                    time.sleep(0.5)
                # ball.direction = 180 - ball.direction
            # left edge - player2 win
            elif 0 > ball.xpos:
                self.player2.score += 1
                self.balls.remove(ball)
                if len(self.balls) == 0:
                    self.balls.append(
                        Ball(ball.speed, ball.size, random.randint(170, 190) % 360))
                    self.bat_setup()
                    time.sleep(0.5)
                # ball.direction = 180 - ball.direction
            else:
                ball.in_collision = False

            ball.direction %= 360
            ball.xpos += ball.speed * cos(radians(ball.direction))
            ball.ypos += ball.speed * sin(radians(ball.direction))

    def render_scene(self):
        self.renderer.clear()
        x, y = -SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2
        # drawing a gray background
        self.renderer.goto(x, y + SCREEN_HEIGHT)
        self.renderer.draw_shape(
            ((0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, - SCREEN_HEIGHT), (0, -SCREEN_HEIGHT)), ['gray70', 'gray70'])

        # drawing the ball
        for ball in self.balls:
            self.renderer.goto(x + ball.xpos, y + ball.ypos)
            self.renderer.draw_reg_pol(ball.size, 4)

        # drawing the bats
        # bat 1
        self.renderer.goto(x + self.bat1.xpos, y + self.bat1.ypos)
        self.renderer.draw_shape(
            ((0, 0), (self.bat1.width, 0), (self.bat1.width, - self.bat1.height), (0, - self.bat1.height)))
        # bat 2
        self.renderer.goto(x + self.bat2.xpos, y + self.bat2.ypos)
        self.renderer.draw_shape(
            ((0, 0), (self.bat2.width, 0), (self.bat2.width, - self.bat2.height), (0, - self.bat2.height)))

        # drawing player scores
        # player1 - left
        self.renderer.goto(x + 4*BAT_OFFSET, y + SCREEN_HEIGHT - 100)
        self.renderer.write_text(self.player1.score)
        # player2 - right
        self.renderer.goto(x + SCREEN_WIDTH - 4*BAT_OFFSET,
                           y + SCREEN_HEIGHT - 100)
        self.renderer.write_text(self.player2.score)

        self.renderer.render_frame()


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.score = 0


class Ball:
    def __init__(self, speed: float, size: int, direction: float = 30) -> None:
        self.xpos = SCREEN_WIDTH / 2
        self.ypos = SCREEN_HEIGHT / 2
        self.direction = direction
        self.speed = speed
        self.size = size

        self.in_collision = False


class Bat:
    def __init__(self, width: int, height: int, speed: float) -> None:
        self.xpos = 0
        self.ypos = 0
        self.width = width
        self.height = height
        self.speed = speed

    def move_up(self):
        if self.ypos + self.speed <= SCREEN_HEIGHT:
            self.ypos += self.speed
        else:
            self.ypos = SCREEN_HEIGHT

    def move_down(self):
        if self.ypos - self.height - self.speed >= 0:
            self.ypos -= self.speed
        else:
            self.ypos = 0 + self.height


def my_sqrt(x):
    try:
        if x < 0:
            return -sqrt(-x)
        else:
            return sqrt(x)
    except ValueError:
        return 0


if __name__ == '__main__':
    game = Game_Pong(['P1', 'P2'], BALL_SPEED, BALL_SIZE)

    while True:
        game.simulate_tick()
        game.simulate_tick()
        game.render_scene()
        time.sleep(1/60)
