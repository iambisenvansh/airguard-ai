import React, { useState } from 'react';
import Layout from '../components/Layout/Layout';
import { useCommandStore } from '../store/commandStore';
import { api } from '../services/api';
import { Send, Star, Loader, AlertCircle, CheckCircle, Clock } from 'lucide-react';

const COMMAND_SUGGESTIONS = [
    'Generate pollution report for Delhi',
    'Analyze AQI in Delhi',
    'Send critical alert about high pollution levels in Delhi',
    'Generate pollution report for Mumbai',
    'Analyze AQI in Mumbai',
];

export default function Commands() {
    const { commands, favorites, addCommand, toggleFavorite, currentCommand, setCurrentCommand, lastResult, setLastResult, setIsExecuting, isExecuting } = useCommandStore();
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [filteredSuggestions, setFilteredSuggestions] = useState(COMMAND_SUGGESTIONS);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setCurrentCommand(value);

        if (value) {
            const filtered = [
                ...favorites.filter(f => f.toLowerCase().includes(value.toLowerCase())),
                ...COMMAND_SUGGESTIONS.filter(
                    s => s.toLowerCase().includes(value.toLowerCase()) && !favorites.includes(s)
                ),
                ...commands.filter(
                    c => c.toLowerCase().includes(value.toLowerCase()) && !favorites.includes(c) && !COMMAND_SUGGESTIONS.includes(c)
                ),
            ];
            setFilteredSuggestions(filtered.slice(0, 8));
            setShowSuggestions(true);
        } else {
            setFilteredSuggestions([...favorites, ...COMMAND_SUGGESTIONS].slice(0, 8));
            setShowSuggestions(true);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!currentCommand.trim()) return;

        setIsExecuting(true);
        try {
            const response = await api.processCommand(currentCommand);
            const result = response.data;

            setLastResult(result);
            addCommand(currentCommand);
            setCurrentCommand('');
            setShowSuggestions(false);
        } catch (err) {
            setLastResult({
                success: false,
                message: err.response?.data?.message || 'Failed to execute command',
                error: true,
            });
        } finally {
            setIsExecuting(false);
        }
    };

    const handleSuggestionClick = (suggestion) => {
        setCurrentCommand(suggestion);
        setShowSuggestions(false);
    };

    return (
        <Layout>
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Command Execution</h1>
                    <p className="text-gray-600 mt-2">Enter natural language commands to control the AI agent</p>
                </div>

                {/* Command Input */}
                <div className="bg-white rounded-lg shadow-md p-6">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="relative">
                            <input
                                type="text"
                                value={currentCommand}
                                onChange={handleInputChange}
                                onFocus={() => setShowSuggestions(true)}
                                placeholder="e.g., Generate pollution report for Delhi"
                                disabled={isExecuting}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent disabled:bg-gray-100"
                            />

                            {/* Suggestions Dropdown */}
                            {showSuggestions && filteredSuggestions.length > 0 && (
                                <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-10">
                                    {filteredSuggestions.map((suggestion, idx) => (
                                        <button
                                            key={idx}
                                            type="button"
                                            onClick={() => handleSuggestionClick(suggestion)}
                                            className="w-full text-left px-4 py-2 hover:bg-gray-100 border-b last:border-b-0 flex items-center justify-between group"
                                        >
                                            <span className="text-sm text-gray-700">{suggestion}</span>
                                            {favorites.includes(suggestion) && (
                                                <Star size={16} className="text-yellow-500 fill-yellow-500" />
                                            )}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>

                        <button
                            type="submit"
                            disabled={isExecuting || !currentCommand.trim()}
                            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2"
                        >
                            {isExecuting ? (
                                <>
                                    <Loader size={18} className="animate-spin" />
                                    Executing...
                                </>
                            ) : (
                                <>
                                    <Send size={18} />
                                    Execute Command
                                </>
                            )}
                        </button>
                    </form>

                    {/* Command Tips */}
                    <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                        <h3 className="font-medium text-blue-900 mb-2">Try these commands:</h3>
                        <ul className="text-sm text-blue-700 space-y-1">
                            <li>• Generate pollution report for [location]</li>
                            <li>• Analyze AQI in [location]</li>
                            <li>• Send critical alert about high pollution levels</li>
                        </ul>
                    </div>
                </div>

                {/* Result Display */}
                {lastResult && (
                    <CommandResult result={lastResult} onAddToFavorite={() => toggleFavorite(currentCommand)} />
                )}

                {/* Command History */}
                {commands.length > 0 && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-4">Recent Commands</h2>
                        <div className="space-y-2">
                            {commands.slice(0, 10).map((cmd, idx) => (
                                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                                    <button
                                        onClick={() => handleSuggestionClick(cmd)}
                                        className="flex-1 text-left text-sm text-gray-700 hover:text-green-600"
                                    >
                                        {cmd}
                                    </button>
                                    <button
                                        onClick={() => toggleFavorite(cmd)}
                                        className="p-1 hover:bg-gray-200 rounded transition"
                                    >
                                        <Star
                                            size={18}
                                            className={favorites.includes(cmd) ? 'text-yellow-500 fill-yellow-500' : 'text-gray-400'}
                                        />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}

function CommandResult({ result, onAddToFavorite }) {
    const getStatusIcon = () => {
        if (result.error) return <AlertCircle className="text-red-600" size={20} />;
        if (result.policy_decision?.allowed === false) return <AlertCircle className="text-orange-600" size={20} />;
        return <CheckCircle className="text-green-600" size={20} />;
    };

    const getStatusColor = () => {
        if (result.error) return 'red';
        if (result.policy_decision?.allowed === false) return 'orange';
        return result.success ? 'green' : 'red';
    };

    const color = getStatusColor();
    const bgClass = `bg-${color}-50 border-${color}-200`;
    const textClass = `text-${color}-700`;

    return (
        <div className={`bg-white rounded-lg shadow-md p-6 border-l-4 border-${color}-600`}>
            <div className="flex items-start gap-4 mb-4">
                {getStatusIcon()}
                <div className="flex-1">
                    <h2 className="text-lg font-bold text-gray-900">Command Response</h2>
                    <p className={`text-sm ${textClass} mt-1`}>{result.message}</p>
                </div>
            </div>

            {/* Parsed Intent */}
            {result.intent && (
                <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">Parsed Intent</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <p className="text-gray-600">Action</p>
                            <p className="font-medium text-gray-900">{result.intent.action}</p>
                        </div>
                        <div>
                            <p className="text-gray-600">Confidence</p>
                            <p className="font-medium text-gray-900">{(result.intent.confidence * 100).toFixed(1)}%</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Policy Decision */}
            {result.policy_decision && (
                <div className={`mb-4 p-4 ${bgClass} border border-${color}-200 rounded-lg`}>
                    <h3 className="font-semibold text-gray-900 mb-2">Policy Decision</h3>
                    <div className="space-y-2 text-sm">
                        <p>
                            <span className="text-gray-600">Status:</span>
                            <span className={`ml-2 font-medium ${result.policy_decision.allowed ? 'text-green-600' : 'text-red-600'}`}>
                                {result.policy_decision.allowed ? '✓ Allowed' : '✗ Blocked'}
                            </span>
                        </p>
                        <p>
                            <span className="text-gray-600">Reason:</span>
                            <span className="ml-2 font-medium text-gray-900">{result.policy_decision.reason}</span>
                        </p>
                    </div>
                </div>
            )}

            {/* Execution Result */}
            {result.success && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">Execution Result</h3>
                    <div className="space-y-2 text-sm">
                        <p>
                            <span className="text-gray-600">Execution Time:</span>
                            <span className="ml-2 font-medium text-gray-900">{result.execution_time?.toFixed(2) || 'N/A'}s</span>
                        </p>
                        {result.files_created && result.files_created.length > 0 && (
                            <div>
                                <p className="text-gray-600 mb-1">Files Created:</p>
                                <ul className="list-disc list-inside space-y-1">
                                    {result.files_created.map((file, idx) => (
                                        <li key={idx} className="text-gray-700 break-all">{file}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Action Buttons */}
            <div className="mt-4 flex gap-2">
                <button
                    onClick={onAddToFavorite}
                    className="flex items-center gap-2 px-4 py-2 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 transition"
                >
                    <Star size={18} />
                    Add to Favorites
                </button>
                <button
                    onClick={() => navigator.clipboard.writeText(JSON.stringify(result, null, 2))}
                    className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
                >
                    <Clock size={18} />
                    Copy Response
                </button>
            </div>
        </div>
    );
}
