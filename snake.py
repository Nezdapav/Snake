
class Coordinates:
    x: int = None
    y: int = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.y}:{self.x}"


class Snake:

    class Body:

        def __init__(self, previousone, nextone, coordinatess):
            self.previousOne = previousone
            self.nextOne = nextone
            self.coordinates = coordinatess

    def __init__(self, coordinatess):
        self.length = 1
        self.score = 0
        self.head = Snake.Body(None, None, coordinatess)
        self.tail = self.head

    def look_at_body(self):
        x = self.head
        while x is not None:
            print(x.coordinates.x, x.coordinates.y)
            x = x.nextOne

    def move(self, direction):
        if self.tail.previousOne is None:
            self.head.coordinates.x += direction.x
            self.head.coordinates.y += direction.y
        else:
            x = self.tail.previousOne
            x.nextOne = None
            self.tail = x
            tmp = Snake.Body(None, self.head, Coordinates(self.head.coordinates.x + direction.x, self.head.coordinates.y + direction.y))
            self.head.previousOne = tmp
            self.head = tmp

    def opposite_direction(self, direction):
        if self.head.nextOne is not None:
            g = self.head.nextOne
            tmp = Coordinates(self.head.coordinates.x - g.coordinates.x, self.head.coordinates.y - g.coordinates.y)
            if (tmp.x == direction.x and tmp.y == -direction.y) or (tmp.x == -direction.x and tmp.y == direction.y):
                return True
        return False

    def eat(self, direction):
        tmp = Snake.Body(None, self.head, Coordinates(self.head.coordinates.x + direction.x, self.head.coordinates.y + direction.y))
        self.head.previousOne = tmp
        self.head = tmp
        self.length += 1
        self.score += 1
        return self
