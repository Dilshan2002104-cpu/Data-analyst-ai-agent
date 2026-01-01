import { User, Bot, FileText, Download } from 'lucide-react';
import ChartRenderer from './ChartRenderer';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatMessage = ({ message }) => {
    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const parseResponse = (response) => {
        if (!response) return { text: '', chartConfig: null };

        let chartConfig = null;
        let text = response;

        // 1. Try to find Markdown Code Block
        const jsonBlockRegex = /```json\s*([\s\S]*?)\s*```/;
        const match = response.match(jsonBlockRegex);

        if (match) {
            try {
                chartConfig = JSON.parse(match[1]);
                text = response.replace(match[0], '').trim();
                return { text, chartConfig };
            } catch (e) {
                console.error("Failed to parse code block JSON", e);
            }
        }

        // 2. Fallback: Look for raw JSON object at the end of the string
        // We look for a pattern starting with { and containing "type" and "data"
        try {
            const lastOpenBrace = response.lastIndexOf('{');
            if (lastOpenBrace !== -1) {
                const potentialJson = response.substring(lastOpenBrace);
                // Basic check to see if it looks like our chart config before try-parsing
                if (potentialJson.includes('"type"') && potentialJson.includes('"data"')) {
                    const parsed = JSON.parse(potentialJson);
                    if (parsed.type && parsed.data) {
                        chartConfig = parsed;
                        text = response.substring(0, lastOpenBrace).trim();
                    }
                }
            }
        } catch (e) {
            // Check for common issue: Trailing text after JSON
            // Sometimes AI adds "Hope this helps!" after the JSON
            // We can try to find the last closing brace '}' that matches the last opening brace '{'
            // But for now, let's assume the JSON is at the end or near the end.
            console.log("Fallback JSON parse failed", e);
        }

        return { text, chartConfig };
    };

    const { text, chartConfig } = parseResponse(message.aiResponse);

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
                        <div className="prose prose-sm max-w-none text-gray-900">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {text}
                            </ReactMarkdown>
                        </div>

                        {/* Render Chart if config exists */}
                        {chartConfig && (
                            <div className="mt-4">
                                <ChartRenderer config={chartConfig} />
                            </div>
                        )}

                        {/* Render Report Download if available */}
                        {message.reportGenerated && message.reportDownloadUrl && (
                            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                                <div className="flex items-center gap-3">
                                    <div className="flex-shrink-0 w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                                        <FileText className="w-5 h-5 text-white" />
                                    </div>
                                    <div className="flex-1">
                                        <h4 className="font-semibold text-blue-900">PDF Report Generated</h4>
                                        <p className="text-sm text-blue-700">Your analysis has been compiled into a professional report</p>
                                    </div>
                                    <a
                                        href={`http://localhost:5000${message.reportDownloadUrl}`}
                                        download={message.reportFilename}
                                        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                                    >
                                        <Download className="w-4 h-4" />
                                        <span>Download PDF</span>
                                    </a>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;
