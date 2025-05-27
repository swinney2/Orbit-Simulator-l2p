# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (64, 64, 64)
BRIGHT_YELLOW = (255, 255, 128)

# Physics constants
G = 0.1  # Reduced gravitational constant for better visualization
SCALE = 1.0  # No scaling needed since we're using simplified units
DT = 0.016  # Smaller time step (roughly 1/60 second)

# Speed control settings
MIN_TIME_SCALE = 1.0
MAX_TIME_SCALE = 5000.0
SPEED_BAR_HEIGHT = 20
SPEED_BAR_WIDTH = 400
SPEED_BAR_MARGIN = 40
SPEED_HANDLE_WIDTH = 10
SPEED_HANDLE_HEIGHT = 30

# Trail settings
MAX_TRAIL_LENGTH = 50
TRAIL_FADE = True

# Celestial body types
CELESTIAL_BODIES = {
    'fixed_star': {
        'mass': 5000,
        'radius': 20,
        'color': BRIGHT_YELLOW,
        'key': '0',
        'is_fixed': True
    },
    'star': {
        'mass': 2000,
        'radius': 15,
        'color': YELLOW,
        'key': '1',
        'is_fixed': False
    },
    'planet': {
        'mass': 200,
        'radius': 8,
        'color': BLUE,
        'key': '2',
        'is_fixed': False
    },
    'moon': {
        'mass': 50,
        'radius': 4,
        'color': GRAY,
        'key': '3',
        'is_fixed': False
    },
    'asteroid': {
        'mass': 10,
        'radius': 2,
        'color': RED,
        'key': '4',
        'is_fixed': False
    }
}

# Default body settings
DEFAULT_MASS = 1000  # Reduced mass
DEFAULT_RADIUS = 10  # Smaller radius 