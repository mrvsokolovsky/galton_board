import time
import pygame
import pymunk
import pymunk.pygame_util
import numpy as np

pygame.init()
# setting constants (constants to be moved to a new file)
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
    """ creates a window with white background"""
    window.fill(WHITE)
    space.debug_draw(draw_options)
    pygame.display.update()


def create_boundaries(space, width, height):
    """creates static 'walls' around the window borders"""
    # setting the positions and sizes of the rectangles used for borders
    rects = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
    ]

    # adding all four walls on the screen
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.2 # arbitrary values for elasticity
        shape.friction = 0.6   # and friction (making the simulation more realistic)
        space.add(body, shape)


def draw_obstacles(space, width, height):
    """creates the obstacles that make the ball change
    trajectory"""
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
    """creates bins in which the balls eventually fall"""
    for i in np.linspace(10, width - 10, n_bins):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (i, height - 70)
        shape = pymunk.Poly.create_box(body, (10, 250))
        shape.elasticity = 0.2
        shape.friction = 0.6
        space.add(body, shape)


def draw_ball(space, radius=10, mass=10):
    """creates the ball"""
    body = pymunk.Body()
    body.position = (WIDTH // 2, 10) # positioning the ball in the middle on the screen
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 165, 0, 100)
    shape.elasticity = 0.9
    shape.friction = 0.4
    space.add(body, shape)


def main():
    """main event loop"""
    # setting the clock in order to run the simulation
    # with constant FPS
    clock = pygame.time.Clock()
    run = True
    # one delta-time that we use to make one step
    # every 1/60 of a second
    dt = 1/FPS

    #setting the space to run physics in
    space = pymunk.Space()
    #setting all of the options for the space
    space.gravity = (0, 981)
    create_boundaries(space, WIDTH, HEIGHT)
    draw_obstacles(space, WIDTH, HEIGHT)
    draw_bins(space, WIDTH, HEIGHT, 21) #making 21 bins for now

    draw_options = pymunk.pygame_util.DrawOptions(WIN)

    #main event loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # if user closes the window, we break the main loop
            if event.type == pygame.QUIT:
                run = False
                break
            # if user clicks a mousebutton, we drop one ball
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw_ball(space)

        draw_window(space, WIN, draw_options)
        space.step(dt)

    pygame.quit()


if __name__ == '__main__':
    main()