"""
Flask Application for Data Analyst AI Service
Integrates Vertex AI Gemini 2.0 Flash and ChromaDB
"""

from flask import Flask
from flask_cors import CORS
import config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Import and register blueprints
from routes import health_bp, process_bp, query_bp, sql_bp, unified_bp, reports_bp

app.register_blueprint(health_bp)
app.register_blueprint(process_bp)
app.register_blueprint(query_bp)
app.register_blueprint(sql_bp)
app.register_blueprint(unified_bp)
app.register_blueprint(reports_bp)

logger.info("Flask application initialized successfully")


@app.route('/')
def index():
    """Root endpoint"""
    return {
        'service': 'Data Analyst AI Service',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'process': '/api/process',
            'query': '/api/query',
            'dataset_info': '/api/dataset/<dataset_id>/info'
        }
    }


if __name__ == '__main__':
    logger.info(f"Starting Flask server on port {config.PORT}")
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.FLASK_DEBUG
    )
