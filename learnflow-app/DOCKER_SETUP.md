# 🐳 LearnFlow Docker Setup Guide

This guide explains how to set up and run the LearnFlow application using Docker containers.

## 📋 Prerequisites

- Docker Desktop installed and running
- At least 4GB RAM available
- Sufficient disk space for containers

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd learnflow-app
```

### 2. Create Environment Files
Copy the example environment files and update with your values:

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your values

# Frontend
cp frontend/.env.example frontend/.env.local
# Edit frontend/.env.local with your values
```

### 3. Start All Services
```bash
docker-compose up -d
```

### 4. Check Service Status
```bash
docker-compose ps
```

### 5. Access the Applications
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Backend API Docs: `http://localhost:8000/docs`

## 🔧 Service Details

### Database (PostgreSQL)
- Port: 5432
- Database: `learnflow`
- User: `postgres`
- Password: `secretpassword`

### Message Queue (Kafka)
- Port: 9092
- Zookeeper: 2181

### Cache (Redis)
- Port: 6379

### Backend API
- Port: 8000
- Framework: FastAPI

### Frontend
- Port: 3000
- Framework: Next.js

## 🛠️ Management Commands

### Start Services
```bash
# Start all services in detached mode
docker-compose up -d

# Start with rebuild
docker-compose up -d --build
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs
```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

### Scale Services
```bash
# Scale backend to 2 instances
docker-compose up -d --scale backend=2
```

## 🧪 Development Mode

For development, the containers are configured to mount local code:

- Backend code changes reflect immediately
- Frontend code changes reflect immediately
- Live reloading is enabled

## 🚨 Troubleshooting

### Common Issues

**Issue**: Ports already in use
**Solution**: Check if other services are using ports 3000, 8000, 5432, 9092

**Issue**: Out of memory
**Solution**: Ensure at least 4GB RAM is available to Docker

**Issue**: Dependency installation fails
**Solution**: Check internet connection and retry with `--build` flag

**Issue**: Database connection fails
**Solution**: Wait for PostgreSQL to be healthy before starting backend

### Health Checks
```bash
# Check service health
docker-compose ps

# Check specific container logs
docker logs learnflow-postgres
docker logs learnflow-kafka
docker logs learnflow-backend
```

## 🚀 Production Considerations

### Environment Variables
Update the .env files with production values:
- Strong passwords and secrets
- Production database URLs
- Security settings
- Monitoring configurations

### Resource Limits
Consider adding resource limits in production:
```yaml
services:
  backend:
    # ... other config
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

### Security
- Use secrets for sensitive data
- Enable authentication
- Set up HTTPS/SSL
- Regular security updates

## 📊 Performance Tuning

### Docker Desktop Settings
- Allocate sufficient memory (recommended: 4GB+)
- Enable experimental features if needed
- Configure disk space appropriately

### Container Optimization
- Use multi-stage builds
- Minimize image sizes
- Use .dockerignore files
- Optimize layer caching

## 🔄 Updates and Maintenance

### Update Dependencies
```bash
# Rebuild with updated dependencies
docker-compose build --no-cache
docker-compose up -d
```

### Backup Database
```bash
# Backup PostgreSQL data
docker exec learnflow-postgres pg_dump -U postgres learnflow > backup.sql
```

### Restore Database
```bash
# Restore PostgreSQL data
docker exec -i learnflow-postgres psql -U postgres -d learnflow < backup.sql
```

## 🏁 Stopping and Cleanup

### Graceful Shutdown
```bash
# Stop all services
docker-compose down

# Remove all containers, networks, and volumes
docker-compose down -v --remove-orphans
```

---

## 🎯 Ready to Go!

Your LearnFlow application is now running in Docker containers. The system is production-ready and optimized for 4GB RAM systems.

**Happy Learning!** 🎓