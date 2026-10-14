# 🚀 AirGuard AI - Quick Start (2 Minutes)

## What You'll Get
A complete full-stack web application with:
- ✅ React frontend with dark mode
- ✅ Flask REST API backend
- ✅ SQLite database (auto-created)
- ✅ Role-based access control
- ✅ Real-time pollution dashboard
- ✅ Audit logging system

---

## Step 1: Install Backend Dependencies

**Open Terminal/PowerShell in project root**

```bash
pip install -r requirements_api.txt
```

**Expected output:** Successfully installed flask, flask-cors, flask-sqlalchemy, pyjwt, python-dotenv, gunicorn

---

## Step 2: Start Backend

**Keep Terminal 1 open, run:**

```bash
python backend_api.py
```

**Expected output:**
```
✅ Default users created in database
* Running on http://0.0.0.0:5000/
```

⚠️ **Leave this running - don't close this terminal!**

✅ Database file created: `airguard.db`

---

## Step 3: Start Frontend

**Open NEW Terminal in project root**

```bash
cd frontend
npm install
npm start
```

**Expected output:**
```
Compiled successfully
Local:   http://localhost:3000/
```

Browser will auto-open to login page. If not, visit: **http://localhost:3000**

---

## Step 4: Login & Test

**Use any of these credentials:**

| Username | Password | Role |
|----------|----------|------|
| admin | password123 | Full access |
| operator | password123 | Execute commands |
| viewer | password123 | Read-only |

**After login, you'll see:**
- 📊 Dashboard with pollution metrics
- ⚡ Commands page to execute natural language commands
- 📋 Audit logs of all executions
- 📄 Reports page
- ⚙️ Settings page

---

## Step 5: Test Database Integration

**Try this workflow:**

1. Go to **Commands** page
2. Enter command: `Generate pollution report for Delhi`
3. Click Submit
4. View the response (should show parsed intent and policy decision)
5. Go to **Audit Logs** page
6. Your command should appear in the list (auto-recorded to database!)
7. Click the entry to see full details

**Check Database Directly:**
```bash
sqlite3 airguard.db "SELECT username, command, policy_allowed FROM audit_log ORDER BY timestamp DESC LIMIT 1;"
```

Should show your command!

---

## 🎨 Features to Try

### Dark Mode
- Click moon icon in top-right
- Toggle dark/light themes
- Preference persists across sessions

### Audit Logs
- Filter by date range
- Search by user or command
- Sort by any column
- View full JSON details

### Reports
- View generated reports
- Download report files
- Delete reports (admin only)

### User Management (Admin Only)
- Go to Settings → Users
- Create new users with roles
- Deactivate users

---

## ❌ Troubleshooting

### "Backend connection error" on frontend
**Solution:** Verify backend is running on port 5000
```bash
# Terminal 1 should show:
* Running on http://0.0.0.0:5000/
```

### "Cannot import Flask-SQLAlchemy"
**Solution:** Reinstall dependencies
```bash
pip install -r requirements_api.txt --force-reinstall
```

### Port already in use
**Change port in backend:**
```python
# Edit backend_api.py, last line:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### npm: command not found
**Install Node.js from:** https://nodejs.org

---

## 📁 What Gets Created

After first run, you'll have:

```
airguard.db          ← SQLite database (persistent storage)
├─ User table        ← Stores login credentials & roles
├─ AuditLog table    ← Logs all command executions
└─ Report table      ← Tracks generated reports

output/              ← Generated report files
frontend/
├─ node_modules/    ← Downloaded dependencies
├─ src/
│  ├─ pages/        ← 6 React pages (Login, Dashboard, etc.)
│  ├─ store/        ← Zustand state management
│  └─ services/     ← API client
└─ ...
```

---

## 🔐 Security Notes (Development Only)

This is configured for development. For production:

1. **Change SECRET_KEY** in `backend_api.py` (line 23)
2. **Hash passwords** with bcrypt (don't store plaintext)
3. **Use HTTPS** instead of HTTP
4. **Set DEBUG=False** in Flask
5. **Use PostgreSQL** instead of SQLite for multi-user

---

## 📊 System Workflow

```
1. User logs in (Frontend)
   ↓
2. Credentials sent to /api/auth/login (Backend)
   ↓
3. Backend validates & returns JWT token
   ↓
4. User executes command (Frontend)
   ↓
5. Command sent to /api/process_command with token (Backend)
   ↓
6. Command processed by AI agent
   ↓
7. Audit log AUTOMATICALLY recorded to database
   ↓
8. Result returned to frontend
   ↓
9. User views audit logs (pulls from database)
```

---

## 💡 Key Endpoints

After backend starts on port 5000, try these:

**Health Check (no auth needed):**
```bash
curl http://localhost:5000/api/health
# Response: {"status": "healthy", "timestamp": "..."}
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"password123"}'
# Response includes: {"token": "eyJ...", "user": {...}}
```

**Get Audit Logs (requires token):**
```bash
curl -X GET http://localhost:5000/api/audit_logs \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
# Response: {"logs": [{...}, {...}]}
```

---

## 🎯 What Works Out of the Box

✅ User login with 3 default roles  
✅ Natural language command execution  
✅ Automatic audit log recording  
✅ Real-time pollution dashboard  
✅ Report generation & tracking  
✅ Dark mode with premium styling  
✅ Responsive mobile design  
✅ Role-based access control  
✅ JWT authentication  
✅ SQLite database persistence  

---

## 📚 More Information

**See these files for details:**
- `PROJECT_STATUS.md` - Complete project overview
- `DATABASE_INTEGRATION_COMPLETE.md` - Database setup & queries
- `FULL_STACK_GUIDE.md` - Architecture details
- `FRONTEND_SETUP.md` - React component documentation
- `DARK_MODE_SETUP.md` - Dark mode implementation

---

## 🚨 Common Mistakes

❌ Only running backend (frontend shows "cannot connect")  
→ Start BOTH: backend in Terminal 1, `cd frontend && npm start` in Terminal 2

❌ Closing backend terminal  
→ Backend keeps running - if you close it, API stops working

❌ Using wrong credentials  
→ Use exactly: admin/password123 or operator/password123 or viewer/password123

❌ Frontend port 3000 already used  
→ Edit `frontend/package.json` and add `"PORT": 3001` to scripts

---

## ✅ You're Ready!

Your system is now running:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000
- **Database:** airguard.db (auto-created)

**Enjoy! 🎉**

---

**Need help?** Check PROJECT_STATUS.md or DATABASE_INTEGRATION_COMPLETE.md for detailed guides.
