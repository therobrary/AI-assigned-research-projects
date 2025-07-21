# Deploying Docker MCP Gateway & Servers: Complete Guide

## Table of Contents

1. [Introduction](#introduction)
2. [MCP Architecture Overview](#mcp-architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Installation and Setup](#installation-and-setup)
5. [Single Server Deployment](#single-server-deployment)
6. [Scaled Multi-Server Deployment](#scaled-multi-server-deployment)
7. [Networking and Security](#networking-and-security)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Client Connection Examples](#client-connection-examples)
10. [Troubleshooting FAQ](#troubleshooting-faq)
11. [Resources](#resources)

## Introduction

The Docker MCP (Managed Capabilities Platform) Gateway provides a secure, scalable infrastructure for delivering AI agent capabilities through containerized services. This guide demonstrates how to deploy and configure MCP Gateway with various server types (stout, SSE, and streamable HTTP) for both local and remote client connections.

### What You'll Learn

- Understanding MCP architecture and component relationships
- Setting up Docker-based MCP Gateway and servers
- Configuring authentication and security
- Scaling deployments with Docker Compose and orchestration
- Connecting clients to MCP services
- Monitoring and troubleshooting MCP deployments

### Use Cases

- **Local Development**: Single-server setup for development and testing
- **Production Deployment**: Multi-server setup with load balancing and scaling
- **Remote Access**: Secure external client connections
- **Microservices Architecture**: Distributed MCP services across infrastructure

## MCP Architecture Overview

The MCP platform consists of several key components that work together to provide AI capabilities:

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │    │   MCP Client    │    │   MCP Client    │
│   (Python)      │    │   (cURL/HTTP)   │    │   (JavaScript)  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼───────────────┐
                    │        MCP Gateway          │
                    │    (Load Balancer &         │
                    │     Authentication)         │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
    ┌─────▼─────┐           ┌─────▼─────┐           ┌─────▼─────┐
    │   Stout   │           │    SSE    │           │Streamable │
    │  Server   │           │  Server   │           │   HTTP    │
    │           │           │           │           │  Server   │
    └───────────┘           └───────────┘           └───────────┘
```

### Server Types

1. **Stout Server**: High-throughput request/response processing
2. **SSE Server**: Server-Sent Events for real-time streaming
3. **Streamable HTTP Server**: HTTP-based streaming for large data transfers

### MCP Gateway Features

- **Load Balancing**: Distributes requests across available servers
- **Authentication**: OAuth2, API key, and token-based security
- **SSL/TLS Termination**: Secure communication endpoints
- **Health Monitoring**: Server health checks and failover
- **Rate Limiting**: Request throttling and quota management

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 22.04 LTS (recommended) or compatible Linux distribution
- **Memory**: Minimum 4GB RAM (8GB+ recommended for production)
- **Storage**: At least 20GB available disk space
- **Network**: Open ports 80, 443, and custom MCP ports (8080-8083 by default)

### Required Software

Before proceeding, ensure the following software is installed:

#### Docker Engine

```bash
# Update package index
sudo apt update

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
```

#### Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Verification

```bash
# Test Docker installation
docker run hello-world

# Test Docker Compose
docker-compose --version
```

## Installation and Setup

### 1. Download MCP Images

The MCP Gateway and server images are available from Docker Hub:

```bash
# Pull MCP Gateway image
docker pull docker/mcp-gateway:latest

# Pull server images
docker pull docker/mcp-stout-server:latest
docker pull docker/mcp-sse-server:latest
docker pull docker/mcp-streamable-server:latest
```

### 2. Create Project Directory

```bash
# Create project directory
mkdir -p ~/mcp-deployment
cd ~/mcp-deployment

# Create subdirectories
mkdir -p {config,logs,data,ssl}
```

### 3. Environment Configuration

Create environment file from the provided template:

```bash
# Copy environment template
cp env.sample .env

# Edit configuration
nano .env
```

Configure the following variables in `.env`:

```bash
# MCP Gateway Configuration
MCP_GATEWAY_PORT=8080
MCP_GATEWAY_SSL_PORT=8443
MCP_DOMAIN=localhost

# Authentication
MCP_API_KEY=your-secure-api-key-here
MCP_JWT_SECRET=your-jwt-secret-key-here
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret

# Server Configuration
STOUT_SERVER_PORT=8081
SSE_SERVER_PORT=8082
STREAMABLE_SERVER_PORT=8083

# Database (if required)
POSTGRES_DB=mcp_db
POSTGRES_USER=mcp_user
POSTGRES_PASSWORD=secure-db-password

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

## Single Server Deployment

For development and testing, start with a single MCP Gateway and one stout server.

### Docker Compose Configuration

Use the provided `docker-compose.single.yml`:

```bash
# Deploy single server setup
docker-compose -f docker-compose.single.yml up -d

# Check status
docker-compose -f docker-compose.single.yml ps

# View logs
docker-compose -f docker-compose.single.yml logs -f
```

### Service Health Check

```bash
# Test MCP Gateway health
curl http://localhost:8080/health

# Test stout server connection
curl -H "Authorization: Bearer ${MCP_API_KEY}" \
     http://localhost:8080/api/v1/stout/health
```

### Basic Client Test

```bash
# Test with curl
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${MCP_API_KEY}" \
     -d '{"query": "Hello, MCP!", "max_tokens": 100}' \
     http://localhost:8080/api/v1/stout/generate
```

## Scaled Multi-Server Deployment

For production environments, deploy multiple servers with load balancing and auto-scaling.

### Multi-Server Architecture

```bash
# Deploy scaled setup
docker-compose -f docker-compose.scaled.yml up -d

# Scale individual services
docker-compose -f docker-compose.scaled.yml up -d --scale stout-server=3
docker-compose -f docker-compose.scaled.yml up -d --scale sse-server=2
```

### Load Balancing Configuration

The MCP Gateway automatically load balances between available servers:

- **Round Robin**: Default distribution method
- **Least Connections**: Routes to server with fewest active connections
- **Health-Based**: Excludes unhealthy servers from rotation

### Auto-Scaling Configuration

```yaml
# Add to docker-compose.scaled.yml
deploy:
  replicas: 3
  update_config:
    parallelism: 1
    delay: 10s
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

### Horizontal Pod Autoscaling (HPA)

For Kubernetes deployments:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mcp-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mcp-stout-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Networking and Security

### SSL/TLS Configuration

#### Generate SSL Certificates

```bash
# Create self-signed certificate for development
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/mcp-gateway.key \
    -out ssl/mcp-gateway.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set proper permissions
chmod 600 ssl/mcp-gateway.key
chmod 644 ssl/mcp-gateway.crt
```

#### Production SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/
sudo chown $USER:$USER ssl/*.pem
```

### Firewall Configuration

```bash
# Allow MCP Gateway ports
sudo ufw allow 8080/tcp
sudo ufw allow 8443/tcp

# Allow server ports (if accessed directly)
sudo ufw allow 8081:8083/tcp

# Enable firewall
sudo ufw --force enable

# Check status
sudo ufw status
```

### API Key Management

```bash
# Generate secure API key
export MCP_API_KEY=$(openssl rand -hex 32)

# Store in environment file
echo "MCP_API_KEY=${MCP_API_KEY}" >> .env
```

### OAuth2 Configuration

Configure OAuth2 for production environments:

```yaml
# Gateway OAuth configuration
oauth:
  provider: "auth0"  # or "keycloak", "okta"
  client_id: "${OAUTH_CLIENT_ID}"
  client_secret: "${OAUTH_CLIENT_SECRET}"
  redirect_uri: "https://your-domain.com/auth/callback"
  scopes: ["openid", "profile", "email"]
```

## Monitoring and Logging

### Docker Logs

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mcp-gateway
docker-compose logs -f stout-server

# Search logs
docker-compose logs | grep ERROR
```

### Log Configuration

Configure structured logging in `config/logging.yml`:

```yaml
version: 1
formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  json:
    format: '{"timestamp": "%(asctime)s", "service": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'

handlers:
  console:
    class: logging.StreamHandler
    formatter: json
  file:
    class: logging.FileHandler
    filename: /app/logs/mcp.log
    formatter: json

loggers:
  mcp:
    level: INFO
    handlers: [console, file]
  mcp.gateway:
    level: DEBUG
    handlers: [console, file]
```

### Health Checks

```bash
# Gateway health endpoint
curl http://localhost:8080/health

# Server health endpoints
curl http://localhost:8080/api/v1/stout/health
curl http://localhost:8080/api/v1/sse/health
curl http://localhost:8080/api/v1/streamable/health

# Detailed status
curl http://localhost:8080/api/v1/status
```

### Prometheus Metrics

Enable Prometheus metrics collection:

```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
```

### Grafana Dashboard

```yaml
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./config/grafana:/etc/grafana/provisioning
```

## Client Connection Examples

### Python Client Examples

#### Stout Server Client

See `examples/client_examples/python_stout_client.py` for a complete implementation.

Basic usage:

```python
import requests
import json

# Configure client
client = MCPStoutClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Generate response
response = client.generate("Hello, MCP!", max_tokens=100)
print(response)
```

#### SSE Client

See `examples/client_examples/python_sse_client.py` for streaming implementation.

#### Streamable HTTP Client

For large data transfers, use the streamable HTTP endpoint.

### cURL Examples

#### Basic Request

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${MCP_API_KEY}" \
     -d '{"query": "Explain quantum computing", "max_tokens": 500}' \
     http://localhost:8080/api/v1/stout/generate
```

#### Streaming Request

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${MCP_API_KEY}" \
     -d '{"query": "Write a story", "stream": true}' \
     http://localhost:8080/api/v1/sse/stream
```

### Authentication Examples

#### API Key Authentication

```bash
curl -H "Authorization: Bearer your-api-key" \
     http://localhost:8080/api/v1/health
```

#### OAuth2 Flow

```bash
# Step 1: Get authorization URL
curl "http://localhost:8080/auth/authorize?client_id=your-client-id&redirect_uri=http://localhost:3000/callback"

# Step 2: Exchange code for token
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"code": "auth-code", "client_id": "your-client-id", "client_secret": "your-secret"}' \
     http://localhost:8080/auth/token

# Step 3: Use access token
curl -H "Authorization: Bearer access-token" \
     http://localhost:8080/api/v1/health
```

## Troubleshooting FAQ

### Common Issues

#### Q: Gateway fails to start with "Port already in use" error

**A**: Check for conflicting services and change ports:

```bash
# Check port usage
sudo netstat -tulpn | grep :8080

# Kill conflicting process
sudo kill -9 <PID>

# Or change port in .env file
MCP_GATEWAY_PORT=8081
```

#### Q: Servers show as unhealthy in gateway status

**A**: Check server logs and network connectivity:

```bash
# Check server logs
docker-compose logs stout-server

# Test direct server connection
curl http://localhost:8081/health

# Restart servers
docker-compose restart stout-server
```

#### Q: Authentication fails with "Invalid API key" error

**A**: Verify API key configuration:

```bash
# Check environment variable
echo $MCP_API_KEY

# Verify key in .env file
grep MCP_API_KEY .env

# Test with correct key
curl -H "Authorization: Bearer correct-api-key" \
     http://localhost:8080/api/v1/health
```

#### Q: SSL/TLS certificate errors

**A**: Check certificate validity and configuration:

```bash
# Verify certificate
openssl x509 -in ssl/mcp-gateway.crt -text -noout

# Check certificate expiration
openssl x509 -in ssl/mcp-gateway.crt -checkend 86400

# Test SSL connection
openssl s_client -connect localhost:8443
```

#### Q: High memory usage or performance issues

**A**: Optimize resource allocation and scaling:

```bash
# Check resource usage
docker stats

# Increase memory limits
# Edit docker-compose.yml:
# mem_limit: 1g
# mem_reservation: 512m

# Scale servers
docker-compose up -d --scale stout-server=3
```

### Performance Optimization

1. **Resource Allocation**:
   - Allocate appropriate CPU and memory limits
   - Use memory-mapped files for large datasets
   - Implement connection pooling

2. **Caching**:
   - Enable Redis for response caching
   - Implement request deduplication
   - Use CDN for static assets

3. **Load Balancing**:
   - Configure sticky sessions for stateful operations
   - Implement health-based routing
   - Use multiple gateway instances

### Debugging Tips

1. **Enable Debug Logging**:
   ```bash
   # Set debug level in .env
   LOG_LEVEL=DEBUG
   ```

2. **Monitor Metrics**:
   ```bash
   # Check Prometheus metrics
   curl http://localhost:9090/metrics
   ```

3. **Trace Requests**:
   ```bash
   # Enable request tracing
   MCP_TRACE_REQUESTS=true
   ```

## Resources

### Official Documentation

- [Docker MCP Gateway Documentation](https://docs.docker.com/ai/mcp-gateway/)
- [MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- [Docker MCP Gateway Blog Post](https://www.docker.com/blog/docker-mcp-gateway-secure-infrastructure-for-agentic-ai/)

### Community Resources

- [Docker Community Forums](https://forums.docker.com/)
- [MCP GitHub Repository](https://github.com/docker/mcp)
- [Docker Discord Server](https://discord.gg/docker)

### API References

- [MCP Gateway API Documentation](https://docs.docker.com/ai/mcp-gateway/api/)
- [Server API Specifications](https://docs.docker.com/ai/mcp-servers/)

### Additional Tools

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Portainer](https://www.portainer.io/) - Docker management UI
- [Traefik](https://traefik.io/) - Advanced load balancing and SSL termination

---

*This guide is part of the AI-assigned research projects collection. For updates and additional resources, visit the [repository](https://github.com/therobrary/AI-assigned-research-projects).*