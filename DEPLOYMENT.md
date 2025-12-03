# SAGE Deployment Guide for Raspberry Pi

This guide covers deploying SAGE (Smart Autonomous General-purpose Engine) on Raspberry Pi devices.

## Hardware Requirements

### Minimum Requirements
- **Raspberry Pi 4 (4GB RAM)** or newer
- **32GB microSD card** (64GB+ recommended)
- **Active cooling** (fan or heatsink)
- **Stable power supply** (official Raspberry Pi PSU recommended)

### Recommended Configuration
- **Raspberry Pi 5 (8GB RAM)** for better performance
- **64GB+ microSD card** or SSD via USB 3.0
- **Active cooling solution**
- **Wired Ethernet connection** (for faster model downloads)

## Prerequisites

### 1. Install Docker and Docker Compose

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version
```

### 2. Optimize Raspberry Pi Settings

```bash
# Increase swap space (recommended for 4GB RAM models)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# Enable memory cgroup (required for Docker resource limits)
sudo nano /boot/firmware/cmdline.txt
# Add to end of line: cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1
sudo reboot
```

## Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sage.git
cd sage
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration (use nano or vim)
nano .env
```

**Important Settings for Raspberry Pi:**
- Set `OLLAMA_MODEL=tinyllama` for 4GB RAM
- Set `OLLAMA_MODEL=phi` for 8GB RAM
- Use `WHISPER_MODEL=tiny` or `base`
- Keep `WHISPER_DEVICE=cpu`

### 3. Build and Start Services

```bash
# Build the application (this may take 15-30 minutes on first run)
docker compose build

# Start all services
docker compose up -d

# Monitor logs
docker compose logs -f sage
```

### 4. Download AI Models

```bash
# Pull Ollama model (choose based on your RAM)
docker exec -it sage-ollama ollama pull tinyllama    # 1.1GB - for 4GB RAM
# OR
docker exec -it sage-ollama ollama pull phi          # 2.7GB - for 8GB RAM

# Verify model is loaded
docker exec -it sage-ollama ollama list
```

## Performance Optimization

### Resource Allocation

The docker-compose.yml is pre-configured with resource limits:
- **SAGE app**: 2GB RAM, 3 CPU cores max
- **Ollama**: 3GB RAM, 2.5 CPU cores max
- **PostgreSQL**: 512MB RAM, 1 CPU core max
- **ChromaDB**: 1GB RAM, 1 CPU core max

### Model Selection Guide

| Model | RAM Usage | Speed | Quality | Recommended For |
|-------|-----------|-------|---------|-----------------|
| tinyllama | ~1.5GB | Fast | Basic | Pi 4 (4GB) |
| phi | ~3GB | Medium | Good | Pi 4 (8GB), Pi 5 |
| mistral | ~4.5GB | Slow | Better | Pi 5 (8GB) only |
| llama2 | ~4GB | Slow | Good | Pi 5 (8GB) only |

### Whisper Model Sizes

| Model | RAM | Speed | Accuracy |
|-------|-----|-------|----------|
| tiny | ~400MB | Fast | Basic |
| base | ~700MB | Medium | Good |
| small | ~2.5GB | Slow | Better |

**Recommendation**: Use `tiny` for real-time applications, `base` for better accuracy.

## Monitoring

### Check Service Status

```bash
# View all services
docker compose ps

# Check resource usage
docker stats

# View logs for specific service
docker compose logs -f sage
docker compose logs -f ollama
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Ollama status
curl http://localhost:11434/api/tags

# ChromaDB status
curl http://localhost:8001/api/v1/heartbeat
```

## Troubleshooting

### Out of Memory Issues

1. **Reduce model sizes** in `.env`
2. **Stop unused services**:
   ```bash
   docker compose stop chromadb  # If not using vector storage
   ```
3. **Increase swap space** (see Prerequisites)
4. **Use lighter Ollama model** (tinyllama)

### Slow Performance

1. **Enable active cooling** - Pi will throttle when hot
2. **Use SSD instead of SD card** for better I/O
3. **Reduce concurrent requests** - set `MAX_WORKERS=1` in `.env`
4. **Close other applications** on the Pi

### Build Failures

```bash
# Clean rebuild
docker compose down -v
docker system prune -a
docker compose build --no-cache
```

### Port Conflicts

If ports are already in use, edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to another port
```

## Maintenance

### Update Application

```bash
git pull
docker compose down
docker compose build
docker compose up -d
```

### Backup Data

```bash
# Backup volumes
docker run --rm -v sage_postgres-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz -C /data .

docker run --rm -v sage_chroma-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/chroma-backup.tar.gz -C /data .
```

### Clean Up

```bash
# Remove unused images and containers
docker system prune -a

# Remove all SAGE data (WARNING: destructive)
docker compose down -v
```

## Expected Performance

### Raspberry Pi 4 (4GB)
- **Model load time**: 30-60 seconds (tinyllama)
- **Inference speed**: 2-5 tokens/second
- **STT processing**: 0.5x-1x realtime (tiny model)
- **API response time**: 200-500ms

### Raspberry Pi 5 (8GB)
- **Model load time**: 20-40 seconds (phi/mistral)
- **Inference speed**: 5-10 tokens/second
- **STT processing**: 1x-2x realtime (base model)
- **API response time**: 100-300ms

## Security Considerations

1. **Change default passwords** in `.env` and `docker-compose.yml`
2. **Use firewall** to restrict access:
   ```bash
   sudo ufw allow 8000/tcp  # SAGE API only
   sudo ufw enable
   ```
3. **Keep system updated**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
4. **Use HTTPS** in production (consider nginx reverse proxy)

## Additional Resources

- [Ollama Models](https://ollama.ai/library)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Docker on ARM](https://docs.docker.com/engine/install/debian/)

## Support

For issues specific to Raspberry Pi deployment, check:
1. System temperature: `vcgencmd measure_temp`
2. Memory usage: `free -h`
3. Docker logs: `docker compose logs`
4. System logs: `journalctl -xe`
