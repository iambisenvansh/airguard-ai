# AirGuard AI - Complete Full-Stack System Guide

## 🌍 System Overview

AirGuard AI is a complete full-stack pollution monitoring system consisting of:

1. **Python Backend** - Autonomous AI agent with policy enforcement
2. **Flask API** - REST API wrapper for frontend integration
3. **React Frontend** - Modern web interface for users

```
┌─────────────────────────────────────────────────────────────────┐
│                    USERS                                        │
│                   (Browsers)                                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
    ┌───────────────▼────────────┐  ┌────▼──────────────────┐
    │   React Frontend           │  │   Static Files        │
    │   (Port 3000)              │  │   (HTML/CSS/JS)       │
    ├──────────────────────────┤  └───────────────────────┘
    │ - Dashboard              │
    │ - Command Executor       │
    │ - Audit Logs             │
    │ - Reports Manager        │
    │ - Settings               │
    └────────────┬─────────────┘
                 │
        ┌────────▼────────┐
        │  HTTP/REST API  │
        │  (axios client) │
        └────────┬────────┘
                 │
    ┌────────────▼──────────────┐
    │  Flask API Server         │
    │  (Port 5000)              │
    ├─────────────────────────┤
    │ - Authentication         │
    │ - Route handlers         │
    │ - Database integration   │
    │ - Error handling         │
    │ - CORS support          │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │  Python Backend           │
    │  (AirGuard AI Core)       │
    ├─────────────────────────┤
    │ - Intent Parser          │
    │ - Policy Engine          │
    │ - Security Enforcer      │
    │ - Executor               │
    │ - Audit Logger           │
    │ - File Operations        │
    └──────────────────────────┘
```

## 🚀 Getting Started - Complete Setup

### Prerequisites
- Node.js 14+ (for frontend)
- Python 3.9+ (for backend)
- npm or yarn
- pip

### Step 1: Install Dependencies

**Backend API**
```bash
# Install Python packages
pip install -r requirements_api.txt

# Or install individually
pip install flask flask-cors pyjwt python-dotenv gunicorn
```

**Frontend**
```bash
cd frontend
npm install
```

### Step 2: Configure Environment

**Frontend .env**
```bash
cd frontend
cp .env.example .env
# Edit .env if needed
```

**Backend (Optional)**
```bash
# Create .env in root directory if needed
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

### Step 3: Run the System

**Terminal 1 - Backend API Server**
```bash
python backend_api.py
# Server runs on http://localhost:5000
# Logs show: Running on http://0.0.0.0:5000
```

**Terminal 2 - Frontend Development Server**
```bash
cd frontend
npm start
# Browser opens at http://localhost:3000
# Press Ctrl+C to stop
```

**Terminal 3 - Python Backend (Optional, if running separately)**
```bash
# The main Python agent runs as part of the Flask API
# No separate process needed
```

### Step 4: Access the System

1. Open browser: `http://localhost:3000`
2. Login with credentials:
   - Username: `admin` (or `operator` / `viewer`)
   - Password: `password123`

## 📊 Component Architecture

### Frontend Layer (React - Port 3000)

**Pages**
- **Login.jsx** - Authentication page
- **Dashboard.jsx** - Real-time metrics and analytics
- **Commands.jsx** - Command input and execution
- **AuditLogs.jsx** - Historical command logs
- **Reports.jsx** - Report management
- **Settings.jsx** - Admin configuration

**Services**
- **api.js** - Axios client with interceptors, JWT handling, error management

**Stores** (Zustand)
- **authStore.js** - Authentication and user state
- **commandStore.js** - Command history and favorites

**Components**
- **Layout/Header.jsx** - Navigation and user menu
- **Layout/Layout.jsx** - Page wrapper

**Styling**
- Tailwind CSS for utility-first styling
- Responsive design (mobile, tablet, desktop)
- Dark mode support (configurable)

### API Layer (Flask - Port 5000)

**Authentication Routes**
```
POST /api/auth/login - User authentication
POST /api/auth/logout - Session termination
POST /api/auth/refresh - Token renewal
```

**Command Routes**
```
POST /api/process_command - Execute AI commands
```

**Status Routes**
```
GET /api/status - Real-time pollution metrics
GET /api/system_status - System statistics
GET /api/health - Health check
```

**Audit Routes**
```
GET /api/audit_logs - Filtered audit logs
```

**Report Routes**
```
GET /api/reports - List reports
GET /api/reports/<filename> - Download report
DELETE /api/reports/<filename> - Delete report
```

**Admin Routes**
```
GET /api/users - List users
POST /api/users - Create user
DELETE /api/users/<id> - Delete user
GET/PUT /api/settings - Manage settings
```

### Backend Layer (Python - Core Logic)

**agent.py** - Main orchestrator
- Coordinates intent parsing, policy validation, enforcement, execution
- `process_command()` - Main entry point
- `get_system_status()` - Statistics

**intent.py** - NLP processing
- `parse_intent()` - Converts natural language to Intent objects
- Pattern matching engine

**policy.py** - Security decisions
- `validate_intent()` - Checks policy rules
- Rule loading and matching

**enforce.py** - Critical security gateway
- `enforce_and_execute()` - Final authorization
- Blocks unauthorized actions

**executor.py** - Action handlers
- `generate_report()` - Creates analysis reports
- `analyze_aqi()` - Calculates pollution statistics
- `send_alert()` - Sends notifications

**logger.py** - Audit trail
- `log_action()` - Records all operations
- JSON-based audit logs

**models.py** - Data structures
- Intent, PolicyDecision, ExecutionResult classes

## 🔒 Security Architecture

### Authentication Flow
```
User Input (username/password)
    ↓
Flask /login endpoint validates credentials
    ↓
JWT token generated with 24-hour expiry
    ↓
Token sent to frontend, stored in HttpOnly cookie
    ↓
Subsequent requests include Authorization header
    ↓
JWT middleware validates token
```

### Authorization Flow
```
Authenticated Request
    ↓
Check user role (admin/operator/viewer)
    ↓
Verify endpoint permissions
    ↓
Route decorator checks @admin_required, etc.
    ↓
Either allow or return 403 Forbidden
```

### Command Execution Flow
```
User Command → Frontend
    ↓
POST /api/process_command with auth token
    ↓
Backend Flask API receives request
    ↓
Intent Parser: "Generate report" → Intent object
    ↓
Policy Engine: Check if action allowed
    ↓
Enforcer: Final security check (CRITICAL)
    ↓
Executor: Run approved action (or block)
    ↓
Logger: Record decision and result
    ↓
Response: Return intent + decision + result
    ↓
Frontend: Display response
```

## 📡 API Request/Response Examples

### Authentication
**Request**
```bash
POST /api/auth/login
{
  "username": "admin",
  "password": "password123"
}
```

**Response**
```json
{
  "user": {
    "username": "admin",
    "role": "admin",
    "id": 1
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Command Execution
**Request**
```bash
POST /api/process_command
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

{
  "command": "Generate pollution report for Delhi"
}
```

**Response (Allowed)**
```json
{
  "success": true,
  "message": "Report generated successfully",
  "intent": {
    "action": "generate_report",
    "parameters": {"location": "Delhi"},
    "confidence": 0.95,
    "timestamp": "2024-01-15T10:30:45.123456",
    "user_command": "Generate pollution report for Delhi"
  },
  "policy_decision": {
    "allowed": true,
    "reason": "Report generation is read-only and essential for pollution monitoring",
    "rule_name": "generate_report"
  },
  "result": {
    "success": true,
    "message": "Report generated successfully",
    "execution_time": 0.234,
    "files_created": ["output/delhi_report_2024_01_15.txt"]
  },
  "status": "SUCCESS",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "user": "admin"
}
```

**Response (Blocked)**
```json
{
  "success": false,
  "message": "Action blocked by policy enforcement",
  "intent": {
    "action": "shutdown_factory",
    "parameters": {"location": "Mayapuri"},
    "confidence": 0.95
  },
  "policy_decision": {
    "allowed": false,
    "reason": "Critical infrastructure control requires human authorization",
    "rule_name": "shutdown_factory"
  },
  "status": "BLOCKED"
}
```

## 🧪 Testing the System

### Frontend Testing
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build

# Start production build
npm start
```

### Backend Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'

# Test command (replace TOKEN with actual token)
curl -X POST http://localhost:5000/api/process_command \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "Analyze AQI in Delhi"}'
```

### Integration Testing
```bash
# Run the complete system
# Terminal 1: Backend API
python backend_api.py

# Terminal 2: Frontend
cd frontend && npm start

# Terminal 3: Manual testing
# Open http://localhost:3000 in browser
# Test all workflows
```

## 🚢 Production Deployment

### Frontend Production Build
```bash
cd frontend
npm run build

# Build output in frontend/build/
# Serve with web server (nginx, Apache, S3+CloudFront)
```

### Backend Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend_api:app

# Using uWSGI
uwsgi --http :5000 --wsgi-file backend_api.py --callable app

# With reverse proxy (nginx recommended)
# See deployment guide below
```

### Docker Deployment
```bash
# Build images
docker build -t airguard-frontend -f Dockerfile.frontend .
docker build -t airguard-backend -f Dockerfile.backend .

# Run containers
docker run -p 3000:3000 airguard-frontend
docker run -p 5000:5000 airguard-backend

# Or use docker-compose
docker-compose up
```

### Nginx Configuration (Production)
```nginx
upstream backend_api {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    root /var/www/airguard/build;
    location / {
        try_files $uri /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Logs

### Frontend Logs
- Browser console: Open DevTools (F12) → Console tab
- Network requests: DevTools → Network tab
- Local storage: DevTools → Application → Local Storage

### Backend Logs
- Terminal output shows all Flask logs
- Request/response logging enabled by default
- Check `logs/audit.log` for audit trail

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Token expired, login again |
| 403 Forbidden | Insufficient permissions for role |
| 404 Not Found | API endpoint doesn't exist, check URL |
| 500 Server Error | Check backend logs, restart if needed |
| CORS errors | Verify backend CORS config, check origin |
| Command timeout | Check backend is responsive, increase timeout |

## 🔄 Data Flow Examples

### Example 1: Admin Login and View Audit Logs
```
1. User enters credentials on Login page
2. Frontend POST /auth/login
3. Backend validates, returns JWT token
4. Frontend stores token, redirects to dashboard
5. User clicks "Audit Logs"
6. Frontend GET /audit_logs with Authorization header
7. Backend validates token, checks role is admin/operator
8. Backend fetches logs, returns filtered results
9. Frontend displays paginated table
```

### Example 2: Operator Executes Command
```
1. User types: "Generate pollution report for Delhi"
2. Frontend shows suggestions/autocomplete
3. User presses Enter or clicks Submit
4. Frontend POST /process_command with token
5. Backend intent parser extracts: action=generate_report, location=Delhi
6. Backend policy engine checks policy.json: allowed=true
7. Backend enforcer verifies: not blocked, proceed
8. Backend executor creates report file
9. Backend returns: success, result, files_created
10. Frontend displays success response
11. User can download or view report
```

### Example 3: Viewer Attempts Blocked Action
```
1. Viewer is limited to read-only operations
2. Viewer attempts: "Shutdown factory in Mayapuri"
3. Frontend POST /process_command with token
4. Backend intent parser: action=shutdown_factory
5. Backend policy engine: allowed=false, reason="needs human auth"
6. Backend enforcer: BLOCKS action (returns denial)
7. Backend does NOT call executor (critical!)
8. Response shows: blocked, reason, policy_decision
9. Frontend displays blocked message in red
10. Action logged in audit trail
```

## 🎓 Learning Resources

### Frontend Development
- React documentation: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/
- Axios: https://axios-http.com/
- Zustand: https://github.com/pmndrs/zustand

### Backend Development
- Flask: https://flask.palletsprojects.com/
- JWT: https://jwt.io/
- Python requests: https://requests.readthedocs.io/

### System Architecture
- REST APIs: https://restfulapi.net/
- Authentication: https://owasp.org/www-community/controls/Authentication
- Authorization: https://owasp.org/www-community/controls/Access_Control

## 📞 Troubleshooting

### "Cannot GET /api/..."
- Backend not running on port 5000
- Check if `python backend_api.py` is executing
- Verify no firewall blocking port 5000

### "Unexpected end of JSON input"
- Backend returned non-JSON response
- Check backend error logs
- Ensure correct Content-Type headers

### "Invalid token" errors
- Token has expired (24-hour expiry)
- Token corrupted or modified
- Login again to get new token

### Frontend won't start
- Check Node.js installed: `node --version`
- Try: `npm install` and `npm start` again
- Clear node_modules: `rm -rf node_modules && npm install`

### Backend crashes
- Check Python version: `python --version` (need 3.9+)
- Check dependencies: `pip list | grep flask`
- Try: `pip install -r requirements_api.txt`

## 📝 Next Steps

1. **Customize** - Modify pages and components to match your branding
2. **Extend** - Add new API endpoints and frontend pages
3. **Integrate** - Connect to real pollution data sources
4. **Scale** - Optimize for production (caching, CDN, database)
5. **Monitor** - Set up logging, error tracking, and alerting

## 📄 File Reference

### Frontend Files
- `frontend/src/pages/` - Page components
- `frontend/src/services/api.js` - API client
- `frontend/src/store/` - State management
- `frontend/src/components/` - Reusable components
- `frontend/package.json` - Dependencies

### Backend Files
- `backend_api.py` - Flask API server
- `requirements_api.txt` - Python dependencies
- `agent.py` - AI agent orchestrator
- `policy.json` - Security rules
- `logs/audit.log` - Audit trail

## 📞 Support & Contact

For issues:
1. Check this guide
2. Review backend logs
3. Check frontend console (F12)
4. Verify services are running
5. Check firewall/ports are open

---

**AirGuard AI - Complete Full-Stack Pollution Monitoring System**

Built with React, Flask, and Python for secure, efficient air quality monitoring.

✨ **Happy monitoring!** ✨
