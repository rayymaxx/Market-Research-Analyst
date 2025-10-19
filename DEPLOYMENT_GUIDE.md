# Market Research AI - Deployment Guide

## Production Deployment

### Prerequisites
- **Server**: Linux/Ubuntu 20.04+ or similar
- **Python**: 3.12+
- **Node.js**: 18+
- **Domain**: Optional but recommended
- **SSL Certificate**: For HTTPS (Let's Encrypt recommended)

## Backend Deployment

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.12 python3.12-venv python3-pip nginx -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Application Setup
```bash
# Clone repository
git clone <your-repo-url>
cd Market-Research-Analyst

# Backend setup
cd marketresearch
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Environment configuration
cp .env.example .env
nano .env  # Add your API keys and configuration
```

### 3. Environment Variables (.env)
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Optional
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 4. Systemd Service (Backend)
```bash
# Create service file
sudo nano /etc/systemd/system/market-research-api.service
```

```ini
[Unit]
Description=Market Research AI API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Market-Research-Analyst/marketresearch/api
Environment=PATH=/path/to/Market-Research-Analyst/marketresearch/venv/bin
ExecStart=/path/to/Market-Research-Analyst/marketresearch/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable market-research-api
sudo systemctl start market-research-api
sudo systemctl status market-research-api
```

## Frontend Deployment

### 1. Build Frontend
```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 2. Nginx Configuration
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/market-research-ai
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Frontend
    location / {
        root /path/to/Market-Research-Analyst/frontend/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    
    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        root /path/to/Market-Research-Analyst/frontend/build;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/market-research-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker Deployment (Alternative)

### 1. Backend Dockerfile
```dockerfile
# marketresearch/Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
WORKDIR /app/api

EXPOSE 8000
CMD ["python", "run.py"]
```

### 2. Frontend Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./marketresearch
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    volumes:
      - ./marketresearch/knowledge:/app/knowledge
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

```bash
# Deploy with Docker
docker-compose up -d
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Setup
```bash
# Launch EC2 instance (t3.medium recommended)
# Security groups: HTTP (80), HTTPS (443), SSH (22)
# Use Ubuntu 20.04 LTS AMI
```

#### 2. Application Load Balancer
```bash
# Create ALB with:
# - Target groups for frontend (port 80) and backend (port 8000)
# - Health checks on /health endpoint
# - SSL certificate from ACM
```

#### 3. RDS (Optional)
```bash
# For persistent storage:
# - PostgreSQL instance
# - Update backend to use database instead of localStorage
```

### Google Cloud Platform

#### 1. Compute Engine
```bash
# Create VM instance
gcloud compute instances create market-research-ai \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-medium \
    --tags=http-server,https-server
```

#### 2. Cloud Run (Serverless)
```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT-ID/market-research-api ./marketresearch
gcloud run deploy --image gcr.io/PROJECT-ID/market-research-api --platform managed

# Deploy frontend to Cloud Storage + CDN
gsutil -m cp -r ./frontend/build/* gs://your-bucket-name/
```

### DigitalOcean Droplet

#### 1. Create Droplet
```bash
# Ubuntu 20.04, 2GB RAM minimum
# Add SSH key for secure access
```

#### 2. One-Click Apps
```bash
# Use Docker one-click app
# Or LAMP stack for traditional deployment
```

## Monitoring & Maintenance

### 1. Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend availability
curl http://localhost/

# Service status
sudo systemctl status market-research-api
sudo systemctl status nginx
```

### 2. Logging
```bash
# Backend logs
sudo journalctl -u market-research-api -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Backup Strategy
```bash
# Knowledge base backup
tar -czf knowledge-backup-$(date +%Y%m%d).tar.gz ./marketresearch/knowledge/

# Database backup (if using)
pg_dump market_research > backup-$(date +%Y%m%d).sql
```

### 4. Updates
```bash
# Pull latest changes
git pull origin main

# Update backend
cd marketresearch
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart market-research-api

# Update frontend
cd frontend
npm install
npm run build
sudo systemctl restart nginx
```

## Security Considerations

### 1. Firewall Setup
```bash
# UFW configuration
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. API Security
- Use strong JWT secrets
- Implement rate limiting
- Enable CORS properly
- Validate all inputs
- Use HTTPS only

### 3. File Upload Security
- Validate file types
- Scan for malware
- Limit file sizes
- Sanitize filenames

## Performance Optimization

### 1. Backend Optimization
- Use Redis for caching
- Implement connection pooling
- Enable gzip compression
- Use async/await patterns

### 2. Frontend Optimization
- Enable Nginx gzip
- Set proper cache headers
- Use CDN for static assets
- Implement lazy loading

### 3. Database Optimization
- Use connection pooling
- Implement proper indexing
- Regular maintenance tasks
- Monitor query performance

## Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports 80, 443, 8000 are available
2. **Permission errors**: Ensure proper file permissions
3. **SSL issues**: Verify certificate installation
4. **API connectivity**: Check firewall and proxy settings

### Debug Commands
```bash
# Check service status
sudo systemctl status market-research-api nginx

# View logs
sudo journalctl -u market-research-api --since "1 hour ago"

# Test connectivity
curl -I http://localhost:8000/health
curl -I http://localhost/

# Check ports
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80
```

---

For production support, ensure you have monitoring, backups, and update procedures in place.