class Block:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def add(self, other):
        self.y += other.y
        self.x += other.x

class Tetromino:
    def __init__(self, y, x, id = '', rotation = 0):
        self.blocks = [
            Block(y, x),
            Block(y, x),
            Block(y, x),
            Block(y, x),
        ]
    
        self.id = ''
        self.rotation = 0
    
    def update(self, positions):
        for i in range(len(self.blocks)):
            self.blocks[i].add(positions[i])

    def reset(self, y, x):
        for i in range(len(self.blocks)):
            self.blocks[i].y = y
            self.blocks[i].x = x

    def rotate(self):
        if self.id == 'O':
            return
        
        self.rotation += 1

        if (self.id in 'ISZ' and self.rotation == 2) or self.rotation == 4:
            self.rotation = 0

        tetrominos_rotations = {
            'I': {
                0: [Block(-1, 0), Block(0, 0), Block(1, 0), Block(2, 0)],
                1: [Block(0, 1), Block(0, 0), Block(0, -1), Block(0, -2)]
            },
            'S': {
                0: [Block(0, 1), Block(0, 0), Block(1, 0), Block(1, -1)],
                1: [Block(-1, 0), Block(0, 0), Block(0, 1), Block(1, 1)]
            },
            'Z': {
                0: [Block(0, -1), Block(0, 0), Block(1, 0), Block(1, 1)],
                1: [Block(-1, 0), Block(0, 0), Block(0, -1), Block(1, -1)]
            },
            'T': {
                0: [Block(0, -1), Block(0, 0), Block(0, 1), Block(1, 0)],
                1: [Block(-1, 0), Block(0, 0), Block(1, 0), Block(0, -1)],
                2: [Block(0, -1), Block(0, 0), Block(0, 1), Block(-1, 0)],
                3: [Block(-1, 0), Block(0, 0), Block(1, 0), Block(0, 1)]
            },
            'L': {
                0: [Block(-1, 0), Block(0, 0), Block(1, 0), Block(1, 1)],
                1: [Block(0, -1), Block(0, 0), Block(0, 1), Block(1, -1)],
                2: [Block(1, 0), Block(0, 0), Block(-1, 0), Block(-1, -1)],
                3: [Block(0, -1), Block(0, 0), Block(0, 1), Block(-1, 1)]
            },
            'J': {
                0: [Block(-1, 0), Block(0, 0), Block(1, 0), Block(1, -1)],
                1: [Block(0, -1), Block(0, 0), Block(0, 1), Block(-1, -1)],
                2: [Block(1, 0), Block(0, 0), Block(-1, 0), Block(-1, 1)],
                3: [Block(0, -1), Block(0, 0), Block(0, 1), Block(1, 1)]
            },
        }

        # we use block[1] as a reference to rotate around
        # then we rotate clockwise +90 degrees around that block
        self.reset(self.blocks[1].y, self.blocks[1].x)
        self.update(tetrominos_rotations[self.id][self.rotation])