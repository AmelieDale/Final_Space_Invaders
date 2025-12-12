import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# ---------- Constants ----------
CELL_SIZE = 6  # size of each block cell (pixel width & height)
BLOCK_COLOR = (243,216,63)  # colour of the obstical

# ---------- Block Sprite (single obstacle cell) ----------
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # create a Surface so Pygame can render the block
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill((0,255,0))  # colour
        # set rect for positioning and collision
        self.rect = self.image.get_rect(topleft=(x, y))
# ---------- Define the Grid ----------#
grid = [
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]

class Obstacle:
    def __init__(self, x, y):
        self.blocks_group = pygame.sprite.Group()
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1:
                    pos_x = x + column * 3
                    pos_y = y + row * 3
                    block = Block(pos_x, pos_y)
                    self.blocks_group.add(block)
	
    def create_obstacles(num=4, top_y=420):
        obstacles = []
        blocks_group = pygame.sprite.Group()
        margin = 80
        usable_width = SCREEN_WIDTH - 2 * margin
        spacing_between = usable_width // (num - 1) if num > 1 else 0

        for i in range(num):
            x = margin - 20 + i * spacing_between
            y = top_y
            obs = Obstacle(x, y)
            obstacles.append(obs)
            for b in obs.blocks_group:
                blocks_group.add(b)

        return obstacles, blocks_group
