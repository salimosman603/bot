FROM python:3.10-slim

# Install dependencies including Tor and GUI libraries
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    tor \
    xvfb \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libharfbuzz0b \
    libgdk-pixbuf2.0-0

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Configure Tor
RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc
RUN echo "Log notice stdout" >> /etc/tor/torrc
RUN echo "ExitPolicy reject *:*" >> /etc/tor/torrc  # Prevent becoming exit node

# Set up application
WORKDIR /app
COPY . .
RUN pip install -r deploy/requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Start services
CMD service tor start && \
    Xvfb :0 -screen 0 1024x768x24 & \
    export DISPLAY=:0 && \
    python start.py