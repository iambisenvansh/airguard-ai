# AirGuard API Usage Examples

## Quick Reference

### Base URL
```
http://localhost:5000
```

### Authentication
All endpoints (except `/api/health`) require Bearer token in header:
```
Authorization: Bearer <token_from_login>
```

---

## Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

**Response:** Returns JWT token to use in headers

---

## Execute Command (Auto-Records to Audit Log)

```bash
curl -X POST http://localhost:5000/api/process_command \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Generate pollution report for Delhi"
  }'
```

**What happens:**
1. Command processed by AI agent
2. Policy decision made (allowed/blocked)
3. **Audit log entry AUTOMATICALLY saved to database**
4. Result returned to frontend

---

## Get Audit Logs (Database-Backed)

```bash
# Get all logs
curl -X GET http://localhost:5000/api/audit_logs \
  -H "Authorization: Bearer TOKEN"

# Get logs from specific date range
curl -X GET "http://localhost:5000/api/audit_logs?start_date=2024-01-15T00:00:00&end_date=2024-01-15T23:59:59" \
  -H "Authorization: Bearer TOKEN"
```

**Response:** Array of audit log entries with all command history

---

## User Management (Admin Only)

```bash
# Get all users
curl -X GET http://localhost:5000/api/users \
  -H "Authorization: Bearer TOKEN"

# Create new user
curl -X POST http://localhost:5000/api/users \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newop",
    "password": "securepass",
    "role": "operator"
  }'

# Delete user
curl -X DELETE http://localhost:5000/api/users/4 \
  -H "Authorization: Bearer TOKEN"
```

---

## Reports Management

```bash
# Get all reports
curl -X GET http://localhost:5000/api/reports \
  -H "Authorization: Bearer TOKEN"

# Download report
curl -X GET http://localhost:5000/api/reports/1 \
  -H "Authorization: Bearer TOKEN" \
  --output report.txt

# Delete report
curl -X DELETE http://localhost:5000/api/reports/1 \
  -H "Authorization: Bearer TOKEN"
```

---

## Database Queries

Direct SQLite queries:

```bash
sqlite3 airguard.db
```

```sql
-- View all audit logs
SELECT timestamp, username, command, action, policy_allowed FROM audit_log ORDER BY timestamp DESC;

-- Count commands by user
SELECT username, COUNT(*) FROM audit_log GROUP BY username;

-- View all users
SELECT id, username, role, email, is_active FROM user;

-- View reports
SELECT id, name, location, date_created FROM report ORDER BY date_created DESC;
```

---

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | password123 | Full access |
| operator | password123 | Execute commands |
| viewer | password123 | Read-only |

---

## What's New: Database Integration

✅ **All data now persists in SQLite:**
- User logins and roles stored in database
- Commands automatically logged to audit_log table
- Reports tracked in report table
- Survives backend restarts

✅ **Audit Log Recording:**
- Triggered automatically when `/api/process_command` executes
- Includes: user, command text, action, policy decision, result
- Retrievable via `GET /api/audit_logs`
- Filterable by date range

✅ **No Setup Required:**
- Database auto-created on first run
- Tables auto-initialized
- Default users auto-inserted
