from snake import Coordinates
from enum import Enum
from snake import Snake
import random
import pygame


class Node:
    def __init__(self, coordinates, value):
        self.coordinates = coordinates
        self.value = value
        self.parent: Node = None

    def expand_node(self, map):
        listt = []
        if self.coordinates.x + 1 < map.width-1:
            if map.mapa[self.coordinates.y][self.coordinates.x+1] == Type.SPACE or map.mapa[self.coordinates.y][self.coordinates.x+1] == Type.APPLE:
                listt.append(Coordinates(self.coordinates.x+1, self.coordinates.y))
        if self.coordinates.y - 1 > 0:
            if map.mapa[self.coordinates.y-1][self.coordinates.x] == Type.SPACE or map.mapa[self.coordinates.y-1][self.coordinates.x] == Type.APPLE:
                listt.append(Coordinates(self.coordinates.x, self.coordinates.y-1))
        if self.coordinates.x - 1 > 0:
            if map.mapa[self.coordinates.y][self.coordinates.x - 1] == Type.SPACE or map.mapa[self.coordinates.y][self.coordinates.x-1] == Type.APPLE:
                listt.append(Coordinates(self.coordinates.x-1, self.coordinates.y))
        if self.coordinates.y + 1 < map.height-1:
            if map.mapa[self.coordinates.y+1][self.coordinates.x] == Type.SPACE or map.mapa[self.coordinates.y+1][self.coordinates.x] == Type.APPLE:
                listt.append(Coordinates(self.coordinates.x, self.coordinates.y+1))
        return listt

    def trace_back(self, map):
        list = []
        tmp = self
        while not (tmp.coordinates.x == map.snake.head.coordinates.x and tmp.coordinates.y == map.snake.head.coordinates.y):
            list.insert(0, Coordinates(tmp.coordinates.x-tmp.parent.coordinates.x, tmp.coordinates.y-tmp.parent.coordinates.y))
            tmp = tmp.parent
        return list


class PriQue:
    queuee = []

    def __init__(self):
        self.queuee = []

    def put(self, tmp):
        x = len(self.queuee)
        y = 0
        while not x <= y :
            pr = (x+y)//2
            if self.queuee[pr].value < tmp.value:
                y = pr + 1
            elif self.queuee[pr].value > tmp.value:
                x = pr
            else:
                x = pr
                y = pr
        self.queuee.insert(x, tmp)

    def empty(self):
        return len(self.queuee) == 0

    def pop(self):
        self.queuee.pop(0)

    def get(self):
        return self.queuee[0]


class Type(Enum):
    WALL = 0
    SNAKE = 1
    SPACE = 2
    APPLE = 3
    ALG = 4


class Situation(Enum):
    CRASH = 0
    OPPOSITEDIRECTION = 1
    FREE = 2


class Map:

    def __init__(self, boundaries, snake):
        self.boundaries = boundaries
        self.scale = 10
        self.height = self.boundaries.y // self.scale
        self.width = self.boundaries.x // self.scale
        self.mapa = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.snake: Snake = snake
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.mapa[i][j] = Type.WALL
                else:
                    self.mapa[i][j] = Type.SPACE
        self.apple = self.random_coords()
        self.mapa[self.apple.y][self.apple.x] = Type.APPLE

    def draw_map(self, sc):
        for y in range(self.height):
            for x in range(self.width):
                color = (0, 0, 0)
                if self.mapa[y][x] == Type.WALL:
                    color = (255, 0, 0)
                elif self.mapa[y][x] == Type.SNAKE:
                    color = (0, 255, 0)
                elif self.mapa[y][x] == Type.APPLE:
                    color = (0, 0, 255)
                elif self.mapa[y][x] == Type.ALG:
                    color = (0, 125, 125)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(sc, color, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale), 0)
        pygame.display.flip()

    def clear_snake(self):
        x = self.snake.head
        while x is not None:
            self.mapa[x.coordinates.y][x.coordinates.x] = Type.SPACE
            x = x.nextOne

    def write_down_snake(self):
        x = self.snake.head
        while x is not None:
            self.mapa[x.coordinates.y][x.coordinates.x] = Type.SNAKE
            x = x.nextOne

    def get_snake_move(self, coordinates):
        if self.mapa[self.snake.head.coordinates.y + coordinates.y][self.snake.head.coordinates.x + coordinates.x] == Type.SPACE:
            self.clear_snake()
            self.snake.move(coordinates)
            self.write_down_snake()
            return -1
        elif self.mapa[self.snake.head.coordinates.y + coordinates.y][self.snake.head.coordinates.x + coordinates.x] == Type.APPLE:
            self.new_apple()
            self.clear_snake()
            self.snake.eat(coordinates)
            self.write_down_snake()
            return -1
        return self.snake.score

    def random_coords(self):
        random.seed(None)
        x = Coordinates(0, 0)
        while self.mapa[x.y][x.x] != Type.SPACE:
            x = Coordinates(random.randint(1, int(self.height - 2)), random.randint(1, int(self.width - 2)))

        return x

    def new_apple(self):
        self.mapa[self.apple.y][self.apple.x] = Type.SPACE
        self.apple = self.random_coords()
        self.mapa[self.apple.y][self.apple.x] = Type.APPLE

    def a_star(self, sc):
        que = PriQue()
        h = Node(self.snake.head.coordinates, 0)
        que.put(h)
        while not que.empty():
            a = que.get()
            que.pop()
            for i in a.expand_node(self):
                k = Node(i, (self.apple.x - i.x)**2 + (self.apple.y - i.y)**2)
                k.parent = a
                # traceback
                if i.x == self.apple.x and i.y == self.apple.y:
                    for i in range(self.height):
                        for j in range(self.width):
                            if self.mapa[i][j] == Type.ALG:
                                self.mapa[i][j] = Type.SPACE

                    return k.trace_back(self)

                self.mapa[i.y][i.x] = Type.ALG
                que.put(k)
