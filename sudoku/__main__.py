# Example file showing a basic pygame "game loop"
import pygame
import numpy as np
import click

from typing import *
from pygame import Color, Rect
from datetime import datetime

from sudoku.config import *
from sudoku.board import Board


@click.command()
@click.option("--difficulty", default=3)
def main(difficulty: int) -> None:
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = Board(screen)
    running = True
    
    backtracking_algo = board.algo1()
    stop_algo = False

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            running = False
            
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        board.draw()
        if not stop_algo:
            try:
                for i in range(ALGO_ITER_PER_FRAME):
                    stop_algo = next(backtracking_algo)
                    if stop_algo:
                        break
            except StopIteration:
                pass

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()