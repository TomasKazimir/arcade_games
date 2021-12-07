import turtle
from typing import Tuple


class Renderer(turtle.Turtle):
    def __init__(self, pensize: int, screen_size: Tuple[int], speed: Tuple[int]) -> None:
        turtle.Turtle.__init__(self)

        self.screen = turtle.Screen()
        self.screen.setup(*[size + 50 for size in screen_size])
        self.screen.title('Renderer')

        self.pensize(pensize)

        self.color('black', 'black')

        self.screen.tracer(*speed)

        self.penup()

        self.hideturtle()

    def draw_reg_pol(self, length: float, sides: int, color=['black', 'black']):
        self.color(*color)
        self.begin_fill()
        self.pendown()
        for _ in range(sides):
            self.forward(length)
            self.right(360/sides)
        self.end_fill()
        self.penup()

    def draw_shape(self, vertices: Tuple[tuple], color=['black', 'black']):
        """
        Draw a shape defined by vertices, relative to current position.

        Example:
        r1.draw_shape(((0, 0), (5, 0), (2.5, 3.5)))
            3.5 ......#......
                ....#####....
                ..#########..
            0   X############
                0    2.5    5
            Where X is the staring position
        """

        x, y = self.pos()

        self.goto(vertices[0][0] + x, vertices[0][1] + y)
        self.pendown()
        self.color(*color)
        self.begin_fill()
        for vertex in vertices:
            self.goto(vertex[0] + x, vertex[1] + y)
        self.goto(vertices[0][0] + x, vertices[0][1] + y)
        self.end_fill()
        self.penup()
        self.goto(x, y)

    def write_text(self, text, color='black', align='center', font_config=('Courier', 50, 'bold')):
        self.color(color)
        self.write(text, False, align, font_config)

    def render_frame(self):
        self.screen.update()


if __name__ == '__main__':
    r1 = Renderer(1, (600, 400), (1, 0))
    # r1.draw_reg_pol(10, 10)
    # r1.draw_shape(((50, 0), (50, 10), (40, 0)))
    r1.goto(0, 0)
    r1.pendown()
    r1.forward(100)
    r1.render_frame()
    input()
