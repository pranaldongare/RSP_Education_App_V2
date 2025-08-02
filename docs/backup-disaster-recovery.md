# Backup and Disaster Recovery Strategy
# RSP Education Agent V2 - Phase 6 Production Deployment

## Overview

This document outlines the comprehensive backup and disaster recovery (BDR) strategy for the RSP Education Agent V2 production environment. The strategy ensures business continuity, data protection, and rapid recovery from various failure scenarios.

## 🎯 Recovery Time and Point Objectives

- **Recovery Time Objective (RTO)**: 4 hours maximum downtime
- **Recovery Point Objective (RPO)**: Maximum 1 hour of data loss
- **Availability Target**: 99.9% uptime (8.76 hours downtime per year)

## 🗄️ Data Classification and Backup Requirements

### Critical Data (RPO: 15 minutes)
- Student profiles and learning progress
- Assessment results and analytics
- Learning session data
- Voice interaction records

### Important Data (RPO: 1 hour)
- Generated educational content
- System configuration
- Application logs
- Monitoring metrics

### Non-Critical Data (RPO: 24 hours)
- Static assets
- Cached content
- Temporary files

## 🔄 Backup Strategy

### 1. Database Backups

#### PostgreSQL Continuous Backup
```bash
# Full backup daily at 2 AM
0 2 * * * pg_dump -h postgres -U rsp_user -d rsp_education | gzip > /backups/db/rsp_education_$(date +%Y%m%d).sql.gz

# Point-in-time recovery with WAL archiving
archive_mode = on
archive_command = 'test ! -f /backups/wal/%f && cp %p /backups/wal/%f'
wal_level = replica
```

#### Backup Verification
```bash
# Automated backup verification script
#!/bin/bash
BACKUP_FILE="/backups/db/rsp_education_$(date +%Y%m%d).sql.gz"
if [ -f "$BACKUP_FILE" ]; then
    # Test restore to temporary database
    createdb test_restore_$(date +%Y%m%d)
    gunzip -c "$BACKUP_FILE" | psql test_restore_$(date +%Y%m%d)
    dropdb test_restore_$(date +%Y%m%d)
    echo "Backup verification successful"
else
    echo "Backup file not found - ALERT"
    # Send alert notification
fi
```

### 2. Redis Backup
```bash
# Redis snapshot backup every 6 hours
0 */6 * * * docker exec rsp_redis redis-cli BGSAVE
0 */6 * * * cp /var/lib/docker/volumes/rsp_redis_data/_data/dump.rdb /backups/redis/dump_$(date +%Y%m%d_%H).rdb
```

### 3. Application Files and Configuration
```bash
# Backup application configuration and custom content
0 3 * * * tar -czf /backups/app/app_config_$(date +%Y%m%d).tar.gz \
    /app/config \
    /app/uploads \
    /app/logs \
    /app/ssl \
    docker-compose.prod.yml \
    .env.production
```

### 4. Container Images
```bash
# Save Docker images for rapid deployment
docker save rsp_backend:latest | gzip > /backups/images/rsp_backend_$(date +%Y%m%d).tar.gz
docker save postgres:15-alpine | gzip > /backups/images/postgres_$(date +%Y%m%d).tar.gz
docker save redis:7-alpine | gzip > /backups/images/redis_$(date +%Y%m%d).tar.gz
```

## ☁️ Remote Backup Storage

### AWS S3 Configuration
```bash
# Upload backups to S3 with encryption
aws s3 sync /backups/ s3://rsp-education-backups/ \
    --storage-class STANDARD_IA \
    --server-side-encryption AES256 \
    --delete

# Lifecycle policy for cost optimization
{
    "Rules": [
        {
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 30,
                    "StorageClass": "GLACIER"
                },
                {
                    "Days": 90, 
                    "StorageClass": "DEEP_ARCHIVE"
                }
            ],
            "Expiration": {
                "Days": 2555  // 7 years retention
            }
        }
    ]
}
```

### Backup Encryption
```bash
# Encrypt sensitive backups before upload
gpg --cipher-algo AES256 --compress-algo 1 --s2k-cipher-algo AES256 \
    --s2k-digest-algo SHA256 --s2k-mode 3 --s2k-count 65011712 \
    --force-mdc --symmetric --output backup_encrypted.gpg backup.sql
```

## 🚨 Disaster Recovery Procedures

### Scenario 1: Database Corruption/Failure

#### Detection
- Monitoring alerts on database connectivity
- Application errors indicating database issues
- Automated health checks failing

#### Recovery Steps
1. **Immediate Response (0-15 minutes)**
   ```bash
   # Switch to read-only mode
   kubectl patch deployment rsp-backend -p '{"spec":{"replicas":0}}'
   
   # Assess damage
   pg_dump --schema-only rsp_education > schema_check.sql
   ```

2. **Database Recovery (15-60 minutes)**
   ```bash
   # Stop all services
   docker-compose down
   
   # Restore from latest backup
   dropdb rsp_education
   createdb rsp_education
   gunzip -c /backups/db/rsp_education_latest.sql.gz | psql rsp_education
   
   # Apply WAL files for point-in-time recovery
   pg_wal_replay_resume
   ```

3. **Service Restoration (60-90 minutes)**
   ```bash
   # Start services
   docker-compose up -d
   
   # Verify data integrity
   python -m pytest tests/integration/test_data_integrity.py
   
   # Resume normal operations
   ```

### Scenario 2: Complete System Failure

#### Recovery Steps
1. **Infrastructure Provisioning (0-30 minutes)**
   ```bash
   # Deploy to backup infrastructure
   terraform apply -var="environment=disaster-recovery"
   
   # Configure DNS failover
   aws route53 change-resource-record-sets --hosted-zone-id Z123456789 \
       --change-batch file://dns-failover.json
   ```

2. **Data Restoration (30-120 minutes)**
   ```bash
   # Restore all data from S3
   aws s3 sync s3://rsp-education-backups/latest/ /backups/
   
   # Restore databases
   gunzip -c /backups/db/rsp_education_latest.sql.gz | psql rsp_education
   
   # Restore Redis data
   cp /backups/redis/dump_latest.rdb /var/lib/redis/
   ```

3. **Application Deployment (120-180 minutes)**
   ```bash
   # Load Docker images
   docker load < /backups/images/rsp_backend_latest.tar.gz
   
   # Deploy application stack
   docker-compose -f docker-compose.disaster-recovery.yml up -d
   
   # Run health checks
   curl -f http://localhost/health
   ```

### Scenario 3: Data Center Outage

#### Multi-Region Failover
1. **Automatic Failover (0-5 minutes)**
   - Route 53 health checks detect primary region failure
   - DNS automatically routes traffic to secondary region
   - Load balancer redirects to backup infrastructure

2. **Manual Verification (5-15 minutes)**
   ```bash
   # Verify secondary region status
   aws ec2 describe-instances --region us-west-2 --filters "Name=tag:Environment,Values=production-backup"
   
   # Check data synchronization
   pg_stat_replication
   ```

## 📊 Monitoring and Alerting

### Backup Monitoring
```yaml
# Prometheus alerts for backup failures
groups:
  - name: backup.rules
    rules:
      - alert: BackupFailed
        expr: backup_success{job="backup-job"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Backup job failed"
          description: "Backup job {{ $labels.job }} has failed"

      - alert: BackupOld
        expr: time() - backup_last_success_timestamp{job="backup-job"} > 86400
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Backup is older than 24 hours"
```

### Recovery Testing
```bash
# Monthly disaster recovery drill
#!/bin/bash
# File: /scripts/dr_drill.sh

echo "Starting disaster recovery drill..."

# Create isolated test environment
docker-compose -f docker-compose.dr-test.yml up -d

# Restore from backup
restore_from_backup.sh

# Run application tests
python -m pytest tests/integration/ --dr-test

# Measure recovery time
echo "Recovery completed in: $SECONDS seconds"

# Generate drill report
generate_dr_report.sh
```

## 🔧 Automation Scripts

### Backup Automation
```bash
#!/bin/bash
# File: /scripts/automated_backup.sh

set -e

BACKUP_DIR="/backups"
S3_BUCKET="rsp-education-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directories
mkdir -p $BACKUP_DIR/{db,redis,app,images}

# Database backup
echo "Starting database backup..."
pg_dump -h postgres -U rsp_user -d rsp_education | gzip > $BACKUP_DIR/db/rsp_education_$DATE.sql.gz

# Redis backup
echo "Starting Redis backup..."
docker exec rsp_redis redis-cli BGSAVE
sleep 10
cp /var/lib/docker/volumes/rsp_redis_data/_data/dump.rdb $BACKUP_DIR/redis/dump_$DATE.rdb

# Application files backup
echo "Starting application backup..."
tar -czf $BACKUP_DIR/app/app_files_$DATE.tar.gz /app/uploads /app/config /app/ssl

# Upload to S3
echo "Uploading to S3..."
aws s3 sync $BACKUP_DIR/ s3://$S3_BUCKET/ --delete

# Cleanup old local backups (keep last 7 days)
find $BACKUP_DIR -type f -mtime +7 -delete

# Send success notification
curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"Backup completed successfully"}' \
    $SLACK_WEBHOOK_URL

echo "Backup completed successfully at $(date)"
```

### Recovery Automation
```bash
#!/bin/bash
# File: /scripts/automated_recovery.sh

set -e

BACKUP_SOURCE="s3://rsp-education-backups"
RESTORE_POINT=${1:-latest}

echo "Starting automated recovery from $RESTORE_POINT..."

# Stop services
docker-compose down

# Download backups from S3
aws s3 sync $BACKUP_SOURCE/$RESTORE_POINT/ /tmp/restore/

# Restore database
echo "Restoring database..."
dropdb --if-exists rsp_education_restore
createdb rsp_education_restore
gunzip -c /tmp/restore/db/*.sql.gz | psql rsp_education_restore

# Restore Redis
echo "Restoring Redis..."
cp /tmp/restore/redis/dump_*.rdb /var/lib/docker/volumes/rsp_redis_data/_data/dump.rdb

# Restore application files
echo "Restoring application files..."
tar -xzf /tmp/restore/app/*.tar.gz -C /

# Start services
docker-compose up -d

# Verify recovery
sleep 30
curl -f http://localhost/health || exit 1

echo "Recovery completed successfully at $(date)"
```

## 📋 Recovery Checklists

### Critical System Failure Checklist
- [ ] Assess scope of failure
- [ ] Notify stakeholders
- [ ] Activate disaster recovery team
- [ ] Execute recovery procedures
- [ ] Verify data integrity
- [ ] Test all critical functions
- [ ] Update monitoring systems
- [ ] Document lessons learned

### Post-Recovery Validation
- [ ] Database connectivity and integrity
- [ ] All AI agents responding correctly
- [ ] User authentication working
- [ ] File uploads/downloads functional
- [ ] Monitoring and alerting active
- [ ] Performance within acceptable limits
- [ ] Security configurations intact

## 📞 Emergency Contacts

- **System Administrator**: +1-XXX-XXX-XXXX
- **Database Administrator**: +1-XXX-XXX-XXXX  
- **DevOps Lead**: +1-XXX-XXX-XXXX
- **Cloud Provider Support**: Support portal + phone
- **Management**: +1-XXX-XXX-XXXX

## 📅 Maintenance Schedule

- **Daily**: Automated backups, health checks
- **Weekly**: Backup verification, log review
- **Monthly**: Disaster recovery drill
- **Quarterly**: Full BDR plan review and update
- **Annually**: Complete infrastructure disaster recovery test

---

**Last Updated**: July 24, 2025
**Next Review**: October 24, 2025
**Document Owner**: DevOps Team