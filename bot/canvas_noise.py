import random
import base64

def add_canvas_noise(page) -> str:
    """
    Adds random noise to Canvas rendering to prevent fingerprinting
    Returns base64 of modified canvas image for debugging
    """
    script = """
    // Create a temporary canvas
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    
    // Draw something on canvas
    ctx.fillStyle = 'rgb(200, 0, 0)';
    ctx.fillRect(10, 10, 100, 100);
    
    // Add random noise to image data
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
        // Add subtle random noise to RGB channels
        if (Math.random() > 0.7) {
            data[i] = Math.min(255, Math.max(0, data[i] + Math.floor(Math.random() * 10 - 5)));
            data[i+1] = Math.min(255, Math.max(0, data[i+1] + Math.floor(Math.random() * 10 - 5)));
            data[i+2] = Math.min(255, Math.max(0, data[i+2] + Math.floor(Math.random() * 10 - 5)));
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
    
    // Return as data URL
    return canvas.toDataURL();
    """
    
    try:
        result = page.evaluate(script)
        return result.split(',')[1]  # Return base64 part
    except Exception as e:
        print(f"Canvas noise injection failed: {str(e)}")
        return ""