import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout/Layout';
import { api } from '../services/api';
import { AlertCircle, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import {
    LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#6366f1'];

export default function Dashboard() {
    const [status, setStatus] = useState(null);
    const [systemStatus, setSystemStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 30000); // Poll every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [statusRes, sysRes] = await Promise.all([
                api.getStatus(),
                api.getSystemStatus(),
            ]);
            setStatus(statusRes.data);
            setSystemStatus(sysRes.data);
            setError('');
        } catch (err) {
            setError('Failed to fetch data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <Layout>
                <div className="flex justify-center items-center h-96">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Pollution Monitoring Dashboard</h1>
                    <p className="text-gray-600 mt-2">Real-time air quality monitoring across Delhi</p>
                </div>

                {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                        <AlertCircle size={20} className="text-red-600" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <MetricCard
                        title="Total Commands"
                        value={systemStatus?.total_actions || 0}
                        icon={<CheckCircle className="text-blue-600" />}
                        color="blue"
                    />
                    <MetricCard
                        title="Allowed Actions"
                        value={systemStatus?.successful_actions || 0}
                        icon={<TrendingUp className="text-green-600" />}
                        color="green"
                    />
                    <MetricCard
                        title="Blocked Actions"
                        value={systemStatus?.blocked_actions || 0}
                        icon={<AlertTriangle className="text-red-600" />}
                        color="red"
                    />
                    <MetricCard
                        title="Errors"
                        value={systemStatus?.errors || 0}
                        icon={<AlertCircle className="text-orange-600" />}
                        color="orange"
                    />
                </div>

                {/* Pollution Metrics */}
                {status?.metrics && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-bold text-gray-900 mb-4">Current Pollution Metrics</h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
                            {Object.entries(status.metrics).map(([key, value]) => (
                                <div key={key} className="text-center p-4 bg-gray-50 rounded-lg">
                                    <div className="text-sm text-gray-600 uppercase font-semibold">{key}</div>
                                    <div className="text-2xl font-bold text-gray-900 mt-2">{value}</div>
                                    <div className={`text-xs mt-1 ${getSeverityColor(value, key)}`}>
                                        {getSeverityLabel(value, key)}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="text-xs text-gray-500 mt-4">
                            Last updated: {new Date(status.timestamp).toLocaleString()}
                        </div>
                    </div>
                )}

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Action Distribution */}
                    {systemStatus?.action_breakdown && (
                        <div className="bg-white rounded-lg shadow-md p-6">
                            <h2 className="text-lg font-bold text-gray-900 mb-4">Action Distribution</h2>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={Object.entries(systemStatus.action_breakdown).map(([name, value]) => ({ name, value }))}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, value }) => `${name}: ${value}`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {COLORS.map((color, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    )}

                    {/* Command Volume */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-4">Command Trend (Last 24h)</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <LineChart data={generateTimeSeriesData()}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="time" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="commands" stroke="#10b981" name="Total Commands" />
                                <Line type="monotone" dataKey="blocked" stroke="#ef4444" name="Blocked" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Recent Blocked Actions */}
                {systemStatus?.recent_blocked && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-4">Recent Blocked Actions</h2>
                        <div className="space-y-3">
                            {systemStatus.recent_blocked.slice(0, 5).map((item, idx) => (
                                <div key={idx} className="flex items-start gap-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                                    <AlertTriangle size={20} className="text-red-600 mt-0.5 flex-shrink-0" />
                                    <div className="flex-1 min-w-0">
                                        <p className="font-medium text-gray-900">{item.action}</p>
                                        <p className="text-sm text-gray-600">{item.reason}</p>
                                    </div>
                                    <div className="text-xs text-gray-500 flex-shrink-0">
                                        {new Date(item.timestamp).toLocaleTimeString()}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}

function MetricCard({ title, value, icon, color }) {
    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-600 text-sm font-medium">{title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
                </div>
                <div className="p-3 bg-gray-100 rounded-lg">{icon}</div>
            </div>
        </div>
    );
}

function getSeverityColor(value, metric) {
    if (metric === 'AQI') {
        if (value <= 50) return 'text-green-600';
        if (value <= 100) return 'text-yellow-600';
        if (value <= 200) return 'text-orange-600';
        return 'text-red-600';
    }
    return 'text-gray-600';
}

function getSeverityLabel(value, metric) {
    if (metric === 'AQI') {
        if (value <= 50) return 'Good';
        if (value <= 100) return 'Moderate';
        if (value <= 200) return 'Poor';
        return 'Critical';
    }
    return '';
}

function generateTimeSeriesData() {
    const data = [];
    for (let i = 23; i >= 0; i--) {
        const hour = new Date();
        hour.setHours(hour.getHours() - i);
        data.push({
            time: hour.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
            commands: Math.floor(Math.random() * 20) + 5,
            blocked: Math.floor(Math.random() * 5),
        });
    }
    return data;
}
