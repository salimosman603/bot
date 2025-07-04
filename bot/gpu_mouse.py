import numpy as np
import random
import time

def human_click(page, x, y, max_deviation=15):
    """Advanced human-like click simulation with physics"""
    # Get current mouse position
    current_x, current_y = 0, 0  # Start from top-left corner
    
    # Generate path with momentum-based physics
    path = []
    steps = random.randint(30, 50)
    velocity_x = (x - current_x) / steps
    velocity_y = (y - current_y) / steps
    current_x, current_y = 0, 0
    
    for i in range(steps):
        # Apply momentum with slight overshoot correction
        momentum = 1.0 - (i / steps) ** 2
        current_x += velocity_x * momentum + random.gauss(0, max_deviation * (1 - i/steps))
        current_y += velocity_y * momentum + random.gauss(0, max_deviation * (1 - i/steps))
        
        # Correct overshoot
        if abs(current_x - x) < 10 and abs(current_y - y) < 10:
            break
            
        path.append((current_x, current_y))
    
    # Move through the path
    for point in path:
        page.mouse.move(point[0], point[1])
        time.sleep(random.uniform(0.005, 0.03))
    
    # Final adjustments
    page.mouse.move(x, y)
    time.sleep(random.uniform(0.1, 0.3))
    
    # Click with human-like press/release timing
    page.mouse.down()
    time.sleep(random.uniform(0.08, 0.25))
    page.mouse.up()
    time.sleep(random.uniform(0.3, 1.0))