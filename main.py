import pygame
import pymunk
import pymunk.pygame_util
import numpy as np
from pygame import time
import keyboard

import constants as const
import space_setup

pygame.init()
# setting up window parameters
WIN = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption(const.WINDOW_NAME)


def main():
    """main event loop"""
    # setting the clock in order to run the simulation
    # with constant FPS
    clock = pygame.time.Clock()
    run = True
    # one delta-time that we use to make one step
    # every 1/60 of a second
    dt = 1 / const.FPS

    # setting the space to run physics in
    space = pymunk.Space()
    # setting all the options for the space
    space.gravity = (0, 981)
    space_setup.create_boundaries(space, const.WIDTH, const.HEIGHT)
    space_setup.draw_obstacles(space, const.WIDTH, const.HEIGHT)
    space_setup.draw_bins(space, const.WIDTH, const.HEIGHT, 21)  # making 21 bins for now

    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    create_ball = pygame.USEREVENT + 1
        # main event loop
    while run:
        clock.tick(const.FPS)
        for event in pygame.event.get():
            # if user closes the window, we break the main loop
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == create_ball:
                ball = space_setup.Ball(const.BALL_RADIUS, const.BALL_MASS,
                                        const.BALL_ELASTICITY,
                                        const.BALL_FRICTION)
                ball.add(space)
            # if user clicks a mouse button, we drop 100 balls, each after 250 milliseconds
            elif event.type == pygame.MOUSEBUTTONDOWN:
                time.set_timer(pygame.event.Event(create_ball), 250, 100)




        space_setup.draw_window(space, WIN, draw_options)
        space.step(dt)

    pygame.quit()


if __name__ == '__main__':
    main()
