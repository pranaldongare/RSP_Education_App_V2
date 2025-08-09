# 🐳 Docker Setup Guide - RSP Education Agent V2

This guide will help you run the complete RSP Education Agent V2 project using Docker. **No need to install Python, Flutter, or any other dependencies!** Just Docker.

## 📋 Prerequisites

### 1. Install Docker Desktop
- **Windows**: Download from [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
- **Mac**: Download from [Docker Desktop for Mac](https://desktop.docker.com/mac/main/amd64/Docker.dmg)  
- **Linux**: Follow [Docker Engine installation guide](https://docs.docker.com/engine/install/)

### 2. Verify Docker Installation
```bash
docker --version
docker-compose --version
```

You should see version numbers for both commands.

## 🚀 Quick Start (5 Minutes Setup)

### Step 1: Clone and Setup
```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd RSP_Education_App_V2

# Setup environment file
cp .env.example .env
```

### Step 2: Add Your API Keys
Edit the `.env` file and add your API keys:
```env
# Required: Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Optional: Get from https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here

# Generate a secure secret key (or use the provided one for testing)
SECRET_KEY=your_super_secret_jwt_key_here_change_in_production
```

### Step 3: Start the Application
```bash
# Option 1: Using Make (Recommended - Windows users may need to install Make)
make quick-start

# Option 2: Using Docker Compose directly
docker-compose up -d
```

### Step 4: Access the Application
- 🌐 **Frontend (Student/Parent UI)**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 💾 **Database Admin**: http://localhost:8080 (username: `rsp_user`, password: `rsp_password`)

## 📱 How to Use the Application

### For Students:
1. Go to http://localhost:3000
2. Click "Register" to create a new account
3. Fill in your details (Name, Email, Password, Grade)
4. Login with your credentials
5. Select a subject (Mathematics, Science, English, Social Studies)
6. Choose a topic to start learning
7. Get AI-generated explanations and practice questions!

### For Developers:
1. API Documentation: http://localhost:8000/docs
2. Test endpoints directly from the docs
3. Check application logs: `make logs`

## 🛠️ Available Commands

We've created simple commands to manage the entire Docker setup:

```bash
# Essential Commands
make help              # Show all available commands
make quick-start       # Complete setup for first-time users
make up               # Start all services
make down             # Stop all services
make restart          # Restart all services

# Development Commands
make logs             # View all logs
make logs-backend     # View backend logs only
make logs-frontend    # View frontend logs only
make status           # Check service status
make health           # Check service health

# Testing Commands
make test             # Run UAT tests
make test-backend     # Run backend unit tests

# Database Commands
make db-reset         # Reset database (⚠️ Deletes all data)
make db-backup        # Create database backup
make shell-db         # Access database shell

# Maintenance Commands
make clean            # Remove unused Docker resources
make clean-all        # Remove everything (⚠️ Nuclear option)
```

## 🏗️ Architecture Overview

When you run `make up` or `docker-compose up`, the following services start:

```
┌─────────────────────────────────────────────────────────┐
│                 RSP Education Agent V2                  │
├─────────────────────────────────────────────────────────┤
│  🌐 Frontend (Port 3000)                               │
│  ├── Flutter Web Application                           │
│  ├── Student/Parent Dashboard                          │
│  └── Responsive UI for all devices                     │
├─────────────────────────────────────────────────────────┤
│  🔧 Backend API (Port 8000)                            │
│  ├── FastAPI with 8 AI Agents                         │
│  ├── JWT Authentication                                │
│  ├── OpenAI/Anthropic Integration                     │
│  └── RESTful API with auto-docs                       │
├─────────────────────────────────────────────────────────┤
│  💾 PostgreSQL Database (Port 5432)                    │
│  ├── Student data and progress                        │
│  ├── Curriculum and assessments                       │
│  └── Persistent data storage                          │
├─────────────────────────────────────────────────────────┤
│  🚀 Redis Cache (Port 6379)                            │
│  ├── Session storage                                  │
│  ├── API response caching                             │
│  └── Real-time data                                   │
└─────────────────────────────────────────────────────────┘
```

## 🧪 Testing the Setup

### Automated Testing
```bash
# Run the comprehensive UAT test
make test

# Expected output:
# RSP EDUCATION AGENT V2 - UAT READINESS TEST
# =======================================================
# ✓ System Health Check: OPERATIONAL
# ✓ AI Content Generation: SUCCESS (1000+ characters)  
# ✓ User Authentication: SUCCESS
# ✓ Question Generation: SUCCESS
# ✓ AI Agents Status: ACTIVE
# ✓ Curriculum Access: SUCCESS
# 
# Tests Passed: 6/6 (100% Success Rate)
# 🎉 SYSTEM READY FOR UAT!
```

### Manual Testing
1. **Frontend Test**: Go to http://localhost:3000 - should see the RSP Education login page
2. **Backend Test**: Go to http://localhost:8000/health - should return `{"status":"healthy"}`
3. **API Docs Test**: Go to http://localhost:8000/docs - should see interactive API documentation
4. **Database Test**: Go to http://localhost:8080 - should see Adminer database interface

## 🔧 Development Mode

For developers who want to make changes to the code:

```bash
# Start in development mode with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Additional development tools will be available:
# - Database Admin: http://localhost:8080
# - Redis GUI: http://localhost:8081
# - Hot reload for both frontend and backend
```

## 🚨 Troubleshooting

### Issue: Services won't start
```bash
# Check Docker is running
docker info

# Check for port conflicts
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# View detailed logs
make logs
```

### Issue: API keys not working
```bash
# Verify environment file
cat .env | grep API_KEY

# Restart with new environment
make restart
```

### Issue: Database connection failed
```bash
# Check database status
make status

# Reset database if corrupted
make db-reset
```

### Issue: Out of disk space
```bash
# Clean up Docker resources
make clean

# For severe cases (⚠️ removes everything)
make clean-all
```

## 📊 Monitoring and Logs

### View Logs
```bash
# All services
make logs

# Specific service
make logs-backend
make logs-frontend
make logs-db
```

### Check Service Health
```bash
# Quick health check
make health

# Detailed status
make status

# Individual service logs
docker-compose logs backend -f
```

## 🛡️ Security Notes

### For Development:
- Default passwords are used (fine for local development)
- Debug mode is enabled
- CORS is open to localhost

### For Production:
- Change all default passwords in `.env`
- Set `DEBUG=false`
- Configure proper CORS origins
- Use SSL certificates
- Use strong SECRET_KEY

## 📈 Performance

### Resource Usage:
- **RAM**: ~2-3 GB total for all services
- **CPU**: Light load (~10-20% on modern machines)
- **Disk**: ~5 GB for images + data storage
- **Network**: Only localhost traffic

### Scaling:
- Each service can be scaled independently
- Database supports multiple connections
- Redis handles high-frequency caching

## 🎯 Next Steps

After successful setup:

1. **Explore the API**: Go to http://localhost:8000/docs
2. **Test the Frontend**: Register a student account at http://localhost:3000
3. **Generate Content**: Try the AI content generation features
4. **Check Analytics**: View student progress and performance data
5. **Customize**: Modify the code and see changes in real-time

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. View logs: `make logs`
3. Check service status: `make status`
4. Reset if needed: `make clean` and `make up`
5. For persistent issues, check the main README.md

---

## 🎉 Success!

If you've followed this guide, you now have a complete AI-powered education platform running locally! 

**The RSP Education Agent V2 is ready to transform learning experiences with personalized AI tutoring.** 🚀🎓