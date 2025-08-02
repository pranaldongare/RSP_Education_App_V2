# Production Deployment Guide
# RSP Education Agent V2 - Phase 6 Complete Production Deployment

## 🚀 Overview

This comprehensive guide provides step-by-step instructions for deploying the RSP Education Agent V2 to production. The deployment includes all 7 AI agents, Flutter frontend, and enterprise-grade infrastructure with monitoring, security, and backup systems.

## 📋 Prerequisites

### System Requirements
- **CPU**: Minimum 4 cores, Recommended 8+ cores
- **RAM**: Minimum 16GB, Recommended 32GB+
- **Storage**: Minimum 100GB SSD, Recommended 500GB+ SSD
- **Network**: Reliable internet connection with static IP
- **OS**: Ubuntu 20.04 LTS or newer (recommended)

### Software Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional tools
sudo apt install -y git curl wget unzip nginx-common openssl
```

### Domain and DNS Setup
1. Register domain name (e.g., `yourdomain.com`)
2. Configure DNS A records:
   ```
   @ -> YOUR_SERVER_IP
   www -> YOUR_SERVER_IP
   api -> YOUR_SERVER_IP
   ```
3. Configure CNAME records (optional):
   ```
   monitoring -> YOUR_DOMAIN
   grafana -> YOUR_DOMAIN
   ```

## 🔧 Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/RSP_Education_App_V2.git
cd RSP_Education_App_V2
```

### 2. Configure Environment Variables
```bash
# Copy production environment template
cp .env.production .env

# Edit environment variables (CRITICAL - Change all default passwords)
nano .env

# Required changes:
# - POSTGRES_PASSWORD: Strong password for PostgreSQL
# - REDIS_PASSWORD: Strong password for Redis
# - SECRET_KEY: 32+ character random string
# - API keys: Your actual AI service API keys
# - DOMAIN: Your actual domain name
# - EMAIL settings: Your SMTP configuration
```

### 3. Generate SSL Certificates
```bash
# Option A: Let's Encrypt (Free, Automated)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Option B: Commercial Certificate (Follow SSL setup guide)
# See docs/ssl-certificate-setup.md for detailed instructions

# Update docker-compose.prod.yml with certificate paths
```

### 4. Configure Nginx
```bash
# Update nginx configuration with your domain
nano nginx/nginx.prod.conf

# Replace 'your-domain.com' with your actual domain
sed -i 's/your-domain.com/yourdomain.com/g' nginx/nginx.prod.conf
```

## 📊 Database Setup

### 1. Initialize Database Schema
```bash
# Start only the database service first
docker-compose -f docker-compose.prod.yml up -d postgres redis

# Wait for services to be ready
sleep 30

# Run database migrations
docker-compose -f docker-compose.prod.yml exec postgres psql -U rsp_user -d rsp_education -c "SELECT version();"

# Initialize database schema (will be done automatically by backend)
```

### 2. Verify Database Connection
```bash
# Test database connectivity
docker-compose -f docker-compose.prod.yml exec postgres psql -U rsp_user -d rsp_education -c "\dt"
```

## 🔄 Application Deployment

### 1. Build and Deploy Services
```bash
# Build backend Docker image
docker-compose -f docker-compose.prod.yml build backend

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 2. Verify Deployment
```bash
# Check service logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs nginx

# Test API endpoints
curl -f http://localhost/health
curl -f http://localhost/api/v1/
```

### 3. Run Integration Tests
```bash
# Execute API integration tests
cd backend
python test_api_integration.py

# Check test results
cat api_integration_test_results.json
```

## 🎯 Flutter Frontend Deployment

### 1. Build Flutter Web Application
```bash
cd frontend

# Install dependencies
flutter pub get

# Build for production
flutter build web --release --web-renderer html

# Copy build to Nginx directory
sudo cp -r build/web/* /usr/share/nginx/html/
```

### 2. Configure Flutter for Production
```dart
// Update lib/core/constants/api_constants.dart
class ApiConstants {
  static const String baseUrl = 'https://yourdomain.com/api/v1';
  static const String wsUrl = 'wss://yourdomain.com/ws';
  static const Duration timeout = Duration(seconds: 30);
}
```

## 📈 Monitoring Setup

### 1. Enable Monitoring Stack
```bash
# Start monitoring services
docker-compose -f docker-compose.prod.yml --profile monitoring up -d

# Verify Prometheus
curl http://localhost:9090/targets

# Verify Grafana
# Access http://localhost:3000
# Login: admin / [GRAFANA_PASSWORD from .env]
```

### 2. Import Grafana Dashboards
```bash
# Import RSP Education dashboard
curl -X POST \
  http://localhost:3000/api/dashboards/db \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_GRAFANA_API_KEY' \
  -d @monitoring/grafana/dashboards/rsp-education-dashboard.json
```

## 🔒 Security Configuration

### 1. Firewall Setup
```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Optional: Allow monitoring ports (restrict to admin IPs)
sudo ufw allow from YOUR_ADMIN_IP to any port 3000  # Grafana
sudo ufw allow from YOUR_ADMIN_IP to any port 9090  # Prometheus
```

### 2. SSL/TLS Hardening
```bash
# Test SSL configuration
curl -I https://yourdomain.com

# Check SSL Labs rating
curl -s "https://api.ssllabs.com/api/v3/analyze?host=yourdomain.com"
```

### 3. Security Headers Verification
```bash
# Verify security headers
curl -I https://yourdomain.com | grep -i "strict-transport-security\|x-frame-options\|x-content-type-options"
```

## 💾 Backup Configuration

### 1. Setup Automated Backups
```bash
# Create backup directories
sudo mkdir -p /backups/{db,redis,app,images}
sudo chown -R $USER:$USER /backups

# Setup backup scripts
chmod +x scripts/automated_backup.sh
chmod +x scripts/automated_recovery.sh

# Configure cron jobs
crontab -e

# Add backup schedule (daily at 2 AM)
0 2 * * * /path/to/RSP_Education_App_V2/scripts/automated_backup.sh
```

### 2. Test Backup and Recovery
```bash
# Test backup
./scripts/automated_backup.sh

# Test recovery (in staging environment)
./scripts/automated_recovery.sh latest
```

## 📱 Mobile App Deployment (Android)

### 1. Build Android APK
```bash
cd frontend

# Build Android APK
flutter build apk --release

# Build Android App Bundle (for Play Store)
flutter build appbundle --release
```

### 2. Configure App Signing
```bash
# Generate signing key
keytool -genkey -v -keystore ~/rsp-education-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias rsp-education

# Configure signing in android/app/build.gradle
```

## 🚦 Health Checks and Monitoring

### 1. Setup Health Check Endpoints
```bash
# Verify all health checks
curl https://yourdomain.com/health
curl https://yourdomain.com/api/v1/agents/health
curl https://yourdomain.com/api/v1/agents/status/all
```

### 2. Configure Uptime Monitoring
```bash
# External monitoring services (configure as needed)
# - UptimeRobot
# - Pingdom  
# - StatusCake
# - AWS CloudWatch (if using AWS)
```

## 🔄 Load Balancing (High Availability)

### Optional: Multiple Backend Instances
```yaml
# docker-compose.prod.yml - Scale backend
services:
  backend:
    # ... existing config
    deploy:
      replicas: 3
      
  backend-lb:
    image: nginx:alpine
    volumes:
      - ./nginx/load-balancer.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

## 📊 Performance Optimization

### 1. Database Optimization
```sql
-- Connect to PostgreSQL and run performance optimizations
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM students WHERE grade = '5';

-- Create necessary indexes
CREATE INDEX idx_student_activity_date ON session_activities(started_at);
CREATE INDEX idx_assessment_student_subject ON assessments(student_id, subject);

-- Update table statistics
ANALYZE;
```

### 2. Redis Configuration
```bash
# Optimize Redis configuration
docker-compose exec redis redis-cli CONFIG SET maxmemory 2gb
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### 3. Nginx Optimization
```nginx
# Already optimized in nginx.prod.conf
# - Gzip compression enabled
# - Static file caching
# - Connection pooling
# - Rate limiting
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Domain name configured and DNS propagated
- [ ] SSL certificates generated and configured
- [ ] Environment variables configured with strong passwords
- [ ] Firewall rules configured
- [ ] Backup storage (S3/equivalent) configured
- [ ] Email/notification services configured
- [ ] API keys for AI services obtained

### Deployment
- [ ] Repository cloned and configured
- [ ] Docker services built successfully
- [ ] Database initialized and migrations applied
- [ ] All services started and health checks passing
- [ ] Integration tests completed successfully
- [ ] Frontend built and deployed
- [ ] SSL/HTTPS working correctly
- [ ] Monitoring stack deployed and configured

### Post-Deployment
- [ ] Backup system tested
- [ ] Recovery procedures tested
- [ ] Performance benchmarks recorded
- [ ] Security scan completed
- [ ] Load testing performed
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Support procedures established

## 🚨 Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check Docker logs
docker-compose -f docker-compose.prod.yml logs

# Check system resources
free -h
df -h
docker system df
```

#### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose -f docker-compose.prod.yml logs postgres

# Verify database credentials
docker-compose -f docker-compose.prod.yml exec postgres psql -U rsp_user -d rsp_education -c "SELECT 1;"
```

#### SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem -noout -dates

# Test SSL configuration
curl -vI https://yourdomain.com
```

#### High Resource Usage
```bash
# Monitor system resources
htop
docker stats

# Check disk usage
du -sh /var/lib/docker/
docker system prune -a
```

## 📞 Support and Maintenance

### Regular Maintenance Tasks
- **Daily**: Check system health, review logs
- **Weekly**: Update system packages, review metrics
- **Monthly**: Security updates, backup testing
- **Quarterly**: Performance review, capacity planning

### Emergency Contacts
- System Administrator: [Your contact]
- Database Administrator: [Your contact]
- DevOps Team: [Your contact]
- Management: [Your contact]

### Documentation Updates
- Update this guide after any configuration changes
- Maintain runbooks for common procedures
- Keep architecture diagrams current
- Document any custom modifications

## 🎉 Deployment Complete

Congratulations! You have successfully deployed the RSP Education Agent V2 production system. The platform now includes:

✅ **7 AI Agents**: Content Generation, Assessment, Adaptive Learning, Engagement, Analytics, Learning Coordinator, Voice Interaction
✅ **Full-Stack Architecture**: FastAPI backend + Flutter frontend
✅ **Production Database**: PostgreSQL with optimized schema
✅ **Enterprise Security**: SSL/TLS, security headers, rate limiting
✅ **Monitoring & Alerting**: Prometheus + Grafana
✅ **Backup & Recovery**: Automated backup with disaster recovery procedures
✅ **Scalable Infrastructure**: Docker-based container orchestration

Your intelligent tutoring platform is now ready to serve students with personalized CBSE education powered by advanced AI agents!

---

**Last Updated**: July 24, 2025
**Version**: 2.0.0
**Document Owner**: DevOps Team