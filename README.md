# Ad Traffic Bot - User Guide

## 📌 Project Overview
This sophisticated bot system simulates human-like traffic to websites, interacting with advertisements in a realistic manner while avoiding detection. It uses cutting-edge techniques to mimic human behavior and bypass anti-bot measures. 

### Key Features
- 🕵️‍♂️ **Advanced fingerprint spoofing** (user agents, viewports, timezones)
- 🖱️ **Human-like mouse movements** with physics-based algorithms
- 🌐 **Proxy rotation** with residential proxies and Tor support
- 🧩 **Device profile integration** (Windows 11 Edge, macOS Chrome)
- 🛡️ **Anti-detection mechanisms** (canvas noise, WebGL spoofing)
- 📊 **Ad targeting** with intelligent selection algorithms
- 📈 **Traffic analytics** with fraud detection scoring

**⚠️ Important Legal Notice**:  
This software is for **educational purposes only**. Ad fraud is illegal in most jurisdictions. Use responsibly and only on websites where you have explicit permission.

## Project Structure
```
adPhantom-v1.1.0/
├── analysis/           # Fraud detection analytics
├── bot/                # Core bot functionality
│   ├── browser.py      # Browser simulation engine
│   ├── fingerprint.py  # Device fingerprint generation
│   ├── stealth_engine.py # Anti-detection systems
│   └── ...             # Other core components
├── config/             # Configuration files
│   ├── device_profiles/ # Device configurations
│   ├── proxies.txt     # Proxy list
│   └── settings.py     # Main settings
├── deploy/             # Deployment scripts
├── Dockerfile          # Container configuration
└── start.py            # Launch script
```

## Setup Guide

### Prerequisites
- Python 3.10+
- Playwright Chromium
- Tor
- Proxy list (residential recommended)

### Step-by-Step Setup:
#### Install dependencies
```
pip install -r requirements.txt
```
#### Install browser
```
playwright install chromium
```
### Set up configuration
1. **Add proxies** to `config/proxies.txt`: 
```
http://user:pass@ip:port
socks5://user:pass@ip:port
```

2. **Configure settings** in `config/settings.py`:
```python
# Example configuration
TARGET_SITES = [{
   'base_url': 'https://your-target-site.com',
   'entry_paths': ['/', '/products'],
   'ad_selectors': ['div.ad-banner', 'iframe.ad-frame'],
   'probability_click_ad': 0.35
 }]
```

3. **Add device profiles** in `config/device_profiles/` (sample profiles included)

## ⚙️ Configuration
Edit these files before running:

### 1. `config/settings.py`
- `MAX_SESSIONS`: Concurrent sessions (start with 5-10)
- `TARGET_SITES`: Configure your target websites:
  ```python
  'ad_selectors': ['div.ad-banner', 'iframe.ad']  # Update to match target site
  'probability_click_ad': 0.3  # Click probability (30%)
  ```

### 2. `.env` File
```
MAX_SESSIONS_PER_PROXY=2
USER_AGENT_ROTATION_INTERVAL=5
FRAUDSCORE_API_KEY=your_key_here  # Get from fraudscore.io
```

### 3. Device Profiles
Add more profiles in `config/device_profiles/`:
```json
{
  "os": "Windows",
  "browser": "Chrome",
  "viewport": {"width": 1280, "height": 720},
  "userAgent": "Mozilla/5.0 ..."
}
```

## 🚀 Running the Bot

### Basic Execution:
```bash
python start.py
```

### With Restart Script:
```bash
chmod +x run.sh
./run.sh
```

### Docker Setup:
```bash
docker build -t ad-bot -f deploy/Dockerfile .
docker run -it --rm ad-bot
```

## Key Configuration Options

### 🌐 Proxy Configuration
1. Add proxies to `config/proxies.txt` (one per line)
2. Supported formats:
 - `http://user:pass@ip:port`
 - `socks5://ip:port`
 - `socks5h://user:pass@ip:port`

The system automatically verifies and rotates proxies every 30 minutes.

### Device Profiles (`config/device_profiles/`)
- Pre-configured device fingerprints
- Customize existing profiles or add new JSON files
- Supports Windows, macOS, and mobile devices 

### Behavior Settings (`bot/behavior.py`)
- Adjust human-like interactions:
  ```python
  # Modify these values for different behaviors
  MIN_TIME_ON_PAGE = 10  # Minimum seconds per page
  MAX_TIME_ON_PAGE = 60  # Maximum seconds per page
  SCROLL_INTENSITY = 3   # Scroll frequency (1-5)
  ```

## Advanced Features

### Stealth Techniques
 - Canvas fingerprint randomization
 - WebGL vendor spoofing
 - Audio context manipulation
 - Font enumeration masking

### Human Behavior Simulation
 - Physics-based mouse movements
 - Reading pattern simulation
 - Randomized click patterns
 - Natural scrolling behaviors

### Fraud Detection Testing
```bash
python analysis/fraud_detect.py
```
 - Tests your traffic against fraud detection APIs
 - Provides risk score feedback
 - Helps tune stealth parameters

## 📊 Monitoring and Logs
Check log files in `/logs` directory:
 - `traffic.log` - Session details
 - `debug.log` - Technical errors (enable in settings)
 - Real-time console output
 - Health check endpoint: `http://localhost:8080/health`

## 🔍 Key Components Explained

| File | Purpose |
|------|---------|
| `browser.py` | Core automation engine |
| `behavior.py` | Human-like interactions |
| `stealth_engine.py` | Anti-detection techniques |
| `proxy.py` | Proxy management |
| `runner.py` | Session controller |
| `targets.py` | Website configuration |

## 🚨 Troubleshooting

**Common Issues:**
1. *Proxy connection failures*:
- Verify proxy format in `proxies.txt`
- Test proxies manually with:
```python
import requests
print(requests.get("https://ipinfo.io", proxies={"https": "your-proxy"}).text)
```

2. *Detection by websites*:
- Reduce `MAX_SESSIONS_PER_PROXY`
- Increase `SESSION_COOLDOWN` times
- Add more device profiles

3. *Browser launch errors*:
```bash
playwright install
sudo apt-get install libgbm-dev  # Linux dependencies
```

4. *Ads not being detected*:
 - Update CSS selectors in `settings.py > ad_selectors`
 
5. *High fraud scores*:
 - Increase proxy rotation frequency
 - Add more device profiles
 - Adjust behavior parameters in `bot/behavior.py`

6. *Browser detection*:
 - Enable additional stealth measures in `stealth_engine.py`

## ⚠️ Final Notes
1. Start with conservative settings (1-2 sessions)
2. Monitor `fraud_score` in logs (keep <0.25)
3. Rotate proxies frequently
4. Adjust behavior patterns per target site
5. Never use on sites without permission

## Legal and Ethical Considerations
⚠️ **Important Notice:**  
This tool is demonstrates browser automation capabilities. Using this system to generate fraudulent ad traffic:
- Is illegal in most jurisdictions
- Violates advertising platform terms
- Harms website owners and advertisers
- May result in legal consequences

The developers assume no liability for improper use.

Always obtain proper authorization before testing on any website. The authors assume no responsibility for misuse of this software.
