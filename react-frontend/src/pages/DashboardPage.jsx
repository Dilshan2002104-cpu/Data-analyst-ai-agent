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
