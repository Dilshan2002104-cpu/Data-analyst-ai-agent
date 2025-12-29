import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, Database } from 'lucide-react';

const Navbar = () => {
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2">
                        <Database className="w-8 h-8 text-blue-600" />
                        <span className="text-xl font-bold text-gray-900">
                            Data Analyst AI
                        </span>
                    </Link>

                    {/* User Info & Logout */}
                    {currentUser && (
                        <div className="flex items-center gap-4">
                            <div className="text-sm">
                                <p className="font-medium text-gray-900">
                                    {currentUser.displayName || currentUser.email}
                                </p>
                                <p className="text-gray-500 text-xs">{currentUser.email}</p>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                            >
                                <LogOut className="w-4 h-4" />
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
