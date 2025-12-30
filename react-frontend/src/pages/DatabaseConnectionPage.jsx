import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const DatabaseConnectionPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        dbType: 'mysql',
        host: 'localhost',
        port: 3306,
        database: '',
        username: '',
        password: ''
    });
    const [testing, setTesting] = useState(false);
    const [saving, setSaving] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value,
            // Auto-update port when database type changes
            ...(name === 'dbType' && {
                port: value === 'mysql' ? 3306 : 5432
            })
        }));
    };

    const handleTestConnection = async () => {
        setTesting(true);
        try {
            const response = await fetch('http://localhost:5000/api/sql/test-connection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dbType: formData.dbType,
                    host: formData.host,
                    port: parseInt(formData.port),
                    database: formData.database,
                    username: formData.username,
                    password: formData.password
                })
            });

            const data = await response.json();

            if (data.success) {
                toast.success('Connection successful!');
            } else {
                toast.error(data.message || 'Connection failed');
            }
        } catch (error) {
            toast.error('Error testing connection: ' + error.message);
        } finally {
            setTesting(false);
        }
    };

    const handleSaveConnection = async () => {
        if (!formData.name || !formData.database || !formData.username) {
            toast.error('Please fill in all required fields (name, database, username)');
            return;
        }

        setSaving(true);
        try {
            const userId = localStorage.getItem('userId') || 'default_user';
            const connectionId = `conn_${Date.now()}`;

            const response = await fetch('http://localhost:5000/api/sql/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId,
                    connectionId,
                    name: formData.name,
                    dbType: formData.dbType,
                    host: formData.host,
                    port: parseInt(formData.port),
                    database: formData.database,
                    username: formData.username,
                    password: formData.password || ''
                })
            });

            const data = await response.json();

            if (data.success) {
                toast.success('Database connection saved!');
                navigate('/unified-chat');
            } else {
                toast.error(data.message || 'Failed to save connection');
            }
        } catch (error) {
            toast.error('Error saving connection: ' + error.message);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-2xl mx-auto px-4">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h1 className="text-2xl font-bold text-gray-900 mb-6">
                        Connect Database
                    </h1>

                    <div className="space-y-4">
                        {/* Connection Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Connection Name *
                            </label>
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="e.g., Production Database"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        {/* Database Type */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Database Type *
                            </label>
                            <select
                                name="dbType"
                                value={formData.dbType}
                                onChange={handleChange}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="mysql">MySQL</option>
                                <option value="postgresql">PostgreSQL</option>
                            </select>
                        </div>

                        {/* Host and Port */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Host *
                                </label>
                                <input
                                    type="text"
                                    name="host"
                                    value={formData.host}
                                    onChange={handleChange}
                                    placeholder="localhost"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Port *
                                </label>
                                <input
                                    type="number"
                                    name="port"
                                    value={formData.port}
                                    onChange={handleChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                        </div>

                        {/* Database Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Database Name *
                            </label>
                            <input
                                type="text"
                                name="database"
                                value={formData.database}
                                onChange={handleChange}
                                placeholder="my_database"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        {/* Username */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Username *
                            </label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="database_user"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        {/* Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Password <span className="text-gray-400">(optional)</span>
                            </label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Leave empty if no password"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                            <p className="text-xs text-gray-500 mt-1">
                                For local MySQL (XAMPP/WAMP), root often has no password
                            </p>
                        </div>

                        {/* Buttons */}
                        <div className="flex gap-3 pt-4">
                            <button
                                onClick={handleTestConnection}
                                disabled={testing}
                                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {testing ? 'Testing...' : 'Test Connection'}
                            </button>
                            <button
                                onClick={handleSaveConnection}
                                disabled={saving}
                                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {saving ? 'Saving...' : 'Save & Continue'}
                            </button>
                        </div>

                        <button
                            onClick={() => navigate('/dashboard')}
                            className="w-full px-4 py-2 text-gray-600 hover:text-gray-800"
                        >
                            Cancel
                        </button>
                    </div>
                </div>

                {/* Info Box */}
                <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="font-semibold text-blue-900 mb-2">Security Tip</h3>
                    <p className="text-sm text-blue-800">
                        For security, we recommend creating a read-only database user for this connection.
                        This prevents accidental data modifications.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default DatabaseConnectionPage;
