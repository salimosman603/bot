from playwright.sync_api import BrowserContext
import random
import os
import json

def apply_stealth(context: BrowserContext, device_profile: dict = None):
    """Enhanced stealth techniques with device profile integration"""
    # Base stealth script
    base_script = """
    // Remove webdriver flag
    delete Object.getPrototypeOf(navigator).webdriver;
    
    // Spoof permissions
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ? 
            Promise.resolve({ state: Notification.permission }) : 
            originalQuery(parameters)
    );
    
    // Spoof plugins
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
        configurable: false,
        enumerable: true
    });
    
    // Spoof mimeTypes
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => [1, 2, 3],
        configurable: false,
        enumerable: true
    });
    
    // Hide headless Chrome
    window.chrome = { runtime: {} };
    """
    
    # Add device-specific spoofing if profile is available
    if device_profile:
        # WebGL spoofing
        webgl_script = f"""
        // WebGL vendor spoofing
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37445) {{ // UNMASKED_VENDOR_WEBGL
                return '{device_profile.get('webglVendor', 'Google Inc. (NVIDIA)')}';
            }}
            if (parameter === 37446) {{ // UNMASKED_RENDERER_WEBGL
                return '{device_profile.get('webglRenderer', 'ANGLE (NVIDIA)')}';
            }}
            return getParameter.apply(this, [parameter]);
        }};
        """
        
        # AudioContext spoofing
        audio_script = f"""
        // AudioContext sample rate spoofing
        const oldAudioContext = window.AudioContext || window.webkitAudioContext;
        window.AudioContext = class FakeAudioContext extends oldAudioContext {{
            constructor() {{
                super();
                Object.defineProperty(this, 'sampleRate', {{
                    get() {{ return {device_profile.get('audioContext', {}).get('sampleRate', 44100)}; }}
                }});
            }}
        }};
        window.webkitAudioContext = window.AudioContext;
        """
        
        base_script += webgl_script + audio_script
    
    # Add canvas fingerprint defense
    canvas_script = """
    // Canvas fingerprint defense
    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type, ...args) {
        const context = this.getContext('2d');
        const imageData = context.getImageData(0, 0, this.width, this.height);
        const data = imageData.data;
        
        // Add subtle random noise
        for (let i = 0; i < data.length; i += 10) {
            if (Math.random() > 0.7) {
                data[i] = Math.min(255, Math.max(0, data[i] + Math.floor(Math.random() * 10 - 5));
                data[i+1] = Math.min(255, Math.max(0, data[i+1] + Math.floor(Math.random() * 10 - 5));
                data[i+2] = Math.min(255, Math.max(0, data[i+2] + Math.floor(Math.random() * 10 - 5));
            }
        }
        
        context.putImageData(imageData, 0, 0);
        return toDataURL.call(this, type, ...args);
    };
    """
    
    # Add font spoofing
    font_script = """
    // Font enumeration spoofing
    const element = document.createElement('div');
    element.style.font = 'monospace';
    document.body.appendChild(element);
    
    Object.defineProperty(navigator, 'fonts', {
        value: {
            async query() {
                return [
                    { family: 'Arial', status: 'available' },
                    { family: 'Times New Roman', status: 'available' },
                    { family: 'Courier New', status: 'available' }
                ];
            }
        },
        configurable: false,
        enumerable: true
    });
    """
    
    context.add_init_script(base_script + canvas_script + font_script)
    
    # Spoof HTTP headers
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-CH-UA": f'"Chromium";v="{random.randint(90,112)}", "Not A;Brand";v="24"'
    }
    
    # Add device-specific headers if available
    if device_profile:
        headers.update({
            "User-Agent": device_profile['user_agent'],
            "X-Device-Platform": device_profile.get('platform', 'Win32')
        })
    
    context.set_extra_http_headers(headers)