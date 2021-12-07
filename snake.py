from typing import Tuple
from drawing import Renderer
from random import randint

import time
import keyboard


class Game_Snake:
    def __init__(self, screensize: Tuple[int, int], gridsize: Tuple[int, int], starting_length: int = 5, starting_food: int = 1) -> None:
        self.renderer = Renderer(1, screensize, (0, 0))
        self.gridsize = gridsize
        self.screensize = screensize
        self.starting_length = starting_length
        self.starting_food = starting_food
        self.body = [(gridsize[0]//2, gridsize[1]//2)
                     for _ in range(starting_length)]
        self.direction = 'right'
        self.food = []
        for _ in range(starting_food):
            self.food += [self.new_food()]
        self.ate_food = 0

    @property
    def snake_length(self):
        return len(self.body)

    def set_direction(self, diretion):
        self.direction = diretion

    def new_food(self):
        food = [randint(0, self.gridsize[0]-1), randint(0, self.gridsize[1]-1)]
        for x in range(self.gridsize[0]):
            for y in range(self.gridsize[1]):
                if tuple(food) in self.body or tuple(food) in self.food:
                    food[1] = (food[1] + 1) % self.gridsize[1]
                else:
                    break
            if tuple(food) in self.body or tuple(food) in self.food:
                food[0] = (food[0] + 1) % self.gridsize[0]
            else:
                break
        else:
            # TODO: Victory
            self.render_scene()
            time.sleep(2)
            self.body = [(self.gridsize[0]//2, self.gridsize[1]//2)
                         for _ in range(self.starting_length)]
            self.direction = 'right'
            self.ate_food = 0
            self.food = []
            for _ in range(self.starting_food):
                self.food += [self.new_food()]
        return tuple(food)

    def simulate_tick(self):
        # player input

        # adding new body segment
        match self.direction:
            case 'right':
                x, y = 1, 0
            case 'left':
                x, y = -1, 0
            case 'up':
                x, y = 0, 1
            case 'down':
                x, y = 0, -1
            case _:
                raise ValueError(self.direction,
                                 ' - must be right, left, up, or down')
        new_segment = Segment(
            self.body[-1][0] + x,
            self.body[-1][1] + y
        )
        # deleting last body segment if no food was eaten
        if not self.ate_food > 0:
            self.body.pop(0)
        else:
            self.ate_food -= 1
        # snake wrapping around the grid
        new_segment.x %= self.gridsize[0]
        new_segment.y %= self.gridsize[1]

        self.body.append(new_segment.pos)

        # collision detection
        if new_segment.pos in self.body[:-1]:
            self.render_scene()
            time.sleep(2)
            self.body = [(self.gridsize[0]//2, self.gridsize[1]//2)
                         for _ in range(5)]
            self.direction = 'right'
            self.ate_food = 0
            self.food = []
            for _ in range(self.starting_food):
                self.food += [self.new_food()]

        if new_segment.pos in self.food:
            self.food.remove(new_segment.pos)
            self.ate_food += 1

            self.food.append(self.new_food())

        # add food
        if self.food == []:
            self.food.append(self.new_food())

    def render_scene(self):
        self.renderer.clear()
        x, y = -self.screensize[0] / 2, -self.screensize[1] / 2
        seg_width = self.screensize[0] / self.gridsize[0]
        seg_height = self.screensize[1] / self.gridsize[1]
        xgap = seg_width * 0.93
        ygap = seg_height * 0.93
        # drawing a gray background
        self.renderer.goto(x, y + self.screensize[1])
        self.renderer.draw_shape(
            ((0, 0), (self.screensize[0], 0), (self.screensize[0], - self.screensize[1]), (0, -self.screensize[1])), ['gray70', 'gray70'])

        # drawing the snake
        for segment in self.body:
            self.renderer.goto(
                x + seg_width * segment[0],
                y + seg_height * segment[1])
            self.renderer.draw_shape(
                ((0 + xgap, 0 + ygap), (0 + xgap, seg_height - ygap),
                 (seg_width - xgap, seg_height - ygap), (seg_width - xgap, 0 + ygap)))
        # coloring the head
        head = self.body[-1]
        self.renderer.goto(
            x + seg_width * head[0],
            y + seg_height * head[1])
        self.renderer.draw_shape(
            vertices=((0 + xgap, 0 + ygap), (0 + xgap, seg_height - ygap),
                      (seg_width - xgap, seg_height - ygap), (seg_width - xgap, 0 + ygap)),
            color=['dark green', 'dark green'])

        # drawing the food
        xgap = seg_width * 0.8
        ygap = seg_height * 0.8
        for food in self.food:
            self.renderer.goto(
                x + seg_width * food[0],
                y + seg_height * food[1])
            self.renderer.draw_shape(
                ((0 + xgap, 0 + ygap), (0 + xgap, seg_height - ygap),
                 (seg_width - xgap, seg_height - ygap), (seg_width - xgap, 0 + ygap)),
                color=['red', 'red'])

        # length display
        self.renderer.goto(0, -y - 60)
        self.renderer.write_text(
            self.snake_length, font_config=('System', 40, 'bold'), color='gray30')

        self.renderer.screen.bgcolor('black')
        self.renderer.render_frame()


class Segment:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @ property
    def pos(self):
        return self.x, self.y

    def __repr__(self) -> str:
        return f'<X:{self.x}, Y:{self.y}>'


if __name__ == '__main__':

    SCREEN_SIZE = 1600, 900
    K = 5
    GRID_SIZE = 16*K, 9*K

    game = Game_Snake(SCREEN_SIZE, GRID_SIZE,
                      starting_length=5, starting_food=10)

    # w,s,a,d keypress events
    keyboard.add_hotkey('w', lambda: game.set_direction('up'))
    keyboard.add_hotkey('s', lambda: game.set_direction('down'))
    keyboard.add_hotkey('a', lambda: game.set_direction('left'))
    keyboard.add_hotkey('d', lambda: game.set_direction('right'))
    # arrows keypress events
    keyboard.add_hotkey('up', lambda: game.set_direction('up'))
    keyboard.add_hotkey('down', lambda: game.set_direction('down'))
    keyboard.add_hotkey('left', lambda: game.set_direction('left'))
    keyboard.add_hotkey('right', lambda: game.set_direction('right'))

    while True:
        game.simulate_tick()
        game.render_scene()
        time.sleep(1/10)
