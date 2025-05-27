import numpy as np
from config import G

def calculate_gravity(body1, body2):
    """Calculate the gravitational force between two bodies."""
    # Get the vector from body1 to body2
    r = body2.position - body1.position
    
    # Calculate the distance between the bodies
    distance = np.linalg.norm(r)
    
    # Avoid division by zero
    if distance < 1e-10:
        return np.array([0, 0])
    
    # Calculate the magnitude of the gravitational force
    force_magnitude = G * body1.mass * body2.mass / (distance * distance)
    
    # Calculate the direction (unit vector)
    direction = r / distance
    
    # Return the force vector
    return force_magnitude * direction

def update_bodies(bodies, dt):
    """Update all bodies' positions and velocities."""
    # Calculate forces
    for i, body1 in enumerate(bodies):
        # Reset acceleration
        total_force = np.zeros(2)
        
        # Calculate total force on this body from all other bodies
        for j, body2 in enumerate(bodies):
            if i != j:  # Don't calculate force with itself
                force = calculate_gravity(body1, body2)
                total_force += force
        
        # Apply the total force
        body1.apply_force(total_force)
    
    # Update positions and velocities
    for body in bodies:
        body.update(dt)

def check_collision(body1, body2):
    """Check if two bodies are colliding."""
    distance = np.linalg.norm(body2.position - body1.position)
    return distance < (body1.radius + body2.radius) 