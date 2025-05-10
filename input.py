import sys
import select
import tty
import termios

# Original Source : https://stackoverflow.com/a/2409034

class InputReader:
    ARROW_UP = 'up'
    ARROW_DOWN = 'down'
    ARROW_RIGHT = 'right'
    ARROW_LEFT = 'left'

    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def check(self):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    
    def get(self):
        key = sys.stdin.read(1)

        # arrow keys are combination of ESC , [ and 
        # one of these litters (A, B, C and D)
        if key == '\x1b': # ESC
            next = sys.stdin.read(2)

            if next == '[A':
                return self.ARROW_UP
            elif next == '[B':
                return self.ARROW_DOWN
            elif next == '[C':
                return self.ARROW_RIGHT
            elif next == '[D':
                return self.ARROW_LEFT
        
        return key
            
    def stop(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)