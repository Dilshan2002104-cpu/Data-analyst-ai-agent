import { useNavigate } from 'react-router-dom';
import { MessageSquare, Trash2, FileText, CheckCircle, Clock } from 'lucide-react';

const DatasetCard = ({ dataset, onDelete }) => {
    const navigate = useNavigate();

    const handleChat = () => {
        navigate(`/chat/${dataset.id}`);
    };

    const handleDelete = (e) => {
        e.stopPropagation();
        if (window.confirm(`Delete "${dataset.fileName}"?`)) {
            onDelete(dataset.id);
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    const formatDate = (timestamp) => {
        return new Date(timestamp).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    return (
        <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                    <FileText className="w-10 h-10 text-blue-600" />
                    <div>
                        <h3 className="font-semibold text-gray-900 text-lg">
                            {dataset.fileName}
                        </h3>
                        <p className="text-sm text-gray-500">
                            {formatFileSize(dataset.fileSizeBytes)} • {formatDate(dataset.uploadedAt)}
                        </p>
                    </div>
                </div>

                {dataset.processed ? (
                    <CheckCircle className="w-6 h-6 text-green-600" />
                ) : (
                    <Clock className="w-6 h-6 text-yellow-600 animate-pulse" />
                )}
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                <div>
                    <p className="text-gray-500">Rows</p>
                    <p className="font-semibold text-gray-900">{dataset.rowCount || '-'}</p>
                </div>
                <div>
                    <p className="text-gray-500">Columns</p>
                    <p className="font-semibold text-gray-900">{dataset.columnCount || '-'}</p>
                </div>
            </div>

            <div className="flex gap-2">
                <button
                    onClick={handleChat}
                    disabled={!dataset.processed}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${dataset.processed
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        }`}
                >
                    <MessageSquare className="w-4 h-4" />
                    {dataset.processed ? 'Open Chat' : 'Processing...'}
                </button>
                <button
                    onClick={handleDelete}
                    className="px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                >
                    <Trash2 className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
};

export default DatasetCard;
