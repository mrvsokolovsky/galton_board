import time

import pygame
import pymunk
import pymunk.pygame_util
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Galton Board')
FALL_SPEED = 5
BALL_RADIUS = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

FPS = 60


def draw_window(space, window, draw_options):
    window.fill(WHITE)
    space.debug_draw(draw_options)
    pygame.display.update()


def create_boundaries(space, width, height):
    rects = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.2
        shape.friction = 0.6
        space.add(body, shape)


def draw_obstacles(space, width, height):
    row_num = 1
    for i in range(50, width-50, 38):
        for j in range(75, height-250, 50):
            if row_num % 2 == 0 and j < width-15:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (i, j+15)
                shape = pymunk.Circle(body, radius=8)
                shape.mass = 10
                shape.color = (0, 0, 0, 100)
                shape.elasticity = 0.4
                shape.friction = 0.4
                space.add(body, shape)
            else:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (i, j)
                shape = pymunk.Circle(body, radius=8)
                shape.mass = 10
                shape.color = (0, 0, 0, 100)
                shape.elasticity = 0.9
                shape.friction = 0.4
                space.add(body, shape)
        row_num += 1


def draw_bins(space, width, height, n_bins=10):
    for i in np.linspace(10, width - 10, n_bins):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (i, height - 70)
        shape = pymunk.Poly.create_box(body, (10, 250))
        shape.elasticity = 0.2
        shape.friction = 0.6
        space.add(body, shape)

def draw_ball(space, radius=10, mass=10):
    body = pymunk.Body()
    body.position = (WIDTH // 2, 10)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 165, 0, 100)
    shape.elasticity = 0.9
    shape.friction = 0.4
    space.add(body, shape)

def main():
    clock = pygame.time.Clock()
    run = True
    dt = 1/FPS

    space = pymunk.Space()
    space.gravity = (0, 981)
    create_boundaries(space, WIDTH, HEIGHT)
    draw_obstacles(space, WIDTH, HEIGHT)
    draw_bins(space, WIDTH, HEIGHT, 21)

    draw_options = pymunk.pygame_util.DrawOptions(WIN)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw_ball(space)

        draw_window(space, WIN, draw_options)
        space.step(dt)


    pygame.quit()


if __name__ == '__main__':
    main()