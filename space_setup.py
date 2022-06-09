import pygame
import pymunk
import pymunk.pygame_util
import numpy as np
import constants as const


def draw_window(space, window, draw_options):
    """ creates a window with white background"""
    window.fill(const.WHITE)
    space.debug_draw(draw_options)
    pygame.draw.line(start_pos=(const.WIDTH // 2, 0),
                     end_pos=(const.WIDTH // 2, const.HEIGHT),
                     color=const.RED,
                     surface=window)
    pygame.display.update()


def create_boundaries(space, width, height):
    """creates static 'walls' around the window borders"""
    # setting the positions and sizes of the rectangles used for borders
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)],
    ]

    # adding all four walls on the screen
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.1  # arbitrary values for elasticity
        shape.friction = 0.7  # and friction (making the simulation more realistic)
        space.add(body, shape)


def draw_obstacles(space, width, height):
    """creates the obstacles that make the ball change
    trajectory"""
    row_num = 1
    for i in range(50, width - 50, width // 45):
        for j in range(75, height - 225, height // 20):
            if row_num % 2 == 0 and j < width - 15:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (i, j + 15)
                shape = pymunk.Circle(body, radius=5)
                shape.mass = 10
                shape.color = (0, 0, 0, 100)
                shape.elasticity = 0.6
                shape.friction = 0.4
                space.add(body, shape)
            else:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (i, j)
                shape = pymunk.Circle(body, radius=5)
                shape.mass = 10
                shape.color = (0, 0, 0, 100)
                shape.elasticity = 0.6
                shape.friction = 0.4
                space.add(body, shape)
        row_num += 1


def draw_bins(space, width, height, n_bins=10):
    """creates bins in which the balls eventually fall"""
    for i in np.linspace(10, width - 10, n_bins):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (i, height - 70)
        shape = pymunk.Poly.create_box(body, (10, 250))
        shape.elasticity = 0.2
        shape.friction = 0.6
        space.add(body, shape)


class Ball:
    def __init__(self, radius, mass, elasticity, friction):
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.mass = mass
        self.shape.color = (255, 165, 0, 100)  # it's actually orange with 100% opacity
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.body.position = (const.WIDTH // 2, 10)

    def add(self, space):
        space.add(self.body, self.shape)
        return self.body
