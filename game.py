import random
from typing import List, Tuple      # snake body = list of coordinate tuples

Direction = Tuple[int, int]         # (1, 0) → Right, (-1, 0) → Left, (0, 1) → Down, (0, -1) → Above

class SnakeGame:
    def __init__(self, width: int = 20, height: int = 20):    # Constructor calling 
        self.width = width          # Board Size
        self.height = height
        self.reset()            # Starting State

    def reset(self):
        mid_x = self.width // 2         # Snake Journey starts from middle of the board
        mid_y = self.height // 2
        self.snake: List[Tuple[int,int]] = [(mid_x, mid_y), (mid_x-1, mid_y)]  # head + tail
        self.direction: Direction = (1, 0)  # moving right direction
        self.spawn_food()     # Spawning Food
        self.alive = True     # Game is going on
        self.score = 0

    def spawn_food(self):
        empty = [(x,y) for x in range(self.width) for y in range(self.height) if (x,y) not in self.snake]  # Empty cell list creation without snake body
        self.food = random.choice(empty) if empty else None  # None if no place is empty

    def step(self):
        if not self.alive:
            return
        head_x, head_y = self.snake[0]   # New Head Position
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.width, (head_y + dy) % self.height)  # Wrap around effect

        # collision with self
        if new_head in self.snake:
            self.alive = False          # If new head is inside snake body, game over
            return

        # move
        self.snake.insert(0, new_head)

        # eat food
        if self.food and new_head == self.food:
            self.score += 1     # Score increases
            self.spawn_food()   # New Food
        else:
            self.snake.pop()    # move effect

    def set_direction(self, dx: int, dy: int):
        # prevent reverse move to 180 degree
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.direction = (dx, dy)

    def get_state(self):
        return {                    # Create a dictionary to send from server to client
            'width': self.width,
            'height': self.height,
            'snake': self.snake,
            'food': self.food,
            'alive': self.alive,
            'score': self.score,
        }