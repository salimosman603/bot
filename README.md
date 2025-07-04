# Ad Traffic Bot

**WARNING: This project is for educational purposes only. Ad fraud is illegal.**

## Setup

1. Install dependencies: `pip install -r deploy/requirements.txt`
2. Install Playwright: `playwright install chromium`
3. Add proxies to `config/proxies.txt` (one per line)
4. Configure `config/settings.py` for your targets.

## Running

`python start.py`

## Docker

Build: `docker build -t ad-bot -f deploy/Dockerfile .`

Run: `docker run -it --rm ad-bot`