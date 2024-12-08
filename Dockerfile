# Base image
FROM codercom/code-server:latest

# Install Git and other necessary tools
RUN sudo apt-get update && sudo apt-get install -y \
    git \
    curl \
    wget \
    openssh-client \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /workspace

# Expose code-server's default port
EXPOSE 8080
