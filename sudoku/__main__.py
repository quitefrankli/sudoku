import pygame
import click

from typing import *

from sudoku.config import *
from sudoku.board import Board


def find_solvable_board() -> Board:
    for i in range(50):
        print(f"searching for easy board attempt {i}")
        board = Board()
        algo = board.algo1()
        try:
            for _ in range(MAX_STEPS_SOLVABLE):
                if next(algo):
                    board.reset()
                    return board
        except StopIteration:
            print("here")
            pass

    raise RuntimeError("No suitable board found")

@click.command()
@click.option("--difficulty", default=3)
def main(difficulty: int) -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    board = find_solvable_board()
    backtracking_algo = board.algo1()

    running = True
    stop_algo = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            running = False
            
        board.draw(screen)
        if not stop_algo:
            for _ in range(ALGO_ITER_PER_FRAME):
                stop_algo = next(backtracking_algo)
                if stop_algo:
                    break

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()