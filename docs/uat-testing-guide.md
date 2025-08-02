# User Acceptance Testing (UAT) Guide
# RSP Education Agent V2 - Complete System Testing

## 🎯 Overview

This guide provides comprehensive User Acceptance Testing procedures to validate all system components, AI agents, and user workflows. Follow this systematically to ensure the platform works as expected.

## 🚀 Pre-UAT Setup

### 1. Local Development Setup
```bash
# Clone and setup the project
git clone https://github.com/your-org/RSP_Education_App_V2.git
cd RSP_Education_App_V2

# Setup environment (without production passwords)
cp .env.production .env.local
nano .env.local

# Update for local testing:
DATABASE_URL=sqlite:///./test_rsp_education.db
REDIS_URL=redis://localhost:6379/1
APP_DEBUG=true
MOCK_AI_RESPONSES=true  # Enable if no API keys
```

### 2. Start Services Locally
```bash
# Start basic services
docker-compose up -d postgres redis

# Install backend dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements_phase2.txt

# Start FastAPI backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Flutter web
cd ../frontend
flutter pub get
flutter run -d web-server --web-port 3000
```

### 3. Access Points
- **Backend API**: http://localhost:8000
- **Frontend Web**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 UAT Test Scenarios

### Phase 1: System Health & Infrastructure

#### Test 1.1: Basic Connectivity
```bash
# Test backend health
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Test API root
curl http://localhost:8000/api/v1/
# Expected: JSON with agent endpoints

# Test frontend loading
curl http://localhost:3000
# Expected: HTML content with no errors
```

**✅ Pass Criteria**: All endpoints return successful responses

#### Test 1.2: Database Connection
```bash
# Run API integration tests
cd backend
python test_api_integration.py

# Check results
cat api_integration_test_results.json
```

**✅ Pass Criteria**: All database tests pass, no connection errors

### Phase 2: AI Agent API Testing

#### Test 2.1: Content Generator Agent
```bash
# Test content generation
curl -X POST http://localhost:8000/api/v1/agents/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "5",
    "subject": "Mathematics",
    "topic": "Fractions",
    "content_type": "lesson",
    "difficulty": "medium",
    "learning_objectives": ["Understand basic fractions"]
  }'
```

**✅ Pass Criteria**: Returns structured content or mock response

#### Test 2.2: Assessment Agent  
```bash
# Test assessment generation
curl -X POST http://localhost:8000/api/v1/agents/assessment/generate \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "5",
    "subject": "Mathematics", 
    "topic": "Fractions",
    "difficulty": "medium",
    "question_count": 5,
    "question_types": ["multiple_choice"]
  }'
```

**✅ Pass Criteria**: Returns assessment structure with questions

#### Test 2.3: Adaptive Learning Agent
```bash
# Test learning profile update
curl -X POST http://localhost:8000/api/v1/agents/adaptive/profile/update \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "test_student_001",
    "performance_data": {"mathematics": 0.75},
    "completed_topics": ["fractions"],
    "skill_levels": {"problem_solving": 0.7}
  }'
```

**✅ Pass Criteria**: Returns updated learning profile

#### Test 2.4: Voice Interaction Agent
```bash
# Test voice capabilities
curl http://localhost:8000/api/v1/agents/voice/capabilities

# Expected: List of supported languages and features
```

**✅ Pass Criteria**: Returns voice capabilities configuration

#### Test 2.5: Learning Coordinator Agent
```bash
# Test coordinator initialization
curl -X POST http://localhost:8000/api/v1/agents/coordinator/initialize \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "test_student_001",
    "session_type": "adaptive_learning",
    "preferences": {"subjects": ["Mathematics"]}
  }'
```

**✅ Pass Criteria**: Returns session initialization data

### Phase 3: Frontend User Interface Testing

#### Test 3.1: Application Loading
1. Open http://localhost:3000 in browser
2. Verify loading screen appears
3. Check console for JavaScript errors
4. Verify main navigation loads

**✅ Pass Criteria**: App loads without errors, navigation visible

#### Test 3.2: AI Learning Session Widget
1. Navigate to learning session page
2. Enter test student ID: "test_student_001"
3. Select subject: "Mathematics", Grade: "5"
4. Click "Start Session"
5. Verify tabs load: Learn, Practice, Assess, Progress

**✅ Pass Criteria**: All tabs accessible, no Flutter errors

#### Test 3.3: Assessment Interface
1. Go to Assessment tab
2. Click "Start Assessment"
3. Verify questions display properly
4. Test navigation between questions
5. Test answer selection/input
6. Submit assessment

**✅ Pass Criteria**: Assessment flows work, results display

### Phase 4: End-to-End User Workflows

#### Test 4.1: Complete Learning Session
1. **Student Registration**
   - Create new student profile
   - Set grade level and preferences
   - Verify profile saves

2. **Adaptive Learning Flow**
   - Start learning session
   - Complete learning activity
   - Check personalized recommendations
   - Verify progress tracking

3. **Assessment Flow**
   - Take generated assessment
   - Submit answers
   - Review results and feedback
   - Check performance analytics

**✅ Pass Criteria**: Complete workflow functions without errors

#### Test 4.2: Multi-Agent Coordination
1. Start coordinated learning session
2. Complete content learning phase
3. Proceed to practice questions
4. Take assessment
5. Review analytics and next recommendations

**✅ Pass Criteria**: Agents work together seamlessly

### Phase 5: Data Persistence Testing

#### Test 5.1: Database Operations
```sql
-- Connect to database and verify data
sqlite3 test_rsp_education.db

-- Check student data
SELECT * FROM students WHERE id = 'test_student_001';

-- Check learning sessions
SELECT * FROM learning_sessions ORDER BY started_at DESC LIMIT 5;

-- Check assessments
SELECT * FROM assessments ORDER BY created_at DESC LIMIT 5;
```

**✅ Pass Criteria**: All data persists correctly

#### Test 5.2: Session State Management
1. Start learning session
2. Complete partial activity
3. Navigate away and return
4. Verify session state preserved

**✅ Pass Criteria**: State management works correctly

### Phase 6: Performance & Load Testing

#### Test 6.1: Response Time Testing
```bash
# Test API response times
time curl http://localhost:8000/api/v1/agents/content/generate \
  -X POST -H "Content-Type: application/json" \
  -d '{"grade":"5","subject":"Math","topic":"Fractions","content_type":"lesson","difficulty":"medium","learning_objectives":[]}'
```

**✅ Pass Criteria**: Responses under 5 seconds

#### Test 6.2: Concurrent User Simulation
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test concurrent requests
ab -n 100 -c 10 http://localhost:8000/health
```

**✅ Pass Criteria**: System handles concurrent requests

### Phase 7: Error Handling & Edge Cases

#### Test 7.1: Invalid Input Handling
```bash
# Test with invalid data
curl -X POST http://localhost:8000/api/v1/agents/content/generate \
  -H "Content-Type: application/json" \
  -d '{"grade":"invalid","subject":"","topic":"","content_type":"","difficulty":"","learning_objectives":[]}'
```

**✅ Pass Criteria**: Returns appropriate error messages

#### Test 7.2: Network Failure Simulation
1. Disconnect internet
2. Try to use AI features
3. Verify graceful degradation
4. Check error messages to user

**✅ Pass Criteria**: Graceful error handling

## 📱 Mobile App Testing (Android)

### Test 8.1: Android APK Testing
```bash
# Build Android APK
cd frontend
flutter build apk --debug

# Install on Android device/emulator
adb install build/app/outputs/flutter-apk/app-debug.apk

# Test core functionality on mobile
```

**✅ Pass Criteria**: App works on Android device

## 🧪 UAT Checklist

### System Infrastructure ✅
- [ ] Backend API accessible
- [ ] Database connection working
- [ ] Frontend loads without errors
- [ ] Health checks pass
- [ ] API documentation accessible

### AI Agent Functionality ✅
- [ ] Content Generator responds
- [ ] Assessment Agent generates questions
- [ ] Adaptive Learning updates profiles
- [ ] Voice Agent returns capabilities
- [ ] Learning Coordinator initializes sessions
- [ ] Engagement Agent tracks metrics
- [ ] Analytics Agent provides insights

### User Interface ✅
- [ ] Learning session widget functional
- [ ] Assessment interface works
- [ ] Navigation between screens
- [ ] State management working
- [ ] Error handling appropriate
- [ ] Mobile responsive design

### Data Management ✅
- [ ] Student profiles save/load
- [ ] Learning progress tracked
- [ ] Assessment results stored
- [ ] Session data persists
- [ ] Analytics data generated

### Performance ✅
- [ ] Response times acceptable (<5s)
- [ ] Concurrent users supported
- [ ] Memory usage reasonable
- [ ] No memory leaks detected
- [ ] Error rates low (<1%)

### Security ✅
- [ ] Input validation working
- [ ] SQL injection protection
- [ ] XSS protection enabled
- [ ] CORS configured properly
- [ ] Rate limiting functional

## 🐛 Issue Tracking Template

### Bug Report Format
```
**Bug ID**: UAT-001
**Priority**: High/Medium/Low
**Component**: Backend API/Frontend/Database/AI Agent
**Description**: [Detailed description]
**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Expected result
4. Actual result
**Environment**: Local/Docker/Production
**Screenshots**: [If applicable]
**Logs**: [Relevant log entries]
```

## 📊 UAT Results Dashboard

### Create Test Results Tracking
```bash
# Create UAT results file
cat > uat_results.json << EOF
{
  "test_date": "$(date -I)",
  "total_tests": 50,
  "passed": 0,
  "failed": 0,
  "blocked": 0,
  "test_categories": {
    "infrastructure": {"total": 10, "passed": 0, "failed": 0},
    "ai_agents": {"total": 15, "passed": 0, "failed": 0},
    "frontend": {"total": 10, "passed": 0, "failed": 0},
    "workflows": {"total": 8, "passed": 0, "failed": 0},
    "performance": {"total": 5, "passed": 0, "failed": 0},
    "security": {"total": 2, "passed": 0, "failed": 0}
  },
  "issues_found": []
}
EOF
```

## 🚀 UAT Execution Steps

### Day 1: Infrastructure & Backend Testing
1. Execute Tests 1.1 - 1.2 (System Health)
2. Execute Tests 2.1 - 2.5 (AI Agent APIs)
3. Document any issues found
4. Update UAT results

### Day 2: Frontend & UI Testing  
1. Execute Tests 3.1 - 3.3 (Frontend UI)
2. Execute Test 4.1 (Learning Workflows)
3. Test responsive design on different screen sizes
4. Document UI/UX issues

### Day 3: Integration & Performance Testing
1. Execute Test 4.2 (Multi-Agent Coordination)
2. Execute Tests 5.1 - 5.2 (Data Persistence)
3. Execute Tests 6.1 - 6.2 (Performance)
4. Document integration issues

### Day 4: Error Handling & Mobile Testing
1. Execute Tests 7.1 - 7.2 (Error Handling)
2. Execute Test 8.1 (Mobile Testing)
3. Final review and documentation
4. Prepare UAT report

## 📋 Final UAT Sign-off

### Acceptance Criteria
- ✅ 90%+ test pass rate
- ✅ All critical functionality working
- ✅ No high-severity bugs
- ✅ Performance meets requirements
- ✅ Security validations pass
- ✅ User experience acceptable

### UAT Completion Report
```
UAT SUMMARY REPORT
==================
Project: RSP Education Agent V2
Test Period: [Start Date] - [End Date]
Total Test Cases: 50
Passed: [X] | Failed: [Y] | Blocked: [Z]
Pass Rate: [X]%

RECOMMENDATION: 
[ ] ACCEPT - Ready for production
[ ] CONDITIONAL ACCEPT - Minor issues to fix
[ ] REJECT - Major issues require resolution

Tester Signature: ________________
Date: ________________
```

---

This UAT guide ensures comprehensive testing of your entire RSP Education Agent V2 system. Follow it systematically to validate that everything works as expected before production deployment!