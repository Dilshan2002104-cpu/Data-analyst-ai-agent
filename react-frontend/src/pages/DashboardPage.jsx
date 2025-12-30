import { useEffect } from 'react';
import { useData } from '../contexts/DataContext';
import Navbar from '../components/Navbar';
import FileUpload from '../components/FileUpload';
import DatasetCard from '../components/DatasetCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { Upload } from 'lucide-react';

const DashboardPage = () => {
    const { datasets, loading, fetchDatasets, deleteDataset } = useData();

    useEffect(() => {
        fetchDatasets();

        // Poll for updates every 5 seconds (to check for processing completion)
        const intervalId = setInterval(() => {
            fetchDatasets();
        }, 5000);

        return () => clearInterval(intervalId);
    }, [fetchDatasets]);

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">My Datasets</h1>
                    <p className="text-gray-600">
                        Upload and manage your data files for AI-powered analysis
                    </p>
                </div>

                {/* Upload Section */}
                <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
                    <div className="flex items-center gap-2 mb-4">
                        <Upload className="w-5 h-5 text-blue-600" />
                        <h2 className="text-lg font-semibold text-gray-900">
                            Upload New Dataset
                        </h2>
                    </div>
                    <FileUpload onUploadComplete={fetchDatasets} />
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                    <button
                        onClick={() => window.location.href = '/connect-database'}
                        className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg p-6 hover:from-green-600 hover:to-green-700 transition-all shadow-md"
                    >
                        <h3 className="text-lg font-semibold mb-2">🗄️ Connect Database</h3>
                        <p className="text-sm text-green-50">Connect to MySQL or PostgreSQL</p>
                    </button>
                    <button
                        onClick={() => window.location.href = '/unified-chat'}
                        className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg p-6 hover:from-purple-600 hover:to-purple-700 transition-all shadow-md"
                    >
                        <h3 className="text-lg font-semibold mb-2">💬 Unified Chat</h3>
                        <p className="text-sm text-purple-50">Query all your data sources</p>
                    </button>
                </div>

                {/* Datasets Grid */}
                {loading && datasets.length === 0 ? (
                    <div className="flex justify-center py-12">
                        <LoadingSpinner text="Loading datasets..." />
                    </div>
                ) : datasets.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-gray-500 text-lg">No datasets yet</p>
                        <p className="text-gray-400 text-sm mt-2">
                            Upload your first CSV or Excel file to get started
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {datasets.map((dataset) => (
                            <DatasetCard
                                key={dataset.id}
                                dataset={dataset}
                                onDelete={deleteDataset}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DashboardPage;
