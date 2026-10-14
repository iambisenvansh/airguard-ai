import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout/Layout';
import { api } from '../services/api';
import { Download, Trash2, Eye, AlertCircle, Calendar } from 'lucide-react';

export default function Reports() {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [filterLocation, setFilterLocation] = useState('all');
    const [filterDateStart, setFilterDateStart] = useState('');
    const [filterDateEnd, setFilterDateEnd] = useState('');
    const [selectedReport, setSelectedReport] = useState(null);

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            setLoading(true);
            const response = await api.getReports();
            setReports(response.data.reports || []);
            setError('');
        } catch (err) {
            setError('Failed to fetch reports');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = async (filename) => {
        try {
            const response = await api.downloadReport(filename);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.parentElement.removeChild(link);
        } catch (err) {
            alert('Failed to download report');
        }
    };

    const handleDelete = async (filename) => {
        if (!window.confirm('Are you sure you want to delete this report?')) return;

        try {
            await api.deleteReport(filename);
            setReports(reports.filter(r => r.filename !== filename));
        } catch (err) {
            alert('Failed to delete report');
        }
    };

    const handleView = (report) => {
        setSelectedReport(report);
    };

    const filteredReports = reports.filter(report => {
        const matchesLocation = filterLocation === 'all' || report.location === filterLocation;
        const reportDate = new Date(report.date_generated);
        const matchesDateStart = !filterDateStart || reportDate >= new Date(filterDateStart);
        const matchesDateEnd = !filterDateEnd || reportDate <= new Date(filterDateEnd);
        return matchesLocation && matchesDateStart && matchesDateEnd;
    });

    const locations = [...new Set(reports.map(r => r.location))];
    const totalStorage = reports.reduce((sum, r) => sum + (r.size_bytes || 0), 0);

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
                    <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
                    <p className="text-gray-600 mt-2">Manage and view generated pollution analysis reports</p>
                </div>

                {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                        <AlertCircle size={20} className="text-red-600" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

                {/* Statistics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <p className="text-gray-600 text-sm font-medium">Total Reports</p>
                        <p className="text-3xl font-bold text-gray-900 mt-2">{reports.length}</p>
                    </div>
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <p className="text-gray-600 text-sm font-medium">Total Storage</p>
                        <p className="text-3xl font-bold text-gray-900 mt-2">
                            {(totalStorage / 1024 / 1024).toFixed(2)} MB
                        </p>
                    </div>
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <p className="text-gray-600 text-sm font-medium">Unique Locations</p>
                        <p className="text-3xl font-bold text-gray-900 mt-2">{locations.length}</p>
                    </div>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                            <select
                                value={filterLocation}
                                onChange={(e) => setFilterLocation(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                            >
                                <option value="all">All Locations</option>
                                {locations.map(loc => (
                                    <option key={loc} value={loc}>{loc}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                            <input
                                type="date"
                                value={filterDateStart}
                                onChange={(e) => setFilterDateStart(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                            <input
                                type="date"
                                value={filterDateEnd}
                                onChange={(e) => setFilterDateEnd(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
                            />
                        </div>
                    </div>
                </div>

                {/* Reports List */}
                {filteredReports.length > 0 ? (
                    <div className="grid grid-cols-1 gap-4">
                        {filteredReports.map((report, idx) => (
                            <div key={idx} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex-1 min-w-0">
                                        <h3 className="text-lg font-semibold text-gray-900 truncate">{report.name}</h3>
                                        <p className="text-sm text-gray-600 mt-1">
                                            <Calendar size={16} className="inline mr-1" />
                                            {new Date(report.date_generated).toLocaleString()}
                                        </p>
                                        <p className="text-sm text-gray-600">Location: {report.location}</p>
                                        <p className="text-sm text-gray-600">
                                            Size: {(report.size_bytes / 1024).toFixed(2)} KB
                                        </p>
                                    </div>

                                    <div className="flex gap-2 flex-shrink-0">
                                        <button
                                            onClick={() => handleView(report)}
                                            className="flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition"
                                        >
                                            <Eye size={18} />
                                            <span className="hidden sm:inline">View</span>
                                        </button>
                                        <button
                                            onClick={() => handleDownload(report.filename)}
                                            className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition"
                                        >
                                            <Download size={18} />
                                            <span className="hidden sm:inline">Download</span>
                                        </button>
                                        <button
                                            onClick={() => handleDelete(report.filename)}
                                            className="flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition"
                                        >
                                            <Trash2 size={18} />
                                            <span className="hidden sm:inline">Delete</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-md p-12 text-center">
                        <AlertCircle size={48} className="mx-auto text-gray-400 mb-4" />
                        <p className="text-gray-600 text-lg">No reports found</p>
                        <p className="text-gray-500 mt-2">Generate reports using natural language commands</p>
                    </div>
                )}

                {/* Report Viewer Modal */}
                {selectedReport && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                        <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-auto">
                            <div className="flex justify-between items-center p-6 border-b border-gray-200 sticky top-0 bg-white">
                                <h2 className="text-xl font-bold text-gray-900">{selectedReport.name}</h2>
                                <button
                                    onClick={() => setSelectedReport(null)}
                                    className="text-gray-400 hover:text-gray-600"
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="p-6 whitespace-pre-wrap text-sm text-gray-700 font-mono bg-gray-50">
                                {selectedReport.content || 'Report content loading...'}
                            </div>
                            <div className="p-6 border-t border-gray-200 flex justify-end gap-2 bg-gray-50">
                                <button
                                    onClick={() => setSelectedReport(null)}
                                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition"
                                >
                                    Close
                                </button>
                                <button
                                    onClick={() => handleDownload(selectedReport.filename)}
                                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                                >
                                    Download
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}
