# 🌍 AirGuard AI - Full-Stack Pollution Monitoring System

**A complete full-stack AI-powered application for real-time air pollution monitoring with policy-based security enforcement, modern React frontend, and powerful Flask backend.**

---

## 📋 Overview

AirGuard AI is a production-ready full-stack application that monitors air pollution across Indian cities. It features an autonomous AI agent system that converts natural language commands into structured actions, validates them against security policies, and executes approved operations. The system includes a beautiful dark-mode React frontend, comprehensive REST API backend, and SQLite database with auto-audit logging.

### 🎯 Key Features

**Backend AI Agent:**
- ✅ **Natural Language Processing** - Converts commands into structured intents with high accuracy
- ✅ **Policy-Based Security** - Enforces strict rule-based security to prevent unauthorized actions
- ✅ **Blocked Actions** - Prevents dangerous operations (factory shutdown, fine issuance)
- ✅ **Real-Time Analysis** - Analyzes AQI data with statistical calculations

**Frontend Application:**
- ✅ **Modern React UI** - 6 fully featured pages with dark mode and responsive design
- ✅ **Real-time Dashboard** - Live pollution metrics, trends, and city comparisons
- ✅ **JWT Authentication** - Secure login system with role-based access control
- ✅ **Command Interface** - Execute pollution monitoring commands with real-time feedback
- ✅ **Audit Logs** - Track all system actions with detailed timestamps and user info
- ✅ **Reports & Analytics** - Generate and download comprehensive pollution reports
- ✅ **Settings & Admin** - User management and system configuration

**Backend & Database:**
- ✅ **REST API** - 21 endpoints for all operations
- ✅ **SQLite Database** - Persistent data storage with auto-audit logging
- ✅ **Role-Based Access Control** - Admin, user, and viewer roles
- ✅ **CORS Support** - Secure cross-origin requests
- ✅ **Error Handling** - Comprehensive error responses

---

## 🏗️ Architecture

### Full-Stack Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  Dashboard | Commands | Reports | Audit Logs | Settings        │
│         (Port 3000 - Dark Mode, Responsive Design)              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ JWT Authentication
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask REST API)                     │
│  21 Endpoints: Auth, Commands, Logs, Reports, Users, Status    │
│               (Port 5000 - CORS Enabled)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
   │  AI Agent   │  │   Policy    │  │  Executor    │
   │  (Python)   │  │   Engine    │  │  (OpenClaw)  │
   │  - Parser   │  │  - Rules    │  │  - Files     │
   │  - Intent   │  │  - Validate │  │  - Commands  │
   └──────┬──────┘  └─────┬───────┘  └────────┬─────┘
          │                │                   │
          └────────────────┼───────────────────┘
                           ▼
                  ┌──────────────────┐
                  │   SQLite DB      │
                  │   (Persistent)   │
                  │ • Users          │
                  │ • Audit Logs     │
                  │ • Reports        │
                  │ • Commands       │
                  └──────────────────┘
```

### Backend Components

1. **agent.py** - Main AI controller orchestrating the system
2. **intent.py** - Natural language parser for command understanding
3. **policy.py** - Policy engine for security validation
4. **enforce.py** - Security enforcement layer (CRITICAL)
5. **executor.py** - Action executor with OpenClaw integration
6. **logger.py** - Audit logging system
7. **backend_api.py** - Flask REST API with 21 endpoints
8. **models.py** - Data models for Intent, PolicyDecision, ExecutionResult

### Frontend Components

1. **pages/** - 6 complete pages (Login, Dashboard, Commands, Reports, Audit Logs, Settings)
2. **components/Layout/** - Reusable header, sidebar, footer components
3. **services/api.js** - Axios API client with interceptors
4. **store/** - Zustand state management (auth, commands, theme)

---

## 📁 Project Structure

```
airguard-ai/
│
├── 🎨 FRONTEND (React)
│   └── frontend/
│       ├── src/
│       │   ├── pages/
│       │   │   ├── Login.jsx              # Login page with JWT
│       │   │   ├── Dashboard.jsx          # Real-time metrics & trends
│       │   │   ├── Commands.jsx           # Execute monitoring commands
│       │   │   ├── Reports.jsx            # Generate & download reports
│       │   │   ├── AuditLogs.jsx          # View all system actions
│       │   │   └── Settings.jsx           # User & system settings
│       │   ├── components/
│       │   │   └── Layout/
│       │   │       ├── Header.jsx         # Nav with dark mode toggle
│       │   │       ├── Sidebar.jsx        # Navigation menu
│       │   │       └── Footer.jsx         # Footer with info
│       │   ├── services/
│       │   │   └── api.js                 # Axios API client
│       │   ├── store/
│       │   │   ├── authStore.js           # Auth state management
│       │   │   ├── commandStore.js        # Commands state
│       │   │   └── themeStore.js          # Dark mode state
│       │   └── App.jsx                    # Main app component
│       ├── package.json                   # Dependencies
│       ├── tailwind.config.js             # Tailwind CSS config
│       └── postcss.config.js
│
├── 🔧 BACKEND (Python/Flask)
│   ├── backend_api.py                     # Flask REST API (21 endpoints)
│   ├── agent.py                           # AI agent controller
│   ├── intent.py                          # NLP intent parser
│   ├── policy.py                          # Policy engine
│   ├── policy.json                        # Security policy rules
│   ├── enforce.py                         # Security enforcement
│   ├── executor.py                        # Action executor
│   ├── logger.py                          # Audit logging
│   ├── models.py                          # Data models
│   ├── main.py                            # Demo script
│   └── requirements_api.txt               # Python dependencies
│
├── 💾 DATA & LOGS
│   ├── airguard.db                        # SQLite database (auto-created)
│   ├── data/                              # Pollution data files
│   │   ├── delhi_pollution.json
│   │   ├── mumbai_pollution.json
│   │   ├── bangalore_pollution.json
│   │   └── ... (10+ cities)
│   └── output/                            # Generated reports
│
├── 📚 DOCUMENTATION
│   ├── AIRGUARD_PROFESSIONAL_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_INTEGRATION_COMPLETE.md
│   ├── GIT_PUSH_COMMANDS.md
│   └── README.md                          # This file
│
└── ⚙️ CONFIGURATION
    ├── .gitignore                         # Git ignore rules
    ├── .env.example                       # Environment variables template
    └── .vscode/                           # VS Code settings
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js 16+** and npm (for frontend)
- **Python 3.9+** and pip (for backend)
- Git

### Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: **http://localhost:3000**

Default credentials:
- Email: `admin@airguard.com`
- Password: `admin123`

### Backend Setup (Flask)

```bash
# Navigate to project root (if not already there)
cd ..

# Install Python dependencies
pip install -r requirements_api.txt

# Start Flask API server
python backend_api.py
```

Backend will be available at: **http://localhost:5000**

### Verify Installation

```bash
# Check frontend is running
curl http://localhost:3000

# Check backend is running
curl http://localhost:5000/api/health
```

---

## 🎮 Usage Guide

### 1. Login to Dashboard

- Navigate to http://localhost:3000
- Use credentials: `admin@airguard.com` / `admin123`
- JWT token is automatically stored in localStorage

### 2. View Real-Time Metrics

- Dashboard shows AQI levels for multiple cities
- Color-coded pollution levels (Green/Yellow/Orange/Red)
- Real-time trend charts and statistics

### 3. Execute Commands

- Go to **Commands** page
- Select action: Generate Report, Analyze AQI, Send Alert
- Commands are validated against security policies
- Dangerous actions are blocked (e.g., factory shutdown)

### 4. View Audit Logs

- Go to **Audit Logs** page
- See all executed commands with timestamps
- Filter by action, user, or date
- Download audit trail as CSV

### 5. Generate Reports

- Go to **Reports** page
- Select city and date range
- Click "Generate Report"
- Download as PDF or TXT
- Automatic file naming: `{city}_report_{timestamp}`

### 6. Manage Settings

- Go to **Settings** page
- Change password
- View user information
- Admin can manage other users (if admin role)

---

## 🔐 Security Features

### Authentication
- JWT-based authentication
- Secure password hashing (Flask-Security compatible)
- Token expiration and refresh mechanism
- Automatic token refresh on page reload

### Authorization
- Role-based access control (RBAC)
- Three roles: Admin, User, Viewer
- Policy-based command validation
- Dangerous actions blocked by default

### Policy Enforcement

**Allowed Actions:**
- `generate_report` - Read-only operation
- `analyze_aqi` - Data analysis operation
- `send_alert` - Public safety notification

**Blocked Actions:**
- `shutdown_factory` - Requires human authorization
- `issue_fine` - Requires legal review

**Default Policy:** DENY (fail-safe approach)

### Audit Logging

All system actions are automatically logged:
- User login/logout
- Commands executed
- Policy decisions (allow/block)
- Execution results
- Timestamps and user information

---

## � API Documentation

### Base URL
```
http://localhost:5000/api
```

### Key Endpoints

**Authentication:**
```
POST   /login              # Login with email/password
POST   /logout             # Logout current user
GET    /health             # Check API health
```

**Commands:**
```
POST   /process_command    # Execute a command
GET    /commands           # Get command history
POST   /commands/{id}      # Get command details
```

**Reports:**
```
GET    /reports            # Get all reports
POST   /reports            # Generate new report
GET    /reports/{id}       # Get report details
DELETE /reports/{id}       # Delete report
```

**Audit Logs:**
```
GET    /audit_logs         # Get all audit logs
GET    /audit_logs/{id}    # Get specific log entry
POST   /audit_logs/export  # Export logs to CSV
```

**User Management:**
```
GET    /users              # Get all users (admin only)
POST   /users              # Create new user (admin only)
PUT    /users/{id}         # Update user (admin only)
DELETE /users/{id}         # Delete user (admin only)
```

**Settings:**
```
GET    /settings           # Get system settings
PUT    /settings           # Update settings (admin only)
GET    /settings/profile   # Get user profile
PUT    /settings/profile   # Update user profile
```

### Example Request

```bash
# Generate pollution report
curl -X POST http://localhost:5000/api/reports \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Delhi",
    "date_range": "7days",
    "format": "pdf"
  }'
```

---

## 🗄️ Database Schema

### SQLite Tables

**Users Table**
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  is_active BOOLEAN DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP
);
```

**Audit Logs Table**
```sql
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) NOT NULL,
  command VARCHAR(255) NOT NULL,
  action VARCHAR(50) NOT NULL,
  policy_allowed BOOLEAN,
  policy_reason TEXT,
  status VARCHAR(20),
  execution_time FLOAT,
  result TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Reports Table**
```sql
CREATE TABLE report (
  id INTEGER PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  filename VARCHAR(255),
  location VARCHAR(100),
  file_size INTEGER,
  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER,
  file_path VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES user(id)
);
```

---

## 🌐 Supported Cities

The system monitors air pollution data for 12+ Indian cities:

- 🏙️ Delhi
- 🏙️ Mumbai
- 🏙️ Bangalore
- 🏙️ Chennai
- 🏙️ Kolkata
- 🏙️ Pune
- 🏙️ Hyderabad
- 🏙️ Jaipur
- 🏙️ Lucknow
- 🏙️ Nagpur
- 🏙️ Ahmedabad
- 🏙️ And more...

---

## 📞 Support

For questions or issues, contact the AirGuard AI team.

---

## 📄 License

This project is created for hackathon demonstration purposes.

---

**Built with ❤️ for cleaner air in Delhi**
