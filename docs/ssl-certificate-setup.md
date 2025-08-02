# SSL Certificate Setup Guide
# RSP Education Agent V2 - Phase 6 Production Deployment

## Overview

This guide provides comprehensive instructions for setting up SSL/TLS certificates for the RSP Education Agent V2 production environment. It covers multiple certificate authority options, automation, and best practices for security.

## 🔒 Certificate Options

### Option 1: Let's Encrypt (Free, Automated)

#### Prerequisites
- Domain name pointing to your server
- Ports 80 and 443 accessible
- Certbot installed

#### Installation
```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Or using Docker
docker run -it --rm --name certbot \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    certbot/certbot certonly --webroot -w /var/www/html -d yourdomain.com
```

#### Certificate Generation
```bash
# Generate certificate for your domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Or using standalone mode
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### Automated Renewal
```bash
# Add to crontab for automatic renewal
sudo crontab -e

# Add this line to renew certificates twice daily
0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook "docker-compose restart nginx"
```

#### Certificate Locations
```bash
# Let's Encrypt certificates are stored in:
/etc/letsencrypt/live/yourdomain.com/
├── cert.pem          # Certificate only
├── chain.pem         # Intermediate certificates
├── fullchain.pem     # Certificate + intermediates
└── privkey.pem       # Private key
```

### Option 2: Commercial CA (Paid, Extended Validation)

#### Certificate Signing Request (CSR) Generation
```bash
# Generate private key
openssl genrsa -out yourdomain.com.key 2048

# Generate CSR
openssl req -new -key yourdomain.com.key -out yourdomain.com.csr

# Provide information when prompted:
# Country Name: US
# State: Your State
# City: Your City
# Organization: Your Organization
# Organizational Unit: IT Department
# Common Name: yourdomain.com
# Email: admin@yourdomain.com
```

#### Submit CSR to CA
1. Purchase certificate from CA (DigiCert, GlobalSign, etc.)
2. Submit the CSR file during purchase
3. Complete domain validation process
4. Download issued certificate files

#### Certificate Installation
```bash
# Create certificate directory
mkdir -p /etc/ssl/certs/rsp-education
mkdir -p /etc/ssl/private/rsp-education

# Copy certificate files
cp yourdomain.com.crt /etc/ssl/certs/rsp-education/
cp yourdomain.com.key /etc/ssl/private/rsp-education/
cp intermediate.crt /etc/ssl/certs/rsp-education/

# Set proper permissions
chmod 644 /etc/ssl/certs/rsp-education/*
chmod 600 /etc/ssl/private/rsp-education/*
chown root:root /etc/ssl/certs/rsp-education/*
chown root:root /etc/ssl/private/rsp-education/*
```

### Option 3: Self-Signed Certificates (Development/Testing Only)

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Or using a configuration file
cat > ssl.conf << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = State
L = City
O = Organization
CN = yourdomain.com

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = yourdomain.com
DNS.2 = www.yourdomain.com
DNS.3 = api.yourdomain.com
EOF

# Generate certificate with config
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -config ssl.conf
```

## 🐳 Docker Integration

### Update Docker Compose
```yaml
# Add to docker-compose.prod.yml
services:
  nginx:
    volumes:
      - /etc/letsencrypt/live/yourdomain.com/fullchain.pem:/etc/nginx/ssl/cert.pem:ro
      - /etc/letsencrypt/live/yourdomain.com/privkey.pem:/etc/nginx/ssl/key.pem:ro
      # Or for commercial certificates:
      # - /etc/ssl/certs/rsp-education/yourdomain.com.crt:/etc/nginx/ssl/cert.pem:ro
      # - /etc/ssl/private/rsp-education/yourdomain.com.key:/etc/nginx/ssl/key.pem:ro
```

### Nginx SSL Configuration
Update the existing nginx configuration or create a new one:

```nginx
# /nginx/nginx.prod.conf SSL section
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate paths
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    
    # SSL optimization
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/nginx/ssl/chain.pem; # For Let's Encrypt
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Rest of your configuration...
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # ACME challenge for Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}
```

## 🔄 Certificate Renewal Automation

### Let's Encrypt Renewal Script
```bash
#!/bin/bash
# File: /scripts/renew-certificates.sh

set -e

echo "Starting certificate renewal process..."

# Renew certificates
certbot renew --quiet

# Check if renewal was successful
if [ $? -eq 0 ]; then
    echo "Certificate renewal successful"
    
    # Copy certificates to Docker volume location
    cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /docker/ssl/cert.pem
    cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /docker/ssl/key.pem
    
    # Restart Nginx to load new certificates
    docker-compose exec nginx nginx -s reload
    
    # Send success notification
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"SSL certificates renewed successfully"}' \
        $SLACK_WEBHOOK_URL
    
    echo "Certificate deployment completed"
else
    echo "Certificate renewal failed"
    # Send failure notification
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"SSL certificate renewal FAILED - immediate attention required"}' \
        $SLACK_WEBHOOK_URL
    exit 1
fi
```

### Systemd Timer for Renewal
```ini
# /etc/systemd/system/certbot-renewal.service
[Unit]
Description=Renew Let's Encrypt certificates
After=network.target

[Service]
Type=oneshot
ExecStart=/scripts/renew-certificates.sh
User=root

# /etc/systemd/system/certbot-renewal.timer
[Unit]
Description=Run certbot renewal twice daily
Requires=certbot-renewal.service

[Timer]
OnCalendar=*-*-* 00,12:00:00
RandomizedDelaySec=3h
Persistent=true

[Install]
WantedBy=timers.target
```

Enable the timer:
```bash
sudo systemctl enable certbot-renewal.timer
sudo systemctl start certbot-renewal.timer
```

## 📊 Certificate Monitoring

### Certificate Expiry Monitoring
```bash
#!/bin/bash
# File: /scripts/check-certificate-expiry.sh

DOMAIN="yourdomain.com"
CERT_FILE="/etc/letsencrypt/live/$DOMAIN/cert.pem"
WARNING_DAYS=30

# Check certificate expiry
if [ -f "$CERT_FILE" ]; then
    EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)
    EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_TIMESTAMP=$(date +%s)
    DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_TIMESTAMP - $CURRENT_TIMESTAMP) / 86400 ))
    
    echo "Certificate expires in $DAYS_UNTIL_EXPIRY days"
    
    if [ $DAYS_UNTIL_EXPIRY -lt $WARNING_DAYS ]; then
        echo "WARNING: Certificate expires soon!"
        # Send alert
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days\"}" \
            $SLACK_WEBHOOK_URL
    fi
else
    echo "Certificate file not found: $CERT_FILE"
    exit 1
fi
```

### Prometheus Metrics for Certificate Monitoring
```python
# Add to your FastAPI application
from prometheus_client import Gauge
import ssl
import socket
from datetime import datetime

ssl_cert_expiry = Gauge('ssl_certificate_expiry_days', 'Days until SSL certificate expires')

def check_ssl_expiry():
    try:
        context = ssl.create_default_context()
        with socket.create_connection(('yourdomain.com', 443)) as sock:
            with context.wrap_socket(sock, server_hostname='yourdomain.com') as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.now()).days
                ssl_cert_expiry.set(days_until_expiry)
                return days_until_expiry
    except Exception as e:
        print(f"Error checking SSL certificate: {e}")
        return -1

# Call this function periodically in your application
```

## 🔧 Testing and Validation

### SSL Configuration Testing
```bash
# Test SSL configuration with SSL Labs
curl -s "https://api.ssllabs.com/api/v3/analyze?host=yourdomain.com&publish=off" | jq '.'

# Test with testssl.sh
git clone https://github.com/drwetter/testssl.sh.git
cd testssl.sh
./testssl.sh yourdomain.com

# Test certificate chain
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com < /dev/null | openssl x509 -noout -dates

# Verify OCSP stapling
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com -status < /dev/null 2>&1 | grep -A 17 "OCSP response"
```

### Automated SSL Health Check
```bash
#!/bin/bash
# File: /scripts/ssl-health-check.sh

DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"

# Check if HTTPS is accessible
if curl -sf "https://$DOMAIN/health" > /dev/null; then
    echo "HTTPS endpoint is accessible"
else
    echo "ERROR: HTTPS endpoint is not accessible"
    # Send alert
    mail -s "SSL Health Check Failed" $EMAIL < /dev/null
    exit 1
fi

# Check certificate validity
CERT_INFO=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates)
echo "Certificate info: $CERT_INFO"

# Check if certificate is valid for the domain
CERT_SUBJECT=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -subject)
if echo "$CERT_SUBJECT" | grep -q "$DOMAIN"; then
    echo "Certificate is valid for domain $DOMAIN"
else
    echo "ERROR: Certificate is not valid for domain $DOMAIN"
    exit 1
fi

echo "SSL health check passed"
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### Certificate Not Loading
```bash
# Check file permissions
ls -la /etc/letsencrypt/live/yourdomain.com/
ls -la /etc/ssl/certs/rsp-education/

# Check Nginx configuration
nginx -t

# Check certificate validity
openssl x509 -in /path/to/cert.pem -text -noout

# Check if Nginx can access certificate files
docker-compose exec nginx ls -la /etc/nginx/ssl/
```

#### Mixed Content Issues
```javascript
// Force HTTPS in frontend
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
    location.replace('https:' + window.location.href.substring(window.location.protocol.length));
}
```

#### Certificate Chain Issues
```bash
# Verify certificate chain
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /path/to/cert.pem

# For Let's Encrypt, use fullchain.pem instead of cert.pem
ssl_certificate /etc/nginx/ssl/fullchain.pem;  # Not cert.pem
```

### Emergency Certificate Replacement
```bash
#!/bin/bash
# Emergency certificate replacement script

DOMAIN="yourdomain.com"
BACKUP_CERT="/backup/ssl/emergency-cert.pem"
BACKUP_KEY="/backup/ssl/emergency-key.pem"

echo "Replacing SSL certificate with emergency backup..."

# Stop services
docker-compose stop nginx

# Replace certificates
cp "$BACKUP_CERT" "/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
cp "$BACKUP_KEY" "/etc/letsencrypt/live/$DOMAIN/privkey.pem"

# Start services
docker-compose start nginx

# Verify
sleep 10
curl -f "https://$DOMAIN/health" && echo "Emergency certificate replacement successful"
```

## 📋 Security Best Practices

### SSL/TLS Configuration Checklist
- [ ] Use TLS 1.2 and 1.3 only
- [ ] Disable weak ciphers
- [ ] Enable HSTS with appropriate max-age
- [ ] Implement OCSP stapling
- [ ] Use proper certificate chain
- [ ] Set secure file permissions (600 for private keys)
- [ ] Regular certificate rotation
- [ ] Monitor certificate expiry
- [ ] Test SSL configuration regularly

### Security Headers
```nginx
# Additional security headers in Nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' wss:; media-src 'self'; object-src 'none'; child-src 'none'; form-action 'self'; base-uri 'self';" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

---

**Last Updated**: July 24, 2025
**Next Review**: October 24, 2025
**Document Owner**: DevOps Team