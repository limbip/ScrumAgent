FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Rename the custom configuration file if it exists
RUN if [ -f /app/config/taiga_discord_maps.yaml.limbip ]; then \
    mv /app/config/taiga_discord_maps.yaml.limbip /app/config/taiga_discord_maps.yaml; \
    fi

# Create a script to start Ollama and the application
RUN echo '#!/bin/bash\n\
echo "Installing Ollama..."\n\
curl -fsSL https://ollama.com/install.sh | sh\n\
echo "Starting Ollama service..."\n\
ollama serve &\n\
echo "Waiting for Ollama to start..."\n\
sleep 10\n\
echo "Pulling Ollama models..."\n\
ollama pull deepseek-r1:8b || echo "Warning: Failed to pull deepseek-r1:8b, continuing..."\n\
ollama pull llama3.2-vision:11b || echo "Warning: Failed to pull llama3.2-vision:11b, continuing..."\n\
echo "Starting ScrumAgent..."\n\
exec python -m scrumagent.main_discord_bot\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set environment variable to indicate we're in Docker
ENV RUNNING_IN_DOCKER=true

# Start the application using the script
CMD ["/app/start.sh"]
