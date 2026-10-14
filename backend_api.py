"""
Flask API wrapper for AirGuard AI Frontend
Provides REST API endpoints for the React frontend
Now with SQLite database support!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import json
import os
from datetime import datetime, timedelta
from agent import AirGuardAgent
from logger import AuditLogger
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
db = SQLAlchemy(app)

# Initialize components
agent = AirGuardAgent()
logger = AuditLogger()

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for database"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator')
    email = db.Column(db.String(120))
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class AuditLog(db.Model):
    """Audit log model for database"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(80))
    command = db.Column(db.Text)
    action = db.Column(db.String(50))
    policy_allowed = db.Column(db.Boolean)
    policy_reason = db.Column(db.Text)
    status = db.Column(db.String(20))
    execution_time = db.Column(db.Float)
    result = db.Column(db.Text)  # JSON string

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'username': self.username,
            'command': self.command,
            'action': self.action,
            'policy_allowed': self.policy_allowed,
            'policy_reason': self.policy_reason,
            'status': self.status,
            'execution_time': self.execution_time,
            'result': json.loads(self.result) if self.result else None
        }

class Report(db.Model):
    """Report model for database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
            'location': self.location,
            'size_bytes': self.file_size,
            'date_generated': self.date_created.isoformat(),
            'file_path': self.file_path
        }

# Create database tables
with app.app_context():
    db.create_all()
    
    # Initialize default users if they don't exist
    if User.query.count() == 0:
        default_users = [
            User(username='admin', password='password123', role='admin', email='admin@airguard.local'),
            User(username='operator', password='password123', role='operator', email='operator@airguard.local'),
            User(username='viewer', password='password123', role='viewer', email='viewer@airguard.local'),
        ]
        for user in default_users:
            db.session.add(user)
        db.session.commit()
        print("✅ Default users created in database")

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Missing authentication token'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    # Query user from database
    user = User.query.filter_by(username=username).first()
    
    if not user or user.password != password:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'User account is inactive'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate JWT token
    payload = {
        'username': username,
        'role': user.role,
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'user': {
            'username': username,
            'role': user.role,
            'id': user.id
        },
        'token': token
    }), 200

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout():
    """User logout endpoint"""
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/auth/refresh', methods=['POST'])
@token_required
def refresh_token():
    """Refresh authentication token"""
    payload = {
        'username': request.user['username'],
        'role': request.user['role'],
        'id': request.user['id'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

# ============================================================================
# Command Execution Endpoints
# ============================================================================

@app.route('/api/process_command', methods=['POST'])
@token_required
def process_command():
    """Process a natural language command"""
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({'message': 'Command required'}), 400
    
    try:
        result = agent.process_command(command)
        
        # Add request ID for traceability
        result['request_id'] = request.headers.get('X-Request-ID', 'unknown')
        result['user'] = request.user['username']
        
        # Record to audit log database
        audit_log = AuditLog(
            user_id=request.user.get('id'),
            username=request.user['username'],
            command=command,
            action=result.get('action', 'unknown'),
            policy_allowed=result.get('success', False),
            policy_reason=result.get('policy_reason', ''),
            status='success' if result.get('success') else 'error',
            execution_time=result.get('execution_time', 0),
            result=json.dumps(result)
        )
        db.session.add(audit_log)
        db.session.commit()
        
        # If a report file was generated (regardless of action type), save it to database
        if result.get('success'):
            try:
                report_data = result.get('data', {})
                # Check if files were created - report generation creates files
                if result.get('files_created') and len(result.get('files_created', [])) > 0:
                    for report_file in result.get('files_created', []):
                        report_filename = report_file.split('/')[-1] if '/' in report_file else report_file.split('\\')[-1] if '\\' in report_file else report_file
                        
                        # Check if report already exists
                        existing_report = Report.query.filter_by(filename=report_filename).first()
                        if not existing_report:
                            # Calculate actual file size if file exists
                            file_size = 0
                            if os.path.exists(report_file):
                                file_size = os.path.getsize(report_file)
                                print(f"✅ File exists at: {report_file}, size: {file_size} bytes")
                            
                            report = Report(
                                name=report_data.get('report_name', report_filename),
                                filename=report_filename,
                                location=report_data.get('location', 'Unknown'),
                                file_size=file_size,
                                user_id=request.user.get('id'),
                                file_path=report_file
                            )
                            db.session.add(report)
                            db.session.commit()
                            print(f"✅ Report saved to database: {report_filename}")
            except Exception as e:
                print(f"⚠️ Warning: Could not save report to database: {str(e)}")
                db.session.rollback()
        
        return jsonify(result), 200 if result.get('success') else 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e),
            'error': True
        }), 500

# ============================================================================
# Status Endpoints
# ============================================================================

@app.route('/api/status', methods=['GET'])
@token_required
def get_status():
    """Get current system status and pollution metrics"""
    try:
        status = agent.get_system_status()
        
        # Mock pollution metrics
        metrics = {
            'PM2.5': 85,
            'PM10': 120,
            'NO2': 45,
            'SO2': 12,
            'CO': 1.2,
            'O3': 55,
            'AQI': 95
        }
        
        return jsonify({
            'metrics': metrics,
            'timestamp': datetime.now().isoformat(),
            'status': 'online'
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/system_status', methods=['GET'])
@token_required
def get_system_status():
    """Get comprehensive system statistics"""
    try:
        status = agent.get_system_status()
        
        return jsonify({
            'total_actions': status.get('total_actions', 0),
            'successful_actions': status.get('successful_actions', 0),
            'blocked_actions': status.get('blocked_actions', 0),
            'errors': status.get('errors', 0),
            'action_breakdown': {
                'generate_report': 45,
                'analyze_aqi': 30,
                'send_alert': 15,
                'blocked': status.get('blocked_actions', 0)
            },
            'recent_blocked': [
                {
                    'action': 'shutdown_factory',
                    'reason': 'Critical infrastructure control requires human authorization',
                    'timestamp': datetime.now().isoformat()
                }
            ]
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# ============================================================================
# Audit Log Endpoints
# ============================================================================

@app.route('/api/audit_logs', methods=['GET'])
@token_required
def get_audit_logs():
    """Retrieve audit logs with filtering from database"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Query audit logs from database
        query = AuditLog.query
        
        # Filter by date range if provided
        if start_date:
            query = query.filter(AuditLog.timestamp >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AuditLog.timestamp <= datetime.fromisoformat(end_date))
        
        # Sort by timestamp descending (newest first)
        logs = query.order_by(AuditLog.timestamp.desc()).all()
        
        return jsonify({'logs': [log.to_dict() for log in logs]}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/audit_logs', methods=['POST'])
@token_required
def record_audit_log():
    """Record an audit log entry to the database"""
    try:
        data = request.get_json()
        
        # Create new audit log entry
        audit_log = AuditLog(
            user_id=request.user.get('id'),
            username=request.user.get('username'),
            command=data.get('command'),
            action=data.get('action'),
            policy_allowed=data.get('policy_allowed'),
            policy_reason=data.get('policy_reason'),
            status=data.get('status'),
            execution_time=data.get('execution_time'),
            result=json.dumps(data.get('result', {}))
        )
        
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({'id': audit_log.id, 'message': 'Audit log recorded'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ============================================================================
# Report Endpoints
# ============================================================================

@app.route('/api/reports', methods=['GET'])
@token_required
def get_reports():
    """List all generated reports from database"""
    try:
        # Query reports from database
        reports = Report.query.all()
        
        return jsonify({'reports': [report.to_dict() for report in reports]}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/reports', methods=['POST'])
@token_required
def create_report():
    """Create a new report entry in database"""
    try:
        data = request.get_json()
        
        # Create new report entry
        report = Report(
            name=data.get('name'),
            filename=data.get('filename'),
            location=data.get('location'),
            file_size=data.get('file_size', 0),
            user_id=request.user.get('id'),
            file_path=data.get('file_path', f"output/{data.get('filename')}")
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'id': report.id,
            'message': 'Report recorded in database'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@app.route('/api/reports/<report_identifier>', methods=['GET'])
@token_required
def download_report(report_identifier):
    """Download a specific report by ID or filename"""
    try:
        from flask import send_file
        
        # Try to get report by ID first
        report = None
        try:
            report_id = int(report_identifier)
            report = Report.query.get(report_id)
        except (ValueError, TypeError):
            # If not an ID, try filename
            report = Report.query.filter_by(filename=report_identifier).first()
        
        if not report:
            return jsonify({'message': 'Report not found'}), 404
        
        if not os.path.exists(report.file_path):
            return jsonify({'message': 'Report file not found on disk'}), 404
        
        return send_file(report.file_path, as_attachment=True, download_name=report.filename)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/reports/<report_identifier>', methods=['DELETE'])
@token_required
def delete_report(report_identifier):
    """Delete a specific report by ID or filename"""
    try:
        # Try to get report by ID first
        report = None
        try:
            report_id = int(report_identifier)
            report = Report.query.get(report_id)
        except (ValueError, TypeError):
            # If not an ID, try filename
            report = Report.query.filter_by(filename=report_identifier).first()
        
        if not report:
            return jsonify({'message': 'Report not found'}), 404
        
        # Delete file if it exists
        if report.file_path and os.path.exists(report.file_path):
            os.remove(report.file_path)
            print(f"✅ Report file deleted: {report.file_path}")
        
        # Delete database entry
        db.session.delete(report)
        db.session.commit()
        
        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
        
        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ============================================================================
# User Management Endpoints (Admin Only)
# ============================================================================

@app.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    """Get all users from database"""
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200

@app.route('/api/users', methods=['POST'])
@token_required
@admin_required
def create_user():
    """Create a new user in database"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'operator')
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    # Create new user
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'role': new_user.role
    }), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    """Delete a user from database"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Don't allow deleting admin user if it's the last one
    if user.role == 'admin' and User.query.filter_by(role='admin').count() <= 1:
        return jsonify({'message': 'Cannot delete last admin user'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# ============================================================================
# Settings Endpoints
# ============================================================================

@app.route('/api/settings', methods=['GET'])
@token_required
@admin_required
def get_settings():
    """Get system settings"""
    return jsonify({
        'api_url': 'http://localhost:5000/api',
        'notifications': {
            'email_alerts': True,
            'blocked_actions': True
        }
    }), 200

@app.route('/api/settings', methods=['PUT'])
@token_required
@admin_required
def update_settings():
    """Update system settings"""
    data = request.get_json()
    # In production, save to database
    return jsonify({'message': 'Settings updated successfully'}), 200

# ============================================================================
# Health Check
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
