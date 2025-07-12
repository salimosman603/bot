FROM python:3.10-slim

# Install dependencies with optimized layers
RUN apt-get update && \
    apt-get install -y \
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
    libsodium-dev \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    xauth \
    dbus \
    # Clean up cache
    && rm -rf /var/lib/apt/lists/*

# Configure Tor with safe defaults
RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc && \
    echo "Log notice stdout" >> /etc/tor/torrc && \
    echo "ExitPolicy reject *:*" >> /etc/tor/torrc && \
    echo "AvoidDiskWrites 1" >> /etc/tor/torrc

# Set up application
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r deploy/requirements.txt

# Install Playwright browsers with dependencies
RUN playwright install --with-deps chromium

# Fix X display lock conflicts
RUN echo "#!/bin/bash\n" > /entrypoint.sh && \
    echo "rm -f /tmp/.X99-lock 2>/dev/null" >> /entrypoint.sh && \
    echo "Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &" >> /entrypoint.sh && \
    echo "export DISPLAY=:99" >> /entrypoint.sh && \
    echo "service tor start" >> /entrypoint.sh && \
    echo "python start.py" >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set entrypoint with GPU workarounds
CMD ["/bin/bash", "-c", "LIBGL_ALWAYS_SOFTWARE=1 __GLX_VENDOR_LIBRARY_NAME=mesa /entrypoint.sh"]