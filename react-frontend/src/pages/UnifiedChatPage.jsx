import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Database, FileText, Send } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import toast from 'react-hot-toast';

const UnifiedChatPage = () => {
    const navigate = useNavigate();
    const [sources, setSources] = useState({ csvFiles: [], sqlDatabases: [] });
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [loadingSources, setLoadingSources] = useState(true);

    const userId = localStorage.getItem('userId') || 'default_user';

    // Load user's data sources
    useEffect(() => {
        loadSources();
    }, []);

    const loadSources = async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/sql/sources/${userId}`);
            const data = await response.json();

            if (data.success) {
                setSources(data.sources);
            }
        } catch (error) {
            console.error('Error loading sources:', error);
        } finally {
            setLoadingSources(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = input.trim();
        setInput('');

        // Add user message to chat
        setMessages(prev => [...prev, {
            type: 'user',
            content: userMessage,
            timestamp: new Date()
        }]);

        setLoading(true);

        try {
            console.log('Sending unified query:', { userId, question: userMessage });
            console.log('Available sources:', sources);

            const response = await fetch('http://localhost:5000/api/unified/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId,
                    question: userMessage
                })
            });

            const data = await response.json();
            console.log('Unified query response:', data);

            if (data.success) {
                // Add AI response to chat
                setMessages(prev => [...prev, {
                    type: 'ai',
                    content: data.answer,
                    sourcesUsed: data.sourcesUsed,
                    rowCount: data.rowCount,
                    timestamp: new Date()
                }]);
            } else {
                console.error('Query failed:', data.message);
                toast.error(data.message || 'Query failed');
                // Show error in chat
                setMessages(prev => [...prev, {
                    type: 'ai',
                    content: `Error: ${data.message || 'Query failed'}`,
                    timestamp: new Date()
                }]);
            }
        } catch (error) {
            console.error('Error processing query:', error);
            toast.error('Error processing query: ' + error.message);
            // Show error in chat
            setMessages(prev => [...prev, {
                type: 'ai',
                content: `Error: ${error.message}`,
                timestamp: new Date()
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const totalSources = sources.csvFiles.length + sources.sqlDatabases.length;

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar - Data Sources */}
            <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
                <div className="p-4 border-b border-gray-200">
                    <h2 className="text-lg font-semibold text-gray-900">My Data Sources</h2>
                    <p className="text-sm text-gray-500 mt-1">{totalSources} sources</p>
                </div>

                <div className="flex-1 overflow-y-auto p-4">
                    {loadingSources ? (
                        <p className="text-sm text-gray-500">Loading...</p>
                    ) : (
                        <>
                            {/* CSV Files */}
                            {sources.csvFiles.length > 0 && (
                                <div className="mb-6">
                                    <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
                                        CSV Files
                                    </h3>
                                    <div className="space-y-2">
                                        {sources.csvFiles.map((file) => (
                                            <div
                                                key={file.id}
                                                className="flex items-center gap-2 p-2 rounded-md hover:bg-gray-50"
                                            >
                                                <FileText className="w-4 h-4 text-blue-600" />
                                                <span className="text-sm text-gray-700 truncate">
                                                    {file.name}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* SQL Databases */}
                            {sources.sqlDatabases.length > 0 && (
                                <div>
                                    <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">
                                        Databases
                                    </h3>
                                    <div className="space-y-2">
                                        {sources.sqlDatabases.map((db) => (
                                            <div
                                                key={db.id}
                                                className="flex items-center gap-2 p-2 rounded-md hover:bg-gray-50"
                                            >
                                                <Database className="w-4 h-4 text-green-600" />
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm text-gray-700 truncate">{db.name}</p>
                                                    <p className="text-xs text-gray-500">{db.type}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Empty State */}
                            {totalSources === 0 && (
                                <div className="text-center py-8">
                                    <p className="text-sm text-gray-500 mb-4">
                                        No data sources yet
                                    </p>
                                    <button
                                        onClick={() => navigate('/dashboard')}
                                        className="text-sm text-blue-600 hover:text-blue-700"
                                    >
                                        Upload CSV
                                    </button>
                                    <span className="text-sm text-gray-400 mx-2">or</span>
                                    <button
                                        onClick={() => navigate('/connect-database')}
                                        className="text-sm text-blue-600 hover:text-blue-700"
                                    >
                                        Connect Database
                                    </button>
                                </div>
                            )}
                        </>
                    )}
                </div>

                {/* Add Data Button */}
                <div className="p-4 border-t border-gray-200">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="w-full px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    >
                        + Add Data Source
                    </button>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <div className="bg-white border-b border-gray-200 px-6 py-4">
                    <h1 className="text-xl font-semibold text-gray-900">Unified Chat</h1>
                    <p className="text-sm text-gray-500">
                        Ask questions about any of your data sources
                    </p>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                    {messages.length === 0 ? (
                        <div className="text-center py-12">
                            <h2 className="text-lg font-semibold text-gray-700 mb-2">
                                Welcome to Unified Chat!
                            </h2>
                            <p className="text-gray-500 mb-6">
                                Ask questions about your CSV files and databases in one place
                            </p>
                            <div className="max-w-md mx-auto space-y-2 text-left">
                                <p className="text-sm text-gray-600">Try asking:</p>
                                <div className="space-y-1">
                                    <button
                                        onClick={() => setInput("What's the total revenue in sales.csv?")}
                                        className="block w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-md"
                                    >
                                        "What's the total revenue in sales.csv?"
                                    </button>
                                    <button
                                        onClick={() => setInput("Show top 10 customers from the database")}
                                        className="block w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-md"
                                    >
                                        "Show top 10 customers from the database"
                                    </button>
                                    <button
                                        onClick={() => setInput("Compare CSV data with database")}
                                        className="block w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-md"
                                    >
                                        "Compare CSV data with database"
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        messages.map((message, index) => (
                            <div key={index}>
                                {message.type === 'user' ? (
                                    <div className="flex justify-end">
                                        <div className="bg-blue-600 text-white rounded-lg px-4 py-2 max-w-2xl">
                                            {message.content}
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex flex-col gap-2">
                                        <ChatMessage
                                            message={{
                                                userMessage: messages[index - 1]?.content || '',
                                                aiResponse: message.content
                                            }}
                                        />
                                        {message.sourcesUsed && (
                                            <div className="text-xs text-gray-500 ml-12">
                                                Sources: {message.sourcesUsed.join(', ')} • {message.rowCount} rows
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))
                    )}

                    {loading && (
                        <div className="flex items-center gap-2 text-gray-500">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            <span className="ml-2">Analyzing...</span>
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="bg-white border-t border-gray-200 p-4">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask a question about your data..."
                            disabled={loading || totalSources === 0}
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                        />
                        <button
                            onClick={handleSend}
                            disabled={loading || !input.trim() || totalSources === 0}
                            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            <Send className="w-4 h-4" />
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UnifiedChatPage;
