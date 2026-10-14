import React, { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { useThemeStore } from '../../store/themeStore';
import { Menu, X, LogOut, Moon, Sun } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export default function Header() {
    const { user, logout } = useAuthStore();
    const { isDarkMode, toggleDarkMode } = useThemeStore();
    const navigate = useNavigate();
    const [menuOpen, setMenuOpen] = useState(false);
    const [language, setLanguage] = useState('en');

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <header className="sticky top-0 z-40 backdrop-blur-xl border-b border-gray-200 dark:border-green-900/20 bg-white dark:bg-gradient-to-r dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 shadow-lg dark:shadow-2xl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/dashboard" className="flex items-center gap-3 group">
                        <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center group-hover:shadow-lg group-hover:shadow-green-500/50 transition-all duration-300">
                            <span className="text-white font-bold text-sm">AG</span>
                        </div>
                        <span className="hidden sm:inline font-bold text-gray-900 dark:text-white dark:bg-gradient-to-r dark:from-green-400 dark:to-green-300 dark:bg-clip-text dark:text-transparent group-hover:opacity-80 transition">AirGuard AI</span>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-8">
                        <Link to="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200 relative group">
                            Dashboard
                            <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-green-600 group-hover:w-full transition-all duration-300"></span>
                        </Link>
                        {user?.role !== 'viewer' && (
                            <>
                                <Link to="/commands" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200 relative group">
                                    Commands
                                    <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-green-600 group-hover:w-full transition-all duration-300"></span>
                                </Link>
                                <Link to="/reports" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200 relative group">
                                    Reports
                                    <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-green-600 group-hover:w-full transition-all duration-300"></span>
                                </Link>
                                <Link to="/audit-logs" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200 relative group">
                                    Audit Logs
                                    <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-green-600 group-hover:w-full transition-all duration-300"></span>
                                </Link>
                            </>
                        )}
                        {user?.role === 'admin' && (
                            <Link to="/settings" className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors duration-200 relative group">
                                Settings
                                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-green-600 group-hover:w-full transition-all duration-300"></span>
                            </Link>
                        )}
                    </nav>

                    {/* Right Side - Controls */}
                    <div className="flex items-center gap-4">
                        {/* Language Selector */}
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            className="text-sm border border-gray-300 dark:border-green-900/40 bg-white dark:bg-slate-800/50 text-gray-900 dark:text-gray-200 rounded px-3 py-1.5 focus:ring-2 focus:ring-green-600 focus:border-transparent transition-all duration-200 backdrop-blur"
                        >
                            <option value="en">English</option>
                            <option value="hi">हिंदी</option>
                        </select>

                        {/* Dark Mode Toggle */}
                        <button
                            onClick={toggleDarkMode}
                            className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800/50 dark:text-gray-300 rounded-lg transition-all duration-200 group"
                            title="Toggle dark mode"
                        >
                            {isDarkMode ? (
                                <Sun size={20} className="text-yellow-400 group-hover:text-yellow-300 transition" />
                            ) : (
                                <Moon size={20} className="text-gray-700 group-hover:text-gray-900" />
                            )}
                        </button>

                        {/* User Info and Logout */}
                        <div className="hidden sm:flex items-center gap-4 pl-4 border-l border-gray-200 dark:border-green-900/20">
                            <span className="text-sm text-gray-700 dark:text-gray-300 font-medium">{user?.username}</span>
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-2 px-3 py-1.5 text-gray-700 dark:text-gray-300 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 rounded-lg transition-all duration-200"
                            >
                                <LogOut size={18} />
                                <span className="hidden sm:inline text-sm">Logout</span>
                            </button>
                        </div>

                        {/* Mobile Menu Toggle */}
                        <button
                            onClick={() => setMenuOpen(!menuOpen)}
                            className="md:hidden p-2 hover:bg-gray-100 dark:hover:bg-slate-800/50 rounded-lg transition-all duration-200"
                        >
                            {menuOpen ? <X size={24} className="text-gray-900 dark:text-white" /> : <Menu size={24} className="text-gray-900 dark:text-white" />}
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation */}
                {menuOpen && (
                    <nav className="md:hidden pb-4 border-t border-gray-200 dark:border-green-900/20 bg-gradient-to-b from-transparent to-slate-900/50 dark:to-slate-950/50">
                        <Link to="/dashboard" className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                            Dashboard
                        </Link>
                        {user?.role !== 'viewer' && (
                            <>
                                <Link to="/commands" className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                                    Commands
                                </Link>
                                <Link to="/reports" className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                                    Reports
                                </Link>
                                <Link to="/audit-logs" className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                                    Audit Logs
                                </Link>
                            </>
                        )}
                        {user?.role === 'admin' && (
                            <Link to="/settings" className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-green-50 dark:hover:bg-green-900/20 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                                Settings
                            </Link>
                        )}
                        <button
                            onClick={handleLogout}
                            className="block w-full text-left px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                        >
                            Logout
                        </button>
                    </nav>
                )}
            </div>
        </header>
    );
}
