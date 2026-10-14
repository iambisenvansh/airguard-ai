# SQLite Database Integration - Complete

## Overview

The AirGuard AI backend has been fully integrated with SQLite database. All user data, audit logs, and reports are now persisted in a relational database instead of in-memory storage or files.

## Database Schema

### Tables

#### 1. **User Table**
Stores user accounts and authentication information.

```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'operator',
    email VARCHAR(120),
    last_login DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
)
```

**Roles:**
- `admin` - Full system access, user management, audit log review
- `operator` - Command execution, report generation, limited audit logs
- `viewer` - Read-only access to dashboards and reports

**Default Users (auto-created):**
- Username: `admin` | Password: `password123` | Role: `admin`
- Username: `operator` | Password: `password123` | Role: `operator`
- Username: `viewer` | Password: `password123` | Role: `viewer`

#### 2. **AuditLog Table**
Records all command executions, policy decisions, and results for compliance and debugging.

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER FOREIGN KEY REFERENCES user(id),
    username VARCHAR(80),
    command TEXT,
    action VARCHAR(50),
    policy_allowed BOOLEAN,
    policy_reason TEXT,
    status VARCHAR(20),
    execution_time FLOAT,
    result TEXT (JSON)
)
```

**Fields:**
- `timestamp` - When the command was executed
- `username` - Who executed it
- `command` - The natural language command text
- `action` - The parsed action type (e.g., generate_report, analyze_aqi)
- `policy_allowed` - Whether the policy allowed execution
- `policy_reason` - Why the policy allowed or blocked it
- `status` - success/error/blocked
- `execution_time` - How long execution took in seconds
- `result` - Full JSON response from backend

#### 3. **Report Table**
Tracks generated pollution analysis reports.

```sql
CREATE TABLE report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    filename VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(100),
    file_size INTEGER,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER FOREIGN KEY REFERENCES user(id),
    file_path VARCHAR(255)
)
```

**Fields:**
- `name` - Human-readable report name
- `filename` - Actual file name on disk
- `location` - Geographic location covered by report
- `file_size` - Size in bytes
- `file_path` - Full path to report file

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login with username/password
- `POST /api/auth/logout` - Logout (invalidates session)
- `POST /api/auth/refresh` - Refresh authentication token

### Audit Logs
- `GET /api/audit_logs` - Retrieve audit logs with optional filtering
  - Query params: `start_date`, `end_date` (ISO format)
  - Returns: Array of audit log entries
  - Access: Admin, Operator
- `POST /api/audit_logs` - Record a new audit log entry
  - Access: Internal (called by process_command endpoint)

### Reports
- `GET /api/reports` - List all reports
  - Returns: Array of report entries
  - Access: All authenticated users
- `POST /api/reports` - Create new report entry
  - Body: `{name, filename, location, file_size, file_path}`
  - Access: Internal (called by command processor)
- `GET /api/reports/<report_id>` - Download specific report file
  - Returns: File content
  - Access: All authenticated users
- `DELETE /api/reports/<report_id>` - Delete report and database entry
  - Access: Admin

### User Management
- `GET /api/users` - List all users
  - Returns: Array of user objects
  - Access: Admin only
- `POST /api/users` - Create new user
  - Body: `{username, password, role}`
  - Access: Admin only
- `DELETE /api/users/<user_id>` - Delete user
  - Access: Admin only

### System Status
- `GET /api/status` - Get pollution metrics and system status
  - Returns: Pollution metrics, timestamp, status
- `GET /api/system_status` - Get system statistics
  - Returns: Command counts, action breakdown, recent blocked actions
- `POST /api/process_command` - Execute natural language command
  - **NOW RECORDS TO AUDIT LOG AUTOMATICALLY**
  - Body: `{command: "natural language command"}`
  - Returns: Intent, policy decision, execution result

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements_api.txt
```

Required packages:
- Flask 3.0.0
- Flask-CORS 4.0.0
- **Flask-SQLAlchemy 3.1.1** (database ORM)
- PyJWT 2.8.1
- Python-dotenv 1.0.0

### 2. Run Backend

```bash
python backend_api.py
```

**First Run:**
- Database file `airguard.db` will be created automatically in project root
- Tables will be initialized
- Default users will be inserted

**Verification:**
- Backend runs on `http://localhost:5000`
- Health check: `curl http://localhost:5000/api/health`
- Expected: `{"status": "healthy", "timestamp": "..."}`

### 3. Test Database Integration

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"password123"}'
```

Expected response includes JWT token.

#### Get Audit Logs
```bash
curl -X GET http://localhost:5000/api/audit_logs \
  -H "Authorization: Bearer {token}"
```

#### Get Reports
```bash
curl -X GET http://localhost:5000/api/reports \
  -H "Authorization: Bearer {token}"
```

#### Execute Command (Records to Audit Log)
```bash
curl -X POST http://localhost:5000/api/process_command \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"Generate pollution report for Delhi"}'
```

This will:
1. Process the command through the AI agent
2. Automatically record the execution to the AuditLog table
3. Return the result to the frontend

## Data Persistence

### Where Data is Stored

- **Database File:** `airguard.db` (SQLite - in project root)
- **Report Files:** `output/` directory (actual report files on disk)
- **Database Metadata:** All timestamps, user info, command history in `airguard.db`

### Backup Strategy

To backup your data:

```bash
# Backup database
cp airguard.db airguard.db.backup

# Backup reports
cp -r output output.backup
```

To restore:

```bash
# Restore database
cp airguard.db.backup airguard.db

# Restore reports
cp -r output.backup output
```

## Key Features

### ✅ Complete Implementation

1. **User Authentication**
   - Stores users in database
   - Password-based authentication
   - JWT token generation and validation
   - Role-based access control

2. **Audit Logging**
   - All commands automatically recorded
   - Includes user, timestamp, command text, action type
   - Policy decisions and reasons recorded
   - Execution results stored as JSON

3. **Report Management**
   - Report metadata tracked in database
   - File references stored
   - Size and creation date tracked
   - User attribution for reports

4. **Transaction Safety**
   - All database operations use SQLAlchemy sessions
   - Proper rollback on errors
   - Foreign key relationships maintained

### 🔄 Real-World Workflows

#### Scenario 1: User Executes Command
1. Frontend sends command via `/api/process_command` with Bearer token
2. Backend validates token and authenticates user
3. AI agent processes command
4. **Audit log entry created automatically** with:
   - User ID and username
   - Command text
   - Parsed action type
   - Policy decision (allowed/blocked)
   - Execution status and time
   - Full result as JSON
5. Database transaction commits
6. Response sent to frontend

#### Scenario 2: Admin Reviews Audit Logs
1. Admin authenticates via `/api/auth/login`
2. Admin calls `GET /api/audit_logs` with Bearer token
3. Backend retrieves all audit logs from database
4. **Logs can be filtered by date range** using query parameters
5. Logs sorted newest first for compliance review

#### Scenario 3: Admin Manages Users
1. Admin creates new user via `POST /api/users`
2. New user stored in User table
3. Admin can list all users via `GET /api/users`
4. Admin can delete users via `DELETE /api/users/<id>`

## Database Monitoring

### Check Database Size

```bash
# Linux/Mac
ls -lh airguard.db

# Windows PowerShell
Get-Item airguard.db | Select-Object Length
```

### Query Database Directly

```bash
# Install sqlite3 command-line tool
sqlite3 airguard.db

# List tables
.tables

# Check user count
SELECT COUNT(*) FROM user;

# Check audit log count
SELECT COUNT(*) FROM audit_log;

# View recent audit logs
SELECT timestamp, username, command, action, policy_allowed 
FROM audit_log 
ORDER BY timestamp DESC 
LIMIT 10;
```

## Troubleshooting

### Issue: "Database is locked"
**Cause:** Multiple processes accessing database simultaneously
**Solution:** 
- Ensure only one backend instance is running
- Close any SQLite query tools that are open

### Issue: "User not found" after restart
**Cause:** Default users not created
**Solution:**
- Delete `airguard.db`
- Restart backend
- Default users will be re-created

### Issue: Audit logs not appearing
**Cause:** Command execution might be failing before logging
**Solution:**
- Check command processor logs
- Verify command format
- Check backend API response for errors

### Issue: Foreign key constraint error
**Cause:** Deleting a user with associated reports/logs
**Solution:**
- Delete associated reports first
- For audit logs, they reference user_id but don't cascade delete
- Consider archiving instead of deleting

## Next Steps

### For Development
1. ✅ Database fully integrated
2. Test with frontend by executing commands
3. Verify audit logs appear in real-time
4. Monitor report generation and tracking

### For Production
1. Change SECRET_KEY in `backend_api.py` line 23
2. Hash passwords instead of storing plaintext
3. Move database to secure location
4. Implement database backups
5. Add connection pooling for performance
6. Consider PostgreSQL for multi-user environment

### Future Enhancements
- Add database indexes for performance
- Implement data retention policies
- Add encrypted password hashing (bcrypt)
- Add database migrations tool (Alembic)
- Implement API rate limiting per user

## Support

For questions about database integration, check:
- `backend_api.py` - All database models and endpoints
- `requirements_api.txt` - Required dependencies
- `.kiro/specs/airguard-frontend/` - Requirements and design docs

Run `python backend_api.py` and visit `http://localhost:5000/api/health` to verify everything is working.

---

**Status: ✅ Complete** - SQLite database fully integrated with all endpoints working.
