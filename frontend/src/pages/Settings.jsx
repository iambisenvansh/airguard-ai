import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout/Layout';
import { api } from '../services/api';
import { AlertCircle, CheckCircle, Users, Bell, Settings as SettingsIcon } from 'lucide-react';

export default function Settings() {
    const [activeTab, setActiveTab] = useState('users');
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [newUser, setNewUser] = useState({ username: '', password: '', role: 'operator' });
    const [apiUrl, setApiUrl] = useState(localStorage.getItem('apiUrl') || 'http://localhost:5000/api');
    const [notifications, setNotifications] = useState({
        emailAlerts: localStorage.getItem('emailAlerts') === 'true',
        blockedActions: localStorage.getItem('blockedActionsNotif') === 'true',
    });

    useEffect(() => {
        if (activeTab === 'users') {
            fetchUsers();
        }
    }, [activeTab]);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            const response = await api.getUsers();
            setUsers(response.data.users || []);
        } catch (err) {
            setError('Failed to fetch users');
        } finally {
            setLoading(false);
        }
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            await api.createUser(newUser);
            setSuccess('User created successfully');
            setNewUser({ username: '', password: '', role: 'operator' });
            fetchUsers();
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to create user');
        }
    };

    const handleDeleteUser = async (userId) => {
        if (!window.confirm('Are you sure you want to delete this user?')) return;

        try {
            await api.deleteUser(userId);
            setSuccess('User deleted successfully');
            fetchUsers();
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError('Failed to delete user');
        }
    };

    const handleSaveApiUrl = () => {
        localStorage.setItem('apiUrl', apiUrl);
        setSuccess('API URL saved successfully');
        setTimeout(() => setSuccess(''), 3000);
    };

    const handleSaveNotifications = () => {
        localStorage.setItem('emailAlerts', notifications.emailAlerts);
        localStorage.setItem('blockedActionsNotif', notifications.blockedActions);
        setSuccess('Notification settings saved');
        setTimeout(() => setSuccess(''), 3000);
    };

    return (
        <Layout>
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
                    <p className="text-gray-600 mt-2">Manage system configuration and preferences</p>
                </div>

                {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                        <AlertCircle size={20} className="text-red-600" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

                {success && (
                    <div className="p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
                        <CheckCircle size={20} className="text-green-600" />
                        <span className="text-green-700">{success}</span>
                    </div>
                )}

                {/* Tabs */}
                <div className="flex border-b border-gray-200">
                    <button
                        onClick={() => setActiveTab('users')}
                        className={`px-6 py-3 font-medium border-b-2 transition ${activeTab === 'users'
                                ? 'border-green-600 text-green-600'
                                : 'border-transparent text-gray-600 hover:text-gray-900'
                            }`}
                    >
                        <Users size={18} className="inline mr-2" />
                        User Management
                    </button>
                    <button
                        onClick={() => setActiveTab('notifications')}
                        className={`px-6 py-3 font-medium border-b-2 transition ${activeTab === 'notifications'
                                ? 'border-green-600 text-green-600'
                                : 'border-transparent text-gray-600 hover:text-gray-900'
                            }`}
                    >
                        <Bell size={18} className="inline mr-2" />
                        Notifications
                    </button>
                    <button
                        onClick={() => setActiveTab('backend')}
                        className={`px-6 py-3 font-medium border-b-2 transition ${activeTab === 'backend'
                                ? 'border-green-600 text-green-600'
                                : 'border-transparent text-gray-600 hover:text-gray-900'
                            }`}
                    >
                        <SettingsIcon size={18} className="inline mr-2" />
                        Backend Configuration
                    </button>
                </div>

                {/* User Management Tab */}
                {activeTab === 'users' && (
                    <div className="space-y-6">
                        {/* Create New User */}
                        <div className="bg-white rounded-lg shadow-md p-6">
                            <h2 className="text-lg font-bold text-gray-900 mb-4">Create New User</h2>
                            <form onSubmit={handleCreateUser} className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <input
                                        type="text"
                                        placeholder="Username"
                                        value={newUser.username}
                                        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                                        required
                                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                                    />
                                    <input
                                        type="password"
                                        placeholder="Password"
                                        value={newUser.password}
                                        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                        required
                                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                                    />
                                    <select
                                        value={newUser.role}
                                        onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                                    >
                                        <option value="admin">Admin</option>
                                        <option value="operator">Operator</option>
                                        <option value="viewer">Viewer</option>
                                    </select>
                                </div>
                                <button
                                    type="submit"
                                    className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium"
                                >
                                    Create User
                                </button>
                            </form>
                        </div>

                        {/* Users List */}
                        <div className="bg-white rounded-lg shadow-md overflow-hidden">
                            <div className="px-6 py-4 border-b border-gray-200">
                                <h2 className="text-lg font-bold text-gray-900">All Users</h2>
                            </div>
                            <div className="divide-y divide-gray-200">
                                {loading ? (
                                    <div className="p-6 text-center">
                                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
                                    </div>
                                ) : users.length > 0 ? (
                                    users.map(user => (
                                        <div key={user.id} className="px-6 py-4 flex items-center justify-between">
                                            <div>
                                                <p className="font-medium text-gray-900">{user.username}</p>
                                                <p className="text-sm text-gray-600">
                                                    Role: <span className="capitalize font-medium">{user.role}</span>
                                                </p>
                                                <p className="text-sm text-gray-600">
                                                    Last Login: {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}
                                                </p>
                                            </div>
                                            <button
                                                onClick={() => handleDeleteUser(user.id)}
                                                className="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition"
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    ))
                                ) : (
                                    <div className="p-6 text-center text-gray-500">
                                        No users found
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* Notifications Tab */}
                {activeTab === 'notifications' && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-6">Notification Settings</h2>
                        <div className="space-y-4">
                            <label className="flex items-center gap-3 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={notifications.emailAlerts}
                                    onChange={(e) => setNotifications({ ...notifications, emailAlerts: e.target.checked })}
                                    className="w-4 h-4 rounded border-gray-300"
                                />
                                <div>
                                    <p className="font-medium text-gray-900">Email Alerts</p>
                                    <p className="text-sm text-gray-600">Receive email notifications for important events</p>
                                </div>
                            </label>
                            <label className="flex items-center gap-3 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={notifications.blockedActions}
                                    onChange={(e) => setNotifications({ ...notifications, blockedActions: e.target.checked })}
                                    className="w-4 h-4 rounded border-gray-300"
                                />
                                <div>
                                    <p className="font-medium text-gray-900">Blocked Actions Notifications</p>
                                    <p className="text-sm text-gray-600">Get notified when dangerous actions are blocked</p>
                                </div>
                            </label>
                        </div>
                        <button
                            onClick={handleSaveNotifications}
                            className="mt-6 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium"
                        >
                            Save Settings
                        </button>
                    </div>
                )}

                {/* Backend Configuration Tab */}
                {activeTab === 'backend' && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-6">Backend Configuration</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Backend API URL
                                </label>
                                <input
                                    type="text"
                                    value={apiUrl}
                                    onChange={(e) => setApiUrl(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                                    placeholder="http://localhost:5000/api"
                                />
                                <p className="text-sm text-gray-600 mt-2">
                                    The URL where your AirGuard AI backend API is running
                                </p>
                            </div>
                            <button
                                onClick={handleSaveApiUrl}
                                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium"
                            >
                                Save Configuration
                            </button>
                        </div>

                        <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                            <p className="font-medium text-blue-900 mb-2">Backend Status</p>
                            <p className="text-sm text-blue-700">
                                Currently connected to: <span className="font-mono">{apiUrl}</span>
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}
