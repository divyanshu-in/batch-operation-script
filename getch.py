import os
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

color = {
    "red": "\033[31m",  # for errors
    "green": "\033[32m",
    "yellow": "\033[33m",  # for input
    "blue": "\033[34m",  # for indication
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "reset": "\033[0m",
}


getch = _Getch()

# if __name__ == '__main__':
#     print('press a key')
#     k = getch().decode('UTF-8')
#     selected = False
#     while k == ' ':
#         os.system('cls' if os.name == 'nt' else 'clear')
#         if selected:
#             print(color['yellow'],'(',color['green'],'*',color['yellow'],')',sep='')
#         else:
#             print('( )')
        
#         selected = not selected
#         k = getch().decode('UTF-8')
#     print(color['reset'])


# if __name__ == '__main__':
#     print('press a key')
#     k = getch().decode('UTF-8')
#     print(k)
