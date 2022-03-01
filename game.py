from snake import Snake
from snake import Coordinates
from map import Map
import time
import pygame


if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode((800, 800))
    mp = Map(Coordinates(800, 800), Snake(Coordinates(20, 20)))
    mp.snake.eat(Coordinates(1, 0))
    mp.snake.eat(Coordinates(1, 0))
    mp.draw_map(sc)
    run = True
    x = -1
    direction = Coordinates(1, 0)
    while x == -1:
        #time.sleep(0.025)
        #x = mp.get_snake_move(direction)
        #mp.draw_map(sc)
        l = mp.a_star(sc)
        for i in l:
            x = mp.get_snake_move(i)
            mp.draw_map(sc)
            for event in pygame.event.get():
                """
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if not mp.snake.opposite_direction(Coordinates(-1, 0)):
                    direction = Coordinates(-1, 0)
            if keys[pygame.K_RIGHT]:
                if not mp.snake.opposite_direction(Coordinates(1, 0)):
                    direction = Coordinates(1, 0)
            if keys[pygame.K_UP]:
                if not mp.snake.opposite_direction(Coordinates(0, -1)):
                    direction = Coordinates(0, -1)
            if keys[pygame.K_DOWN]:
                if not mp.snake.opposite_direction(Coordinates(0, 1)):
                    direction = Coordinates(0, 1)"""

                if event.type == pygame.QUIT:
                    run = False
