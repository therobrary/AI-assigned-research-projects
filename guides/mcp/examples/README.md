# MCP Docker Examples

This directory contains complete examples for deploying and using Docker MCP Gateway & Servers.

## Quick Start

1. **Copy environment template:**
   ```bash
   cp env.sample .env
   ```

2. **Edit configuration:**
   ```bash
   nano .env
   # Update API keys, passwords, and other settings
   ```

3. **Start single server deployment:**
   ```bash
   docker-compose -f docker-compose.single.yml up -d
   ```

4. **Test the deployment:**
   ```bash
   curl http://localhost:8080/health
   ```

## Files Overview

### Docker Compose Files

- **`docker-compose.single.yml`** - Single MCP Gateway + one stout server
  - Ideal for development and testing
  - Minimal resource requirements
  - Quick setup and teardown

- **`docker-compose.scaled.yml`** - Production-ready multi-server setup
  - MCP Gateway with load balancing
  - Multiple server types (stout, SSE, streamable)
  - Redis caching and PostgreSQL storage
  - Prometheus monitoring and Grafana dashboards

### Configuration Files

- **`env.sample`** - Environment variables template
  - Copy to `.env` and customize
  - Includes all configuration options
  - Security guidelines and best practices

### Client Examples

- **`client_examples/`** - Client implementation examples
  - Python stout client (synchronous)
  - Python SSE client (asynchronous streaming)
  - Shell script for streamable HTTP
  - Comprehensive error handling and documentation

## Deployment Scenarios

### Development Environment

For local development and testing:

```bash
# Single server setup
docker-compose -f docker-compose.single.yml up -d

# Check status
docker-compose -f docker-compose.single.yml ps

# View logs
docker-compose -f docker-compose.single.yml logs -f
```

### Production Environment

For production deployments with high availability:

```bash
# Multi-server setup
docker-compose -f docker-compose.scaled.yml up -d

# Scale specific services
docker-compose -f docker-compose.scaled.yml up -d --scale stout-server=5

# Monitor health
curl http://localhost:8080/api/v1/status
```

### Staging Environment

For staging with production-like setup but reduced resources:

```bash
# Start with fewer replicas
docker-compose -f docker-compose.scaled.yml up -d --scale stout-server=2 --scale sse-server=1
```

## Configuration Examples

### Basic Configuration

Minimal `.env` setup for development:

```env
MCP_API_KEY=dev-api-key-12345
MCP_DOMAIN=localhost
LOG_LEVEL=INFO
POSTGRES_PASSWORD=dev-password
```

### Production Configuration

Security-hardened `.env` for production:

```env
MCP_API_KEY=prod-secure-key-32-chars-hex
MCP_DOMAIN=mcp.yourdomain.com
MCP_GATEWAY_SSL_PORT=443
LOG_LEVEL=WARNING
POSTGRES_PASSWORD=very-secure-production-password
SSL_CERT_PATH=./ssl/production.crt
SSL_KEY_PATH=./ssl/production.key
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
```

## Scaling Examples

### Horizontal Scaling

```bash
# Scale stout servers to handle more requests
docker-compose -f docker-compose.scaled.yml up -d --scale stout-server=10

# Scale SSE servers for more concurrent streams
docker-compose -f docker-compose.scaled.yml up -d --scale sse-server=5

# Scale streamable servers for large file processing
docker-compose -f docker-compose.scaled.yml up -d --scale streamable-server=3
```

### Resource Scaling

Edit `docker-compose.scaled.yml` to adjust resource limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'        # Increase CPU limit
      memory: 4G         # Increase memory limit
    reservations:
      cpus: '1.0'
      memory: 2G
```

## Monitoring Examples

### Health Checks

```bash
# Gateway health
curl http://localhost:8080/health

# Individual server health
curl http://localhost:8080/api/v1/stout/health
curl http://localhost:8080/api/v1/sse/health
curl http://localhost:8080/api/v1/streamable/health

# Detailed status
curl http://localhost:8080/api/v1/status
```

### Metrics and Monitoring

Access monitoring dashboards:

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

View metrics endpoints:

```bash
# Gateway metrics
curl http://localhost:8080/metrics

# Prometheus metrics
curl http://localhost:9090/api/v1/query?query=up
```

### Log Monitoring

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mcp-gateway

# Follow logs with filtering
docker-compose logs -f | grep ERROR

# Structured log analysis
docker-compose logs --no-color | jq '.'
```

## Security Examples

### SSL/TLS Setup

Generate development certificates:

```bash
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/mcp-gateway.key \
    -out ssl/mcp-gateway.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

### API Key Management

Generate secure API keys:

```bash
# Generate 32-character hex key
openssl rand -hex 32

# Generate base64 key
openssl rand -base64 32

# Store in environment
echo "MCP_API_KEY=$(openssl rand -hex 32)" >> .env
```

### Network Security

Configure firewall rules:

```bash
# Allow MCP ports
sudo ufw allow 8080/tcp
sudo ufw allow 8443/tcp

# Restrict access to specific IPs
sudo ufw allow from 192.168.1.0/24 to any port 8080

# Enable firewall
sudo ufw --force enable
```

## Backup and Recovery

### Data Backup

```bash
# Backup PostgreSQL data
docker-compose exec postgres pg_dump -U mcp_user mcp_db > backup.sql

# Backup Redis data
docker-compose exec redis redis-cli --rdb backup.rdb

# Backup configuration files
tar -czf config-backup.tar.gz config/ ssl/ .env
```

### Data Recovery

```bash
# Restore PostgreSQL
docker-compose exec -T postgres psql -U mcp_user mcp_db < backup.sql

# Restore Redis
docker-compose exec -T redis redis-cli --pipe < backup.rdb
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check port usage
   sudo netstat -tulpn | grep :8080
   
   # Change ports in .env
   MCP_GATEWAY_PORT=8081
   ```

2. **Permission errors:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER data/ logs/ ssl/
   chmod 600 ssl/*.key
   ```

3. **Memory issues:**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase memory limits in docker-compose.yml
   ```

### Debug Mode

Enable debug logging:

```env
LOG_LEVEL=DEBUG
DEBUG_MODE=true
TRACE_REQUESTS=true
```

### Performance Tuning

Optimize for your workload:

```env
# High-throughput settings
STOUT_MAX_WORKERS=16
GATEWAY_MAX_CONNECTIONS=2000
RATE_LIMIT_REQUESTS_PER_MINUTE=5000

# Memory optimization
REDIS_MEMORY_LIMIT=1g
POSTGRES_MEMORY_LIMIT=2g
```

## Best Practices

1. **Environment Separation**: Use different `.env` files for dev/staging/prod
2. **Secret Management**: Never commit secrets to version control
3. **Health Monitoring**: Implement comprehensive health checks
4. **Log Management**: Use structured logging and log rotation
5. **Backup Strategy**: Regular automated backups of data and configuration
6. **Security Updates**: Keep Docker images and dependencies updated
7. **Resource Monitoring**: Monitor CPU, memory, and disk usage
8. **Network Security**: Use firewalls and VPNs in production

## Support

For issues and questions:

1. Check the main guide: `../docker-mcp-guide.md`
2. Review client examples: `client_examples/README.md`
3. Examine Docker Compose logs: `docker-compose logs`
4. Test with health endpoints: `curl http://localhost:8080/health`