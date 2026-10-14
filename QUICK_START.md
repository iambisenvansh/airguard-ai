# 🚀 AirGuard AI - Quick Start (5 minutes)

## ⚡ TL;DR - Get Running Fast

### Prerequisites
- Node.js 14+ (check: `node --version`)
- Python 3.9+ (check: `python --version`)

### Start in 3 terminals

**Terminal 1: Backend API**
```bash
pip install flask flask-cors pyjwt
python backend_api.py
```
✅ Shows: `Running on http://0.0.0.0:5000`

**Terminal 2: Frontend**
```bash
cd frontend
npm install
npm start
```
✅ Browser opens: `http://localhost:3000`

**Terminal 3: Done!**
```
Login with: admin / password123
```

## 🎮 What to Try First

1. **Login** - Use `admin` / `password123`
2. **Dashboard** - See real-time pollution metrics
3. **Commands** - Try: `"Generate pollution report for Delhi"`
4. **Audit Logs** - See all commands executed
5. **Settings** - (Admin only) Manage users

## 📊 Test Commands

Copy-paste these to test the system:

```
✅ Allowed:
- Generate pollution report for Delhi
- Analyze AQI in Delhi
- Send critical alert about high pollution

❌ Blocked:
- Shutdown factory in Mayapuri
- Issue fine to polluting factory
```

## 🔑 Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | password123 |
| Operator | operator | password123 |
| Viewer | viewer | password123 |

## 📁 Key Files

```
frontend/           ← React website
backend_api.py      ← Flask API server
FRONTEND_SETUP.md   ← Detailed frontend guide
FULL_STACK_GUIDE.md ← Complete system guide
```

## 🆘 Troubleshooting

### "Cannot connect to backend"
- Is backend running? Check Terminal 1

### "npm not found"
- Install Node.js from https://nodejs.org/

### "No such file: python"
- Install Python from https://python.org/

### API calls showing 404
- Backend must be running on port 5000
- Restart: `python backend_api.py`

## 🎯 Next Steps

1. **Explore** - Try all features in the UI
2. **Modify** - Edit `frontend/src/pages/` to customize
3. **Deploy** - See `FULL_STACK_GUIDE.md` for production
4. **Integrate** - Connect to real pollution data

## 📚 Full Documentation

- **Frontend Only**: Read `FRONTEND_SETUP.md`
- **Complete System**: Read `FULL_STACK_GUIDE.md`
- **Backend Only**: See `README.md` and `ARCHITECTURE.md`

## 🎨 Quick Customization

### Change the title
Edit `frontend/public/index.html`:
```html
<title>Your Title Here</title>
```

### Change colors
Edit `frontend/tailwind.config.js`:
```javascript
green: { 600: '#your-color-here' }
```

### Change API URL
Edit `frontend/.env`:
```
REACT_APP_API_URL=http://your-api:5000/api
```

## ⏱️ Expected Build Times

- Frontend install: ~2 minutes (first time)
- Backend start: ~2 seconds
- Frontend start: ~1 minute
- **Total first-time setup: ~5 minutes**

## 🚢 Quick Deployment Checklist

- [ ] Frontend: `npm run build`
- [ ] Backend: Run with `gunicorn`
- [ ] Nginx: Reverse proxy setup
- [ ] HTTPS: SSL certificate
- [ ] Database: User storage
- [ ] Monitoring: Error tracking

## 🎓 Architecture at a Glance

```
User (Browser)
    ↓
React App (Port 3000)
    ↓
Flask API (Port 5000)
    ↓
Python Backend
    ↓
Database & Files
```

## 💡 Pro Tips

1. **Hotkey**: Press F12 in browser for DevTools
2. **Mobile**: Test on phone with `npm start` showing URL
3. **Offline**: Frontend works without backend (limited)
4. **Logs**: Check browser console for errors
5. **Shortcuts**: Use keyboard nav (Tab, Enter)

## 🐛 Report Issues

If something breaks:

1. Check terminal output for errors
2. Look at browser console (F12 → Console)
3. Restart both servers
4. Clear browser cache
5. Check firewall isn't blocking ports

## 📞 More Help

- **Frontend Issues**: See `FRONTEND_SETUP.md`
- **Backend Issues**: See `README.md`
- **System Design**: See `ARCHITECTURE.md`
- **Full Guide**: See `FULL_STACK_GUIDE.md`

---

**Done? You're running AirGuard AI! 🎉**

Now explore the interface and try the features. Have fun! 🚀

