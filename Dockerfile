# MCP Server Sensory - Docker Image
# Multi-Sensory AI Communication: Morse, Braille, SSTV/REFLUX
#
# Build: docker build -t mcp-server-sensory .
# Run:   docker run -i mcp-server-sensory
#
# Part of HumoticaOS - https://humotica.com

FROM python:3.11-slim

LABEL maintainer="Jasper van de Meent <info@humotica.com>"
LABEL org.opencontainers.image.source="https://github.com/jaspertvdm/mcp-server-sensory"
LABEL org.opencontainers.image.description="Multi-Sensory AI Communication for Off-Grid Networks"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install from PyPI
RUN pip install --no-cache-dir mcp-server-sensory

# MCP servers communicate via stdio
ENTRYPOINT ["python", "-m", "mcp_server_sensory"]
