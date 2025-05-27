import numpy as np
from collections import deque
import pygame
from config import MAX_TRAIL_LENGTH, TRAIL_FADE, WHITE

class Body:
    def __init__(self, x, y, mass, radius, color=WHITE, is_fixed=False):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.acceleration = np.array([0, 0], dtype=float)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = deque(maxlen=MAX_TRAIL_LENGTH)
        self.is_fixed = is_fixed
        
    def update(self, dt):
        if not self.is_fixed:
            # Update position and velocity using Verlet integration
            self.position += self.velocity * dt + 0.5 * self.acceleration * dt * dt
            self.velocity += self.acceleration * dt
        self.trail.append(tuple(self.position))
        
    def draw(self, screen, offset=(0, 0), scale=1.0):
        # Draw the body
        pos = (int(self.position[0] * scale + offset[0]), 
               int(self.position[1] * scale + offset[1]))
        pygame.draw.circle(screen, self.color, pos, int(self.radius * scale))
        
        # Draw the trail
        if len(self.trail) > 1:
            points = [(int(p[0] * scale + offset[0]), 
                      int(p[1] * scale + offset[1])) for p in self.trail]
            
            if TRAIL_FADE:
                # Draw trail with fading effect
                for i in range(len(points) - 1):
                    alpha = int(255 * (i / len(points)))
                    color = (*self.color[:3], alpha)
                    surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                    pygame.draw.line(surface, color, points[i], points[i + 1], 2)
                    screen.blit(surface, (0, 0))
            else:
                # Draw solid trail
                pygame.draw.lines(screen, self.color, False, points, 2)
                
    def apply_force(self, force):
        if not self.is_fixed:
            self.acceleration = force / self.mass
        
    def set_velocity(self, velocity):
        if not self.is_fixed:
            self.velocity = np.array(velocity, dtype=float) 