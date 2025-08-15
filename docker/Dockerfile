# Use Ubuntu 24.04 as base image
FROM ubuntu:24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV NODE_ENV=production
ENV NVM_DIR="/root/.nvm"
ENV PATH="/root/.nvm/versions/node/v24.6.0/bin:/root/.npm-global/bin:$PATH"

# Update package list and install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 24.x using nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash \
    && . "$HOME/.nvm/nvm.sh" \
    && nvm install 24 \
    && nvm use 24 \
    && nvm alias default 24

# Create app directory
WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY web/package*.json ./

# Install Node.js dependencies
RUN . "$HOME/.nvm/nvm.sh" && nvm use 24 && npm ci

# Copy Python requirements
COPY web/requirements.txt ./

# Create Python virtual environment and install dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire web application (excluding node_modules)
COPY web/ ./
RUN rm -rf node_modules package-lock.json

# Reinstall dependencies for Linux platform and build CSS
RUN . "$HOME/.nvm/nvm.sh" && nvm use 24 && npm install --include=dev && npx vite build

# Copy and make startup script executable
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Copy assets to static directory
# Needed for the logo because of the compiling process
RUN cp assets/*.png static/ 2>/dev/null || true

# Expose port 5000
EXPOSE 5000

# Set the default command to run the startup script
# I'm not sure if this is the best way to do this, but it works
CMD ["/start.sh"]
