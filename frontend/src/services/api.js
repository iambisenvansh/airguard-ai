import axios from 'axios';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        // Add request ID for traceability
        config.headers['X-Request-ID'] = generateUUID();
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Handle unauthorized - redirect to login
            localStorage.removeItem('authToken');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Generate UUID for request tracking
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// API endpoints
export const api = {
    // Authentication
    login: (credentials) => apiClient.post('/auth/login', credentials),
    logout: () => apiClient.post('/auth/logout'),
    refreshToken: () => apiClient.post('/auth/refresh'),

    // Commands
    processCommand: (command) => apiClient.post('/process_command', { command }),

    // Status
    getStatus: () => apiClient.get('/status'),
    getSystemStatus: () => apiClient.get('/system_status'),

    // Audit Logs
    getAuditLogs: (params) => apiClient.get('/audit_logs', { params }),

    // Reports
    getReports: () => apiClient.get('/reports'),
    downloadReport: (filename) => apiClient.get(`/reports/${filename}`, {
        responseType: 'blob',
    }),
    deleteReport: (filename) => apiClient.delete(`/reports/${filename}`),

    // User Management (Admin only)
    getUsers: () => apiClient.get('/users'),
    createUser: (userData) => apiClient.post('/users', userData),
    updateUser: (userId, userData) => apiClient.put(`/users/${userId}`, userData),
    deleteUser: (userId) => apiClient.delete(`/users/${userId}`),

    // Settings
    getSettings: () => apiClient.get('/settings'),
    updateSettings: (settings) => apiClient.put('/settings', settings),
};

export default apiClient;
