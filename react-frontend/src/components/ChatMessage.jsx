import { User, Bot } from 'lucide-react';

const ChatMessage = ({ message }) => {
    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="space-y-4">
            {/* User Message */}
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-gray-900">You</span>
                        <span className="text-xs text-gray-500">{formatTime(message.timestamp)}</span>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-3">
                        <p className="text-gray-900">{message.userMessage}</p>
                    </div>
                </div>
            </div>

            {/* AI Response */}
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold text-gray-900">AI Assistant</span>
                        {message.responseTimeMs && (
                            <span className="text-xs text-gray-500">
                                {(message.responseTimeMs / 1000).toFixed(1)}s
                            </span>
                        )}
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                        <p className="text-gray-900 whitespace-pre-wrap">{message.aiResponse}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;
