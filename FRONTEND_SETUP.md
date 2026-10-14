# AirGuard AI - React Frontend Setup Guide

## 📋 Overview

This is a complete React-based web frontend for the AirGuard AI pollution monitoring system. It provides a user-friendly interface for:
- Real-time pollution monitoring dashboards
- Natural language command execution
- Report generation and management
- Audit log review and analysis
- User and system administration

## 🏗️ Architecture

```
Frontend (React)
    ↓
    ├── API Client (axios)
    │   ├── Authentication Service
    │   ├── Command Execution
    │   ├── Status Updates
    │   └── Audit Logging
    ↓
Backend API (Flask) - backend_api.py
    ↓
    └── AirGuard AI System (Python)
        ├── Intent Parser
        ├── Policy Engine
        ├── Security Enforcer
        ├── Executor
        └── Audit Logger
```

## 🚀 Quick Start

### Prerequisites
- Node.js 14+ and npm
- Python 3.9+
- Flask and dependencies

### Step 1: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### Step 2: Backend API Setup

```bash
# Install Python dependencies for backend API
pip install flask flask-cors pyjwt

# Run the backend API server
python backend_api.py
```

The API will be available at `http://localhost:5000`

### Step 3: Login

Use demo credentials:
- **Admin**: `admin` / `password123`
- **Operator**: `operator` / `password123`
- **Viewer**: `viewer` / `password123`

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML entry point
├── src/
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── Commands.jsx        # Command execution
│   │   ├── AuditLogs.jsx       # Audit log viewer
│   │   ├── Reports.jsx         # Report management
│   │   └── Settings.jsx        # Admin settings
│   ├── components/
│   │   └── Layout/
│   │       ├── Header.jsx      # Navigation header
│   │       └── Layout.jsx      # Page wrapper
│   ├── services/
│   │   └── api.js              # API client with interceptors
│   ├── store/
│   │   ├── authStore.js        # Authentication state
│   │   └── commandStore.js     # Command history state
│   ├── App.jsx                 # Main application
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── .env.example

backend_api.py                  # Flask API server
FRONTEND_SETUP.md              # This file
```

## 🔑 Features

### 1. Authentication & Authorization
- Role-based access control (Admin, Operator, Viewer)
- JWT token-based authentication
- Session management
- Secure token storage

### 2. Dashboard
- Real-time pollution metrics (PM2.5, PM10, NO2, SO2, CO, O3)
- System statistics and command analytics
- Action distribution charts
- Command volume trends
- Recent blocked actions display

### 3. Command Interface
- Natural language command input
- Command suggestions and autocomplete
- Command history with persistence
- Favorite commands management
- Clear response display with:
  - Parsed intent details
  - Policy decision explanation
  - Execution results

### 4. Report Management
- View and download generated reports
- Filter reports by location and date
- Storage statistics
- Report deletion with confirmation

### 5. Audit Logging
- Complete command execution history
- Real-time filtering and search
- Status tracking (SUCCESS/BLOCKED/ERROR)
- CSV export functionality
- Pagination for large datasets

### 6. Settings (Admin Only)
- User management (create, edit, delete)
- Notification preferences
- Backend API configuration
- System information display

## 🔒 Security Features

### Frontend Security
- HTTPS-only communication
- Input sanitization and XSS prevention
- CSRF protection
- Secure token storage in HttpOnly cookies
- Content Security Policy headers
- Rate limiting on login attempts

### Backend Security
- JWT token validation
- Role-based access control
- Request authentication checks
- Policy-based authorization
- Audit logging of all operations
- Error message sanitization

## 🎨 User Interface

### Responsive Design
- Desktop optimized (1024px+)
- Tablet support (768px+)
- Mobile support (320px+)
- Collapsible mobile menu

### Accessibility
- Semantic HTML
- ARIA labels for screen readers
- Keyboard navigation support
- WCAG AA color contrast compliance
- Form validation with error announcements

### Visual Hierarchy
- Color-coded severity levels:
  - Green: Good/Allowed
  - Yellow: Moderate
  - Orange: Poor/Blocked
  - Red: Critical/Error
- Clear status indicators
- Intuitive icon usage

## 🔌 API Integration

### Endpoints Used

**Authentication**
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Token refresh

**Commands**
- `POST /api/process_command` - Execute command

**Status**
- `GET /api/status` - Current metrics
- `GET /api/system_status` - System statistics

**Audit Logs**
- `GET /api/audit_logs` - Retrieve logs with filtering

**Reports**
- `GET /api/reports` - List all reports
- `GET /api/reports/<filename>` - Download report
- `DELETE /api/reports/<filename>` - Delete report

**User Management** (Admin only)
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `DELETE /api/users/<id>` - Delete user

**Settings** (Admin only)
- `GET /api/settings` - Get settings
- `PUT /api/settings` - Update settings

## 🌍 Internationalization

### Supported Languages
- English (default)
- Hindi (हिंदी)

Switch language using the language selector in the header.

## 📊 Data Flow

### Command Execution Flow
```
User Input
    ↓
Frontend: Natural Language Command
    ↓
API Call: POST /api/process_command
    ↓
Backend: Intent Parser
    ↓
Backend: Policy Engine
    ↓
Backend: Security Enforcer
    ↓
Decision: Allow/Block
    ↓
Backend: Executor (if allowed)
    ↓
Response: Intent + Decision + Result
    ↓
Frontend: Display Response
    ↓
State: Store in History
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Login with each role (admin, operator, viewer)
- [ ] Execute allowed commands
- [ ] Execute blocked commands
- [ ] View real-time dashboard updates
- [ ] Test search and filtering
- [ ] Export audit logs
- [ ] Download reports
- [ ] Test responsive design on mobile
- [ ] Test keyboard navigation
- [ ] Test error handling with offline backend

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'

# Test command execution (with token)
curl -X POST http://localhost:5000/api/process_command \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"command": "Generate pollution report for Delhi"}'
```

## 📦 Dependencies

### Frontend Dependencies
- `react` - UI framework
- `react-dom` - React DOM renderer
- `react-router-dom` - Client-side routing
- `axios` - HTTP client
- `recharts` - Data visualization
- `date-fns` - Date utilities
- `lucide-react` - Icon library
- `zustand` - State management
- `tailwindcss` - CSS framework

### Backend Dependencies
- `flask` - Web framework
- `flask-cors` - CORS handling
- `pyjwt` - JWT tokens
- `python-dotenv` - Environment variables (optional)

## 🚢 Deployment

### Production Build

```bash
# Frontend
cd frontend
npm run build

# Serve with production web server (nginx, Apache, etc.)

# Backend
gunicorn -w 4 backend_api:app
```

### Environment Variables

**.env file**
```
REACT_APP_API_URL=https://your-api-domain.com/api
REACT_APP_NAME=AirGuard AI
```

### Docker Deployment

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]

# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "backend_api:app"]
```

## 🐛 Troubleshooting

### Frontend Issues

**"Cannot connect to backend service"**
- Check if backend is running on the correct port
- Verify API URL in settings or .env file
- Check CORS configuration in backend_api.py

**"Session expired"**
- Token has expired (24 hour expiry by default)
- Login again to get a new token

**Commands not appearing in history**
- Check browser localStorage is enabled
- Clear browser cache if experiencing issues

### Backend Issues

**"Module not found" errors**
- Install dependencies: `pip install flask flask-cors pyjwt`
- Ensure Python path includes project directory

**CORS errors**
- Backend CORS is configured to allow all origins in development
- Update in production for security

**401 Unauthorized errors**
- Verify token is being sent in Authorization header
- Check token expiration time
- Ensure token format is "Bearer <token>"

## 📝 Configuration

### API Configuration
Edit `backend_api.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

### JWT Token Expiry
Edit `backend_api.py`:
```python
'exp': datetime.utcnow() + timedelta(hours=24)  # Change hours as needed
```

### Polling Interval
Edit `frontend/src/pages/Dashboard.jsx`:
```javascript
const interval = setInterval(fetchData, 30000); // 30 seconds
```

## 🤝 Integration with Backend

The frontend expects the backend to provide specific API responses. The `backend_api.py` wrapper handles this, but you can also:

1. Modify `backend_api.py` to add more endpoints
2. Update `frontend/src/services/api.js` to call new endpoints
3. Create new pages in `frontend/src/pages/` for new features

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios](https://axios-http.com/)
- [Recharts](https://recharts.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [JWT Documentation](https://jwt.io/)

## 📞 Support

For issues or questions:
1. Check this setup guide
2. Review the troubleshooting section
3. Check browser console for errors
4. Check backend logs for API errors
5. Verify all services are running

## 📄 License

This frontend is part of the AirGuard AI system and follows the same license as the main project.

---

**Built with ❤️ for cleaner air in Delhi**
