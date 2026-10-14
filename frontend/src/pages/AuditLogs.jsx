import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout/Layout';
import { api } from '../services/api';
import { Download, Search, AlertCircle, CheckCircle } from 'lucide-react';

export default function AuditLogs() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStatus, setFilterStatus] = useState('all');
    const [filterAction, setFilterAction] = useState('all');
    const [currentPage, setCurrentPage] = useState(1);
    const [dateRange, setDateRange] = useState({ start: '', end: '' });

    const itemsPerPage = 50;

    useEffect(() => {
        fetchLogs();
    }, []);

    const fetchLogs = async () => {
        try {
            setLoading(true);
            const response = await api.getAuditLogs({
                start_date: dateRange.start,
                end_date: dateRange.end,
            });
            setLogs(response.data.logs || []);
            setError('');
        } catch (err) {
            setError('Failed to fetch audit logs');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const filteredLogs = logs.filter(log => {
        const matchesSearch = !searchTerm ||
            log.intent?.user_command?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            log.intent?.action?.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesStatus = filterStatus === 'all' || log.status === filterStatus;
        const matchesAction = filterAction === 'all' || log.intent?.action === filterAction;

        return matchesSearch && matchesStatus && matchesAction;
    });

    const paginatedLogs = filteredLogs.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const totalPages = Math.ceil(filteredLogs.length / itemsPerPage);

    const handleExport = () => {
        const csv = generateCSV(filteredLogs);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `audit_logs_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
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
                    <h1 className="text-3xl font-bold text-gray-900">Audit Logs</h1>
                    <p className="text-gray-600 mt-2">Complete history of executed commands and policy decisions</p>
                </div>

                {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                        <AlertCircle size={20} className="text-red-600" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

                {/* Filters */}
                <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        {/* Search */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                            <div className="relative">
                                <Search size={18} className="absolute left-3 top-3 text-gray-400" />
                                <input
                                    type="text"
                                    value={searchTerm}
                                    onChange={(e) => {
                                        setSearchTerm(e.target.value);
                                        setCurrentPage(1);
                                    }}
                                    placeholder="Search commands..."
                                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                                />
                            </div>
                        </div>

                        {/* Status Filter */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                            <select
                                value={filterStatus}
                                onChange={(e) => {
                                    setFilterStatus(e.target.value);
                                    setCurrentPage(1);
                                }}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                            >
                                <option value="all">All Statuses</option>
                                <option value="SUCCESS">Success</option>
                                <option value="BLOCKED">Blocked</option>
                                <option value="ERROR">Error</option>
                            </select>
                        </div>

                        {/* Action Filter */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Action</label>
                            <select
                                value={filterAction}
                                onChange={(e) => {
                                    setFilterAction(e.target.value);
                                    setCurrentPage(1);
                                }}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                            >
                                <option value="all">All Actions</option>
                                <option value="generate_report">Generate Report</option>
                                <option value="analyze_aqi">Analyze AQI</option>
                                <option value="send_alert">Send Alert</option>
                                <option value="shutdown_factory">Shutdown Factory</option>
                                <option value="issue_fine">Issue Fine</option>
                            </select>
                        </div>

                        {/* Export Button */}
                        <div className="flex items-end">
                            <button
                                onClick={handleExport}
                                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                            >
                                <Download size={18} />
                                Export CSV
                            </button>
                        </div>
                    </div>
                </div>

                {/* Logs Table */}
                <div className="bg-white rounded-lg shadow-md overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Timestamp</th>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Command</th>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Action</th>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Policy Decision</th>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Time (s)</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {paginatedLogs.length > 0 ? (
                                    paginatedLogs.map((log, idx) => (
                                        <tr key={idx} className="hover:bg-gray-50 transition">
                                            <td className="px-6 py-4 text-sm text-gray-600 whitespace-nowrap">
                                                {new Date(log.timestamp).toLocaleString()}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                                                {log.intent?.user_command}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-900">
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                                                    {log.intent?.action}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm">
                                                {log.policy_decision?.allowed ? (
                                                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                                                        ✓ Allowed
                                                    </span>
                                                ) : (
                                                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-medium">
                                                        ✗ Blocked
                                                    </span>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 text-sm">
                                                <div className="flex items-center gap-2">
                                                    {log.status === 'SUCCESS' ? (
                                                        <CheckCircle size={16} className="text-green-600" />
                                                    ) : log.status === 'BLOCKED' ? (
                                                        <AlertCircle size={16} className="text-orange-600" />
                                                    ) : (
                                                        <AlertCircle size={16} className="text-red-600" />
                                                    )}
                                                    <span>{log.status}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-900">
                                                {log.execution_time?.toFixed(2) || 'N/A'}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                                            No logs found
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination */}
                    {totalPages > 1 && (
                        <div className="flex items-center justify-between px-6 py-4 bg-gray-50 border-t border-gray-200">
                            <div className="text-sm text-gray-600">
                                Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, filteredLogs.length)} of {filteredLogs.length} logs
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                    disabled={currentPage === 1}
                                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Previous
                                </button>
                                <button
                                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                                    disabled={currentPage === totalPages}
                                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Next
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}

function generateCSV(logs) {
    const headers = ['Timestamp', 'Command', 'Action', 'Decision', 'Reason', 'Status', 'Execution Time'];
    const rows = logs.map(log => [
        log.timestamp,
        log.intent?.user_command || '',
        log.intent?.action || '',
        log.policy_decision?.allowed ? 'Allowed' : 'Blocked',
        log.policy_decision?.reason || '',
        log.status,
        log.execution_time || '',
    ]);

    const csv = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n');

    return csv;
}
