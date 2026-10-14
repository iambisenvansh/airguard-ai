# What to Expect - AirGuard AI System

## When You Start the System

### Backend Starting

**Terminal 1 Output:**
```
✅ Default users created in database
* Running on http://0.0.0.0:5000/
```

**What's Happening:**
1. SQLite database created: `airguard.db`
2. Tables initialized: User, AuditLog, Report
3. Default users inserted:
   - admin/password123 (full access)
   - operator/password123 (execute commands)
   - viewer/password123 (read-only)
4. Flask development server started
5. API listening on port 5000

---

### Frontend Starting

**Terminal 2 Output:**
```
> airguard-ai-frontend@1.0.0 start
> react-scripts start
...
Compiled successfully

You can now view airguard-ai-frontend in the browser.

  Local:   http://localhost:3000
  Network: http://192.168.x.x:3000
```

**Browser:**
- Automatically opens to `http://localhost:3000`
- Login page displayed
- Ready for credentials

---

## Login & First Interaction

### Login Page Appearance
```
┌─────────────────────────┐
│   AirGuard AI           │
│   Pollution Control     │
│                         │
│ Username: [_________]   │
│ Password: [_________]   │
│           [Login]       │
│                         │
│ © 2024 AirGuard AI      │
└─────────────────────────┘
```

**Try:** `admin` / `password123`

---

## Dashboard After Login

### What You'll See
```
┌─────────────────────────────────────────────┐
│ AirGuard AI | Home | Commands | Logs | ...  │ ☀️
├─────────────────────────────────────────────┤
│                                             │
│  Real-Time Pollution Metrics                │
│  ┌──────────────┬──────────────┐           │
│  │ PM2.5: 85    │ PM10: 120    │           │
│  │ (Poor)       │ (Poor)       │           │
│  └──────────────┴──────────────┘           │
│  ┌──────────────┬──────────────┐           │
│  │ NO2: 45      │ AQI: 95      │           │
│  │ (Moderate)   │ (Poor)       │           │
│  └──────────────┴──────────────┘           │
│                                             │
│  System Status: Online                      │
│  Last Update: 30 seconds ago                │
│                                             │
└─────────────────────────────────────────────┘
```

**Color Coding:**
- 🟢 Green (Good) - 0-50
- 🟡 Yellow (Moderate) - 51-100
- 🟠 Orange (Poor) - 101-150
- 🔴 Red (Critical) - 151+

---

## Commands Page Interaction

### What You'll See
```
┌─────────────────────────────────────────────┐
│ AirGuard AI | Home | Commands | Logs | ...  │
├─────────────────────────────────────────────┤
│                                             │
│ Enter a natural language command:           │
│ ┌─────────────────────────────────────────┐ │
│ │ Generate pollution report for Delhi     │ │
│ └─────────────────────────────────────────┘ │
│                               [Submit]      │
│                                             │
│ Suggested Commands:                         │
│ • Generate pollution report for [city]      │
│ • Show current AQI for Mumbai               │
│ • Alert for pollution spike in Delhi        │
│                                             │
│ ──────────────────────────────────────────  │
│                                             │
│ Response (After Submit):                    │
│                                             │
│ Parsed Intent:                              │
│ • Action: generate_report                   │
│ • Location: Delhi                           │
│ • Confidence: 0.95                          │
│                                             │
│ Policy Decision:                            │
│ ✅ ALLOWED - Operator role authorized      │
│                                             │
│ Result:                                     │
│ ✅ Report generated successfully            │
│ 📄 pollution_report_delhi_2024_01_15.txt    │
│ ⏱️  Executed in 2.5 seconds                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Audit Logs Page

### What You'll See
```
┌─────────────────────────────────────────────┐
│ AirGuard AI | Home | Commands | Logs | ...  │
├─────────────────────────────────────────────┤
│                                             │
│ Audit Logs (Filtering from Database)        │
│                                             │
│ Date Range: [from] [to]  [Search]  [Export]│
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Time  │ User     │ Command │ Status     │ │
│ ├─────────────────────────────────────────┤ │
│ │ 10:35 │ admin    │ Generate│ ✅ Success │ │
│ │       │          │ report  │ (2.5s)    │ │
│ ├─────────────────────────────────────────┤ │
│ │ 10:30 │ operator │ Show AQI │ ✅ Success │ │
│ │       │          │ for Delhi│ (0.8s)    │ │
│ ├─────────────────────────────────────────┤ │
│ │ 10:25 │ viewer   │ Generate│ ❌ Blocked │ │
│ │       │          │ alert   │ Permission│ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Click entry to see full JSON details        │
│                                             │
└─────────────────────────────────────────────┘
```

**Key Feature:** All data comes from SQLite database, searchable by date

---

## Dark Mode Toggle

### Light Mode (Default)
```
┌─────────────────────────────────┐
│ AirGuard AI | ... | ☀️          │ Light background
├─────────────────────────────────┤
│ Dashboard with light colors     │
│ Black text on white background  │
└─────────────────────────────────┘
```

### Dark Mode (Premium)
```
┌─────────────────────────────────┐
│ AirGuard AI | ... | 🌙          │ Dark background
├─────────────────────────────────┤
│ Dashboard with dark colors      │
│ Green glowing accents           │
│ Glassmorphism effects           │
│ Smooth 0.3s transitions         │
└─────────────────────────────────┘
```

**To Toggle:** Click moon/sun icon in top-right corner

---

## Database in Action

### Command Execution Flow

**User Action:**
```
Frontend: "Generate pollution report for Delhi"
```

**Backend Processing:**
```
1. Receive command
2. Authenticate user ✅
3. Process with AI agent ✅
4. Make policy decision ✅
5. Create AuditLog entry ✅
6. Commit to database ✅
7. Return result ✅
```

**Database Result:**
```sql
sqlite> SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 1;
id: 1
timestamp: 2024-01-15 10:35:00
username: admin
command: Generate pollution report for Delhi
action: generate_report
policy_allowed: 1 (TRUE)
status: success
execution_time: 2.5
result: {...JSON response...}
```

### How to Verify

**Check Backend Console:**
```
✅ Default users created in database
* Running on http://0.0.0.0:5000/
  GET /api/auth/login
  POST /api/process_command
  ✅ Audit log recorded
```

**Check Database Directly:**
```bash
sqlite3 airguard.db
SELECT username, command, policy_allowed FROM audit_log ORDER BY timestamp DESC;
```

**Check Frontend:**
- Go to Audit Logs page
- Your command should appear
- Click to see full details

---

## Reports Management

### After Generating Report

**Reports Page Shows:**
```
┌─────────────────────────────────┐
│ Generated Reports               │
├─────────────────────────────────┤
│ Name: Delhi Pollution Report    │
│ Location: Delhi                 │
│ Generated: 2024-01-15 10:35     │
│ Size: 1.2 MB                    │
│ [View] [Download] [Delete]      │
└─────────────────────────────────┘
```

**In Database:**
```sql
sqlite> SELECT * FROM report ORDER BY date_created DESC;
id: 1
name: Delhi Pollution Report
filename: pollution_report_delhi_2024_01_15.txt
location: Delhi
date_created: 2024-01-15 10:35:00
file_size: 1200000
file_path: output/pollution_report_delhi_2024_01_15.txt
```

---

## Settings Page (Admin)

### What Admin Sees
```
┌─────────────────────────────────────┐
│ Settings (Admin Access Only)         │
├─────────────────────────────────────┤
│                                     │
│ [Users] [Notifications] [Backend]   │
│                                     │
│ Users Tab:                          │
│ ┌──────────────────────────────────┐│
│ │ User     │ Role     │ Last Login  ││
│ ├──────────────────────────────────┤│
│ │ admin    │ admin    │ 10:35      ││
│ │ operator │ operator │ 10:30      ││
│ │ viewer   │ viewer   │ Never      ││
│ └──────────────────────────────────┘│
│                                     │
│ [+ Create User] [Edit] [Deactivate] │
│                                     │
└─────────────────────────────────────┘
```

**All changes stored in database**

---

## Mobile View

### Responsive Design
```
Phone (320px):
┌─────────────┐
│ ☀️ AirGuard │
├─────────────┤
│ [≡]         │
│             │
│ Dashboard   │
│ PM2.5: 85   │
│ AQI: 95     │
│             │
│ [Submit]    │
│             │
│ Recent Logs │
│ ...         │
│             │
└─────────────┘
```

**Features:**
- Hamburger menu instead of navbar
- Full-width components
- Touch-friendly buttons
- Scrollable content

---

## Error Scenarios

### Backend Connection Failed
```
❌ Cannot connect to backend service
  http://localhost:5000

[Retry] [Settings]

Make sure:
• Backend is running
• Port 5000 is available
• Firewall allows connections
```

### Authentication Failed
```
❌ Invalid credentials

Username or password is incorrect.
Try: admin / password123

[Try Again]
```

### Command Blocked by Policy
```
❌ Command Blocked

Action: shutdown_factory
Reason: Critical infrastructure control 
        requires human authorization

Suggested Actions:
• Contact administrator
• Use a different command
• Check audit logs
```

---

## Performance Indicators

### Good Performance
- ✅ Page loads in <2 seconds
- ✅ API responds in <500ms
- ✅ Dark mode toggle in <100ms
- ✅ Database queries in <100ms
- ✅ Smooth animations and transitions

### What You Should NOT See
- ❌ Long loading spinners (>5 seconds)
- ❌ White blank pages
- ❌ "Cannot connect" errors on startup
- ❌ 500 errors in console
- ❌ Laggy dark mode toggle

---

## System Health Indicators

### All Good ✅
```
Backend:  http://localhost:5000/api/health
Response: {"status": "healthy", "timestamp": "..."}

Database: airguard.db exists and is readable
Reports:  output/ directory exists

Frontend: http://localhost:3000 loads
Console:  No critical errors
Network:  All API calls successful
```

### Issues to Watch For ❌
```
Backend won't start:
• Check dependencies: pip install -r requirements_api.txt
• Check port 5000: netstat -an | grep 5000

Frontend won't connect:
• Verify backend is running
• Check API base URL in frontend/src/services/api.js

Database errors:
• Delete airguard.db and restart (it will recreate)
• Check permissions on project directory
```

---

## Typical User Journey

### Day 1: First Login
1. Run `RUN_SYSTEM.md` instructions
2. Navigate to http://localhost:3000
3. Login with admin/password123
4. Explore Dashboard page
5. Try a command
6. View audit logs
7. Confirm data in database

### Day 2: Testing Features
1. Switch to dark mode
2. Test different roles (operator, viewer)
3. Check permission enforcement
4. Generate and download reports
5. Filter audit logs by date

### Day 3: Production Prep
1. Review `FINAL_CHECKLIST.md`
2. Plan security hardening
3. Set up database backups
4. Plan deployment strategy

---

## What's Happening Behind the Scenes

### When You Execute a Command

```
Frontend                Backend           Database
   │                      │                  │
   ├─ Command ───────────→│                  │
   │  with Bearer token   │                  │
   │                      ├─ Process ────────│
   │                      ├─ Policy check    │
   │                      ├─ ✅ Log entry ──→│
   │                      │  (AUTO-SAVED)    │
   │                      ├─ Commit ─────────│
   │                      │                  │
   │ ←─ Response ────────┤                  │
   │  with result        │                  │
   │                     │                  │
   └─ Display ──────────→                   │
      in UI               User sees         Data persists
      and stores          result            in database
      in history          immediately       forever
```

---

## Summary: What to Expect

✅ **On Startup:**
- Backend creates database automatically
- Frontend loads in browser
- System ready in <30 seconds

✅ **On Login:**
- Credentials validated against database
- JWT token issued
- Dashboard displays with real data

✅ **On Command Execution:**
- Command auto-logged to database
- Audit logs immediately available
- Data survives backend restart

✅ **Overall:**
- Professional, responsive interface
- Fast, reliable backend
- Persistent data in SQLite
- Complete audit trail
- Role-based access control

---

**You're ready to use AirGuard AI! Follow `RUN_SYSTEM.md` to get started.**
