FROM python:3.10-slim

# Install dependencies
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
    libgdk-pixbuf2.0-0 \
    libsocks5-dev \
    libsodium-dev

# Configure Tor
RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc && \
    echo "Log notice stdout" >> /etc/tor/torrc && \
    echo "ExitPolicy reject *:*" >> /etc/tor/torrc

# Set up application
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r deploy/requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Cleanup to reduce image size
RUN apt-get purge -y wget gnupg && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Start services
CMD service tor start && \
    Xvfb :0 -screen 0 1024x768x24 & \
    export DISPLAY=:0 && \
    python start.py