"""
SQL routes for database connection and querying
"""

from flask import Blueprint, request, jsonify
from services import context_manager, sql_service
import logging

logger = logging.getLogger(__name__)

sql_bp = Blueprint('sql', __name__)

# Initialize SQL service
# sql_service = SQLService() # Removed, using imported instance


@sql_bp.route('/api/sql/connect', methods=['POST'])
def save_connection():
    """
    Save database connection and register with context manager
    
    Request JSON:
        {
            "userId": "user123",
            "connectionId": "conn_123",
            "name": "Production Database",
            "dbType": "mysql",
            "host": "localhost",
            "port": 3306,
            "database": "mydb",
            "username": "user",
            "password": "pass"
        }
    
    Returns:
        JSON with success status
    """
    try:
        data = request.get_json()
        
        user_id = data.get('userId')
        connection_id = data.get('connectionId')
        name = data.get('name')
        db_type = data.get('dbType')
        host = data.get('host')
        port = data.get('port')
        database = data.get('database')
        username = data.get('username')
        password = data.get('password', '')  # Default to empty string if not provided
        
        if not all([user_id, connection_id, name, db_type, host, port, database, username]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields (password is optional)'
            }), 400
        
        logger.info(f"Saving connection for user {user_id}: {name}")
        
        # Create connection in SQLService
        success = sql_service.create_connection(
            connection_id, db_type, host, port, database, username, password
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Failed to create database connection'
            }), 500
        
        # Register with context manager
        context_manager.register_sql_connection(
            user_id=user_id,
            connection_id=connection_id,
            name=name,
            db_type=db_type,
            metadata={
                'host': host,
                'database': database
            }
        )
        
        logger.info(f"Connection {connection_id} created and registered successfully")
        
        return jsonify({
            'success': True,
            'message': 'Connection saved successfully',
            'connectionId': connection_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error saving connection: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@sql_bp.route('/api/sql/test-connection', methods=['POST'])
def test_connection():
    """Test database connection"""
    try:
        data = request.get_json()
        
        db_type = data.get('dbType')
        host = data.get('host')
        port = data.get('port')
        database = data.get('database')
        username = data.get('username')
        password = data.get('password', '')  # Default to empty string
        
        if not all([db_type, host, port, database, username is not None]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields (password is optional)'
            }), 400
        
        logger.info(f"Testing connection to {db_type} database: {host}:{port}/{database}")
        
        result = sql_service.test_connection(
            db_type, host, port, database, username, password
        )
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@sql_bp.route('/api/sql/schema/<connection_id>', methods=['GET'])
def get_schema(connection_id):
    """Get database schema"""
    try:
        logger.info(f"Getting schema for connection: {connection_id}")
        
        schema = sql_service.get_schema(connection_id)
        
        return jsonify({
            'success': True,
            'schema': schema
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting schema: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@sql_bp.route('/api/sql/query', methods=['POST'])
def execute_query():
    """Execute SQL query"""
    try:
        data = request.get_json()
        
        connection_id = data.get('connectionId')
        sql = data.get('sql')
        
        if not all([connection_id, sql]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        logger.info(f"Executing query on {connection_id}")
        
        df = sql_service.execute_query(connection_id, sql)
        results = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': results,
            'rowCount': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@sql_bp.route('/api/sql/nl-query', methods=['POST'])
def natural_language_query():
    """Execute natural language query"""
    try:
        from services import SQLAgent
        
        data = request.get_json()
        
        connection_id = data.get('connectionId')
        question = data.get('question')
        
        if not all([connection_id, question]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        logger.info(f"Processing NL query: {question}")
        
        sql_agent = SQLAgent()
        result = sql_agent.query_database(connection_id, question)
        analysis = sql_agent.analyze_results(question, result['sql'], result['data'])
        
        return jsonify({
            'success': True,
            'sql': result['sql'],
            'data': result['data'],
            'rowCount': result['rowCount'],
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing NL query: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@sql_bp.route('/api/sql/sources/<user_id>', methods=['GET'])
def get_user_sources(user_id):
    """Get all data sources for a user"""
    try:
        logger.info(f"Getting sources for user: {user_id}")
        
        context = context_manager.get_user_context(user_id)
        
        return jsonify({
            'success': True,
            'sources': context
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting user sources: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
