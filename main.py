import pygame
import numpy as np
from config import *
from body import Body
from physics import update_bodies
import sys
import math

class OrbitSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D Orbit Simulator")
        self.clock = pygame.time.Clock()
        
        self.bodies = []
        self.paused = False
        self.time_scale = MIN_TIME_SCALE
        self.dragging = False
        self.drag_start = None
        
        # Initialize font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Set initial body type
        self.current_body_type = 'star'
        
        # Speed control variables
        self.speed_dragging = False
        self.speed_bar_rect = pygame.Rect(
            (WINDOW_WIDTH - SPEED_BAR_WIDTH) // 2,
            WINDOW_HEIGHT - SPEED_BAR_MARGIN,
            SPEED_BAR_WIDTH,
            SPEED_BAR_HEIGHT
        )
        
    def get_speed_handle_pos(self):
        # Convert current time scale to position
        scale_factor = (math.log10(self.time_scale) - math.log10(MIN_TIME_SCALE)) / (math.log10(MAX_TIME_SCALE) - math.log10(MIN_TIME_SCALE))
        x = self.speed_bar_rect.left + (self.speed_bar_rect.width * scale_factor)
        return max(self.speed_bar_rect.left, min(x, self.speed_bar_rect.right))
        
    def get_speed_handle_rect(self):
        x = self.get_speed_handle_pos()
        return pygame.Rect(
            x - SPEED_HANDLE_WIDTH // 2,
            self.speed_bar_rect.centery - SPEED_HANDLE_HEIGHT // 2,
            SPEED_HANDLE_WIDTH,
            SPEED_HANDLE_HEIGHT
        )
        
    def set_time_scale_from_pos(self, x):
        # Convert position to time scale using logarithmic scale
        scale_factor = (x - self.speed_bar_rect.left) / self.speed_bar_rect.width
        scale_factor = max(0, min(1, scale_factor))
        log_scale = math.log10(MIN_TIME_SCALE) + scale_factor * (math.log10(MAX_TIME_SCALE) - math.log10(MIN_TIME_SCALE))
        self.time_scale = 10 ** log_scale
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.bodies.clear()
                    
                # Check for body type selection keys
                key_pressed = event.unicode
                for body_type, properties in CELESTIAL_BODIES.items():
                    if key_pressed == properties['key']:
                        self.current_body_type = body_type
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking speed handle
                    handle_rect = self.get_speed_handle_rect()
                    speed_bar_area = self.speed_bar_rect.inflate(0, SPEED_HANDLE_HEIGHT)
                    mouse_pos = event.pos
                    
                    if handle_rect.collidepoint(mouse_pos) or speed_bar_area.collidepoint(mouse_pos):
                        self.speed_dragging = True
                        # If clicked on bar but not handle, move handle to click position
                        if not handle_rect.collidepoint(mouse_pos):
                            self.set_time_scale_from_pos(mouse_pos[0])
                    else:
                        self.dragging = True
                        self.drag_start = event.pos
                        
                elif event.button == 3:  # Right click
                    # Remove body if clicked on one
                    pos = event.pos
                    for body in self.bodies[:]:
                        screen_pos = (int(body.position[0]), int(body.position[1]))
                        if np.linalg.norm(np.array(pos) - np.array(screen_pos)) < body.radius:
                            self.bodies.remove(body)
                            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging:
                        end_pos = event.pos
                        # Calculate velocity based on drag vector
                        velocity = np.array([
                            (end_pos[0] - self.drag_start[0]) * 0.02,
                            (end_pos[1] - self.drag_start[1]) * 0.02
                        ])
                        
                        # Get properties for current body type
                        body_props = CELESTIAL_BODIES[self.current_body_type]
                        
                        # Create new body with selected properties
                        new_body = Body(
                            self.drag_start[0],
                            self.drag_start[1],
                            body_props['mass'],
                            body_props['radius'],
                            body_props['color'],
                            body_props['is_fixed']
                        )
                        # Only set velocity if the body isn't fixed
                        if not body_props['is_fixed']:
                            new_body.set_velocity(velocity)
                        self.bodies.append(new_body)
                        self.dragging = False
                    self.speed_dragging = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.speed_dragging:
                    self.set_time_scale_from_pos(event.pos[0])
                    
        return True
        
    def update(self):
        if not self.paused:
            update_bodies(self.bodies, DT * self.time_scale)
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw all bodies and their trails
        for body in self.bodies:
            body.draw(self.screen)
            
        # Draw drag line when creating a new body
        if self.dragging:
            current_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, WHITE, self.drag_start, current_pos, 2)
        
        # Draw UI
        self.draw_ui()
        
        # Draw speed control bar
        self.draw_speed_control()
            
        pygame.display.flip()
        
    def draw_speed_control(self):
        # Draw the bar background
        pygame.draw.rect(self.screen, DARK_GRAY, self.speed_bar_rect)
        
        # Draw the handle
        handle_rect = self.get_speed_handle_rect()
        pygame.draw.rect(self.screen, WHITE, handle_rect)
        
        # Draw speed labels
        speed_text = f"{self.time_scale:.1f}x"
        text = self.small_font.render(speed_text, True, WHITE)
        text_rect = text.get_rect(midbottom=(self.speed_bar_rect.centerx, self.speed_bar_rect.top - 5))
        self.screen.blit(text, text_rect)
        
        # Draw min/max labels
        min_text = self.small_font.render("1x", True, WHITE)
        max_text = self.small_font.render("5000x", True, WHITE)
        self.screen.blit(min_text, (self.speed_bar_rect.left, self.speed_bar_rect.top - 25))
        self.screen.blit(max_text, (self.speed_bar_rect.right - 50, self.speed_bar_rect.top - 25))
        
    def draw_ui(self):
        # Draw current body type and controls
        y_pos = 10
        text = self.font.render(f"Selected: {self.current_body_type.title()}", True, WHITE)
        self.screen.blit(text, (10, y_pos))
        
        # Draw body type options
        y_pos += 40
        for body_type, props in CELESTIAL_BODIES.items():
            color = props['color']
            text = self.font.render(f"{props['key']}: {body_type.title()}", True, color)
            self.screen.blit(text, (10, y_pos))
            y_pos += 30
            
        # Draw other controls
        y_pos += 10
        controls = [
            "Space: Pause/Resume",
            "R: Reset",
            "Right click: Delete body"
        ]
        for control in controls:
            text = self.font.render(control, True, WHITE)
            self.screen.blit(text, (10, y_pos))
            y_pos += 30
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulator = OrbitSimulator()
    simulator.run() 