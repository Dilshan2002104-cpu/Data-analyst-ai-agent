import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, Database, Home, MessageSquare, Database as DatabaseIcon } from 'lucide-react';

const Navbar = () => {
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    const isActive = (path) => location.pathname === path;

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3 group">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-200 group-hover:scale-105">
                            <Database className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                            Data Analyst AI
                        </span>
                    </Link>

                    {/* Navigation Links */}
                    <div className="flex items-center gap-2">
                        <Link
                            to="/"
                            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${isActive('/') || isActive('/dashboard')
                                    ? 'bg-blue-50 text-blue-700'
                                    : 'text-gray-700 hover:bg-gray-100'
                                }`}
                        >
                            <Home className="w-4 h-4" />
                            <span className="hidden sm:inline">Dashboard</span>
                        </Link>
                        <Link
                            to="/unified-chat"
                            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${isActive('/unified-chat')
                                    ? 'bg-blue-50 text-blue-700'
                                    : 'text-gray-700 hover:bg-gray-100'
                                }`}
                        >
                            <MessageSquare className="w-4 h-4" />
                            <span className="hidden sm:inline">Chat</span>
                        </Link>
                        <Link
                            to="/connect-database"
                            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${isActive('/connect-database')
                                    ? 'bg-blue-50 text-blue-700'
                                    : 'text-gray-700 hover:bg-gray-100'
                                }`}
                        >
                            <DatabaseIcon className="w-4 h-4" />
                            <span className="hidden sm:inline">Connect DB</span>
                        </Link>
                    </div>

                    {/* User Info & Logout */}
                    {currentUser && (
                        <div className="flex items-center gap-4">
                            <div className="text-sm hidden md:block">
                                <p className="font-semibold text-gray-900">
                                    {currentUser.displayName || currentUser.email}
                                </p>
                                <p className="text-gray-500 text-xs">{currentUser.email}</p>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
                            >
                                <LogOut className="w-4 h-4" />
                                <span className="hidden sm:inline">Logout</span>
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
