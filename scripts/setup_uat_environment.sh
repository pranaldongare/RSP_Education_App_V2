#!/bin/bash
# UAT Environment Setup Script
# RSP Education Agent V2 - User Acceptance Testing

set -e

echo "🚀 Setting up UAT Environment for RSP Education Agent V2"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    print_error "Please run this script from the RSP_Education_App_V2 root directory"
    exit 1
fi

print_status "Step 1: Setting up environment variables..."

# Create UAT environment file
if [ ! -f ".env.uat" ]; then
    print_status "Creating UAT environment configuration..."
    cat > .env.uat << 'EOF'
# UAT Environment Configuration
# RSP Education Agent V2

# Database (SQLite for UAT)
DATABASE_URL=sqlite:///./uat_rsp_education.db
DB_ECHO=true

# Redis (Local)
REDIS_URL=redis://localhost:6379/2

# Application
APP_ENV=uat
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

# AI Mock Mode (Enable if no API keys)
MOCK_AI_RESPONSES=true

# Security (UAT values)
SECRET_KEY=uat_secret_key_for_testing_only_not_for_production
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Logging
LOG_LEVEL=DEBUG

# Performance
WORKERS=2

# Features (Enable all for UAT)
ENABLE_VOICE_INTERACTION=true
ENABLE_MULTILINGUAL_SUPPORT=true
ENABLE_ANALYTICS=true

# UAT Specific
UAT_MODE=true
TEST_DATA_ENABLED=true
EOF
    print_success "UAT environment file created: .env.uat"
else
    print_warning "UAT environment file already exists"
fi

print_status "Step 2: Installing Python dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Install backend dependencies
cd backend
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

print_status "Activating virtual environment and installing dependencies..."
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements_phase2.txt

# Install additional UAT dependencies
pip install pytest httpx

print_success "Python dependencies installed"
cd ..

print_status "Step 3: Setting up Flutter..."

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    print_warning "Flutter is not installed. Please install Flutter to test the frontend."
    print_warning "Visit: https://flutter.dev/docs/get-started/install"
else
    print_status "Installing Flutter dependencies..."
    cd frontend
    flutter pub get
    print_success "Flutter dependencies installed"
    cd ..
fi

print_status "Step 4: Setting up local services..."

# Check if Docker is installed
if command -v docker &> /dev/null; then
    print_status "Starting local Redis with Docker..."
    docker run -d --name uat-redis -p 6379:6379 redis:7-alpine || print_warning "Redis container might already be running"
    print_success "Redis started on port 6379"
else
    print_warning "Docker not found. Please install Redis manually or install Docker."
fi

print_status "Step 5: Creating UAT test data..."

# Create test data script
cat > scripts/create_test_data.py << 'EOF'
#!/usr/bin/env python3
"""
Create test data for UAT
"""
import sqlite3
import json
from datetime import datetime

def create_test_data():
    # Connect to UAT database
    conn = sqlite3.connect('uat_rsp_education.db')
    cursor = conn.cursor()
    
    # Create test student
    cursor.execute('''
        INSERT OR REPLACE INTO students (id, name, grade, email, preferences, learning_style, preferred_language, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'uat_test_student',
        'UAT Test Student',
        '5',
        'uat@test.com',
        json.dumps({"subjects": ["Mathematics", "Science"], "difficulty": "medium"}),
        'visual',
        'en',
        datetime.now().isoformat()
    ))
    
    # Create test learning profile
    cursor.execute('''
        INSERT OR REPLACE INTO learning_profiles (student_id, learning_pace, preferred_difficulty, skill_levels, overall_performance, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'uat_test_student',
        'medium',
        'medium',
        json.dumps({"mathematics": 0.75, "science": 0.80}),
        0.77,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    print("✅ Test data created successfully")

if __name__ == "__main__":
    create_test_data()
EOF

print_status "Step 6: Creating UAT startup script..."

# Create startup script
cat > scripts/start_uat_services.sh << 'EOF'
#!/bin/bash
# Start UAT Services Script

echo "🚀 Starting UAT Services..."

# Start backend
echo "Starting FastAPI backend..."
cd backend
source venv/bin/activate
export $(cat ../.env.uat | xargs)
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend (if Flutter is available)
if command -v flutter &> /dev/null; then
    echo "Starting Flutter frontend..."
    cd frontend
    flutter run -d web-server --web-port 3000 &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Frontend started on http://localhost:3000"
fi

echo ""
echo "🎉 UAT Environment Ready!"
echo "================================"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
echo ""
echo "To run UAT tests:"
echo "python scripts/run_uat_tests.py"
echo ""
echo "To stop services:"
echo "kill $BACKEND_PID"
if [ ! -z "$FRONTEND_PID" ]; then
    echo "kill $FRONTEND_PID"
fi

# Keep script running
wait
EOF

chmod +x scripts/start_uat_services.sh
chmod +x scripts/create_test_data.py
chmod +x scripts/run_uat_tests.py

print_status "Step 7: Creating quick test script..."

# Create quick test script
cat > scripts/quick_uat_check.sh << 'EOF'
#!/bin/bash
# Quick UAT Health Check

echo "🔍 Quick UAT Health Check"
echo "========================"

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not running"
    echo "   Start with: ./scripts/start_uat_services.sh"
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend: Running"
else
    echo "⚠️  Frontend: Not running or not available"
fi

# Check Redis
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Running"
else
    echo "⚠️  Redis: Not running"
fi

echo ""
echo "Run full UAT: python scripts/run_uat_tests.py"
EOF

chmod +x scripts/quick_uat_check.sh

print_success "UAT Environment Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Start UAT services:"
echo "   ./scripts/start_uat_services.sh"
echo ""
echo "2. Run UAT tests:"
echo "   python scripts/run_uat_tests.py"
echo ""
echo "3. Quick health check:"
echo "   ./scripts/quick_uat_check.sh"
echo ""
echo "4. View UAT documentation:"
echo "   docs/uat-testing-guide.md"
echo ""
print_success "UAT environment is ready for testing! 🚀"