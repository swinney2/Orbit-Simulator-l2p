# 2D Orbit Simulator

A real-time interactive 2D sandbox that lets users simulate gravitational interactions between celestial bodies.

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulator

Run the simulator with:
```bash
python main.py
```

## Controls

- **Left Click + Drag**: Create a new body. The drag direction and length determine the initial velocity
- **Right Click**: Delete a body (when clicking on it)
- **Space**: Pause/Resume simulation
- **R**: Reset simulation (clear all bodies)
- **1**: Set time scale to 1x
- **2**: Set time scale to 2x
- **5**: Set time scale to 5x

## Features

- Newtonian gravity simulation between multiple bodies
- Real-time visualization with particle trails
- Interactive body creation and deletion
- Time control (pause, play, different speeds)
- Velocity visualization during body creation

## Physics

The simulator uses Newtonian gravity:
- Force calculation: F = G * (m1 * m2) / r²
- Verlet integration for position and velocity updates
- Configurable time step and gravitational constant

## Tips

1. Try creating a central massive body and smaller bodies orbiting around it
2. Experiment with different initial velocities to achieve stable orbits
3. Create multiple bodies to observe complex gravitational interactions
4. Use time scaling to speed up or slow down the simulation as needed 