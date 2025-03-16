from typing import *
from sudoku.config import *
from pygame import Rect, Color

import random
import pygame


class Board:
    def __init__(self, fill_count: int = FILL_COUNT):
        self.cells: List[List[int]] = [[0] * N for _ in range(N)]
        # for fast validation
        self.rows = [[False] * N for _ in range(N)]
        self.cols = [[False] * N for _ in range(N)]
        self.boxs = [[False] * N for _ in range(N)]
        self.init_coords: Tuple[int, int] = set()

        while fill_count:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.cells[row][col]:
                continue
            rnd = random.randint(1, 9)
            if not self.try_set(rnd, row, col):
                continue
            self.init_coords.add((row, col))
            fill_count-=1

    def _coord2box(r: int, c: int) -> int:
        return r//3*3 + c//3

    def try_set(self, v: int, r: int, c: int) -> bool:
        v -= 1 # for 0 based indexing

        if self.rows[r][v] or self.cols[c][v] or self.boxs[Board._coord2box(r, c)][v]:
            return False
        
        self.rows[r][v] = True
        self.cols[c][v] = True
        self.boxs[Board._coord2box(r, c)][v] = True
        self.cells[r][c] = v + 1

        return True
    
    def unset(self, v: int, r: int, c: int) -> None:
        v -= 1
        self.rows[r][v] = False
        self.cols[c][v] = False
        self.boxs[Board._coord2box(r, c)][v] = False
        self.cells[r][c] = 0
    
    def reset(self) -> None:
        self.rows = [[False] * N for _ in range(N)]
        self.cols = [[False] * N for _ in range(N)]
        self.boxs = [[False] * N for _ in range(N)]

        for r, row in enumerate(self.cells):
            for c, num in enumerate(row):
                if (r, c) in self.init_coords:
                   self.rows[r][num-1] = True
                   self.cols[c][num-1] = True
                   self.boxs[r//3*3+c//3][num-1] = True
                else:
                    row[c] = 0

    def is_solved(self) -> bool:
        return all([c != 0 for r in self.cells for c in r])

    def algo1(self, r: int = 0, c: int = 0):
        if r == N:
            yield True
            return
        
        r2, c2 = (r+1, 0) if c == N-1 else (r, c+1)


        if self.cells[r][c]:
            yield from self.algo1(r2, c2)
            return
        
        for i in range(1, N+1):
            if self.try_set(i, r, c):
                yield False
                yield from self.algo1(r2, c2)
                self.unset(i, r, c)
                yield False
        
        
    def draw(self, screen) -> None:
        def draw_cell(cell: int, row: int, col: int) -> None:
            cell = str(cell)
            font_color = Color(0, 0, 255) if (row, col) in self.init_coords else Color(0, 0, 0)
            font = pygame.font.Font(None, 100)
            surface = font.render(cell, True, font_color)
            rect = surface.get_rect()

            CW = WIDTH / N
            CH = HEIGHT / N

            rect.center = (col * CW + CW/2.0, row * CH + CH/2.0)
            
            bg_rect = Rect((CW*row, CH*col), (CW-PADDING, CH-PADDING))
            bg_rect.center = rect.center
            pygame.draw.rect(screen, Color(255, 255, 255), bg_rect)
            
            if cell != "0":
                screen.blit(surface, rect)

        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                draw_cell(cell, r, c)
