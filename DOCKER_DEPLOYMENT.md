# Docker Deployment Guide for Paragraph Analytics

## Overview
This guide explains how to deploy the Paragraph Analytics application using Docker and Docker Compose.

## Prerequisites
- Docker and Docker Compose installed
- Git repository cloned locally

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ramsharma2002/ParagraphAnalytics-.git
cd ParagraphAnalytics-
```

### 2. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### 3. Access the Application
- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Services

### Web Application
- **Port**: 8000
- **Framework**: Django with Gunicorn
- **Static Files**: Collected and served
- **Media Files**: Persistent volume

### Database
- **Type**: PostgreSQL 15
- **Port**: 5432
- **Credentials**: postgres/postgres
- **Data**: Persistent volume

### Redis
- **Version**: Redis 7 Alpine
- **Port**: 6379
- **Purpose**: Celery message broker

### Celery Services
- **Worker**: Processes background tasks
- **Beat**: Handles scheduled tasks

## Environment Variables

### Production Environment
Update these in `docker-compose.yml`:

```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-actual-secret-key
  - DATABASE_URL=postgresql://user:password@db:5432/dbname
  - CELERY_BROKER_URL=redis://redis:6379/0
  - CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Development Environment
For development, create a `.env` file:
```env
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://postgres:postgres@db:5432/paragraph_analytics
```

## Docker Commands

### Build Images
```bash
# Build web service only
docker-compose build web

# Build all services
docker-compose build
```

### Run Services
```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up web

# Run in background
docker-compose up -d
```

### Management Commands
```bash
# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Production Deployment

### 1. Update Environment Variables
```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-production-secret-key
  - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Configure Domain
Update `ALLOWED_HOSTS` in environment or settings.

### 3. SSL Certificate
Use a reverse proxy (Nginx) for SSL termination.

### 4. Backup Database
```bash
# Backup
docker-compose exec db pg_dump -U postgres paragraph_analytics > backup.sql

# Restore
docker-compose exec -T db psql -U postgres paragraph_analytics < backup.sql
```

## Troubleshooting

### Database Connection Issues
```bash
# Check database health
docker-compose ps db

# Restart database
docker-compose restart db

# View database logs
docker-compose logs db
```

### Static Files Not Loading
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Celery Issues
```bash
# Check Celery worker
docker-compose logs celery

# Restart Celery services
docker-compose restart celery celery-beat
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## Scaling

### Horizontal Scaling
```bash
# Scale web service
docker-compose up --scale web=3

# Scale Celery workers
docker-compose up --scale celery=2
```

### Load Balancing
Use Docker Swarm or Kubernetes for production scaling.

## Monitoring

### Health Checks
All services include health checks:
```bash
# Check service health
docker-compose ps
```

### Logs
```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f web
```

## Security

### Best Practices
1. Change default passwords
2. Use environment variables for secrets
3. Regularly update base images
4. Use non-root users in containers
5. Implement proper logging

### Network Security
```yaml
# Use custom networks
networks:
  app-network:
    driver: bridge
```

## Performance Optimization

### Database Optimization
- Add database indexes
- Use connection pooling
- Implement caching

### Application Optimization
- Use Redis for caching
- Optimize static file serving
- Implement CDN

## Development Workflow

### Local Development
```bash
# Start development environment
docker-compose up -d

# Make changes
# Rebuild and restart
docker-compose up --build web
```

### Testing
```bash
# Run tests in container
docker-compose exec web python manage.py test

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
```

## Support

For issues:
1. Check Docker logs: `docker-compose logs`
2. Verify service status: `docker-compose ps`
3. Check network connectivity
4. Review environment variables
