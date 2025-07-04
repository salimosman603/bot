import random
import time
import math
import numpy as np

def random_delay(min_sec, max_sec):
    """Human-like delay with random variation"""
    base = random.uniform(min_sec, max_sec)
    variation = base * random.uniform(-0.2, 0.2)
    time.sleep(base + variation)

def human_like_mouse_move(page, start_x, start_y, end_x, end_y):
    """More realistic mouse movement with physics-based simulation"""
    # Control points for Bezier curve
    cp1_x = start_x + (end_x - start_x) * random.uniform(0.2, 0.4)
    cp1_y = start_y + (end_y - start_y) * random.uniform(0.1, 0.3)
    cp2_x = start_x + (end_x - start_x) * random.uniform(0.6, 0.8)
    cp2_y = start_y + (end_y - start_y) * random.uniform(0.7, 0.9)
    
    steps = random.randint(20, 40)
    for i in range(steps):
        t = i / steps
        # Cubic Bezier formula
        x = (1-t)**3 * start_x + 3*(1-t)**2*t*cp1_x + 3*(1-t)*t**2*cp2_x + t**3*end_x
        y = (1-t)**3 * start_y + 3*(1-t)**2*t*cp1_y + 3*(1-t)*t**2*cp2_y + t**3*end_y
        
        # Add natural tremor
        tremor_x = random.gauss(0, 0.8)
        tremor_y = random.gauss(0, 0.8)
        
        page.mouse.move(x + tremor_x, y + tremor_y)
        time.sleep(random.uniform(0.005, 0.03))

def random_mouse_movement(page):
    """Random mouse movements while 'reading' the page"""
    movements = random.randint(3, 8)
    viewport = page.evaluate("() => ({width: window.innerWidth, height: window.innerHeight})")
    
    for _ in range(movements):
        start_x = random.randint(0, viewport['width'])
        start_y = random.randint(0, viewport['height'])
        end_x = random.randint(0, viewport['width'])
        end_y = random.randint(0, viewport['height'])
        
        human_like_mouse_move(page, start_x, start_y, end_x, end_y)
        time.sleep(random.uniform(0.2, 1.5))
        
        # Random click 20% of the time
        if random.random() < 0.2:
            page.mouse.down()
            time.sleep(random.uniform(0.05, 0.15))
            page.mouse.up()
            time.sleep(random.uniform(0.5, 1.5))

def simulate_reading(page):
    """Simulates reading behavior with random actions"""
    # Random scroll actions while reading
    scrolls = random.randint(1, 4)
    for _ in range(scrolls):
        scroll_distance = random.randint(100, 500)
        direction = 1 if random.random() > 0.3 else -1  # 70% down, 30% up
        
        page.mouse.wheel(0, scroll_distance * direction)
        time.sleep(random.uniform(1.0, 3.0))
        
        # Random pause to "read"
        if random.random() > 0.7:  # 30% chance for longer pause
            random_delay(2, 5)
            
        # Random highlight (mouse down + move)
        if random.random() < 0.4:
            x = random.randint(50, page.evaluate("window.innerWidth") - 50)
            y = random.randint(50, page.evaluate("window.innerHeight") - 50)
            page.mouse.move(x, y)
            page.mouse.down()
            
            # Simulate highlighting text
            for i in range(5):
                page.mouse.move(x + i*20, y, steps=1)
                time.sleep(0.05)
            
            page.mouse.up()
            time.sleep(random.uniform(0.5, 1.0))