import sys

class Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    
    def __init__(self):
        self.impl = self._get_platform_specific_getch()

    def __call__(self):
        return self.impl()

    @staticmethod
    def _get_platform_specific_getch():
        """Determines the appropriate implementation based on the platform."""
        if sys.platform.startswith('win'):
            return GetchWindows()
        else:
            return GetchUnix()


class GetchUnix:
    """Unix-specific implementation of getting a single character."""
    
    def __call__(self):
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows:
    """Windows-specific implementation of getting a single character."""
    
    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode('utf-8')  # Decode to match Unix behavior


# Create a single instance of Getch for use
getch = Getch()