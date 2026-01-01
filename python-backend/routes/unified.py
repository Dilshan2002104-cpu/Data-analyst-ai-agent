"""
Unified query route
Handles queries across both CSV and SQL data sources using the Orchestrator
"""

from flask import Blueprint, request, jsonify
from services import (
    Orchestrator, 
    context_manager, 
    ChromaDBService, 
    VertexAIService,
    SQLAgent
)
import logging
import os

logger = logging.getLogger(__name__)

unified_bp = Blueprint('unified', __name__)

# Initialize services
orchestrator = Orchestrator()
chromadb = ChromaDBService()
vertex_ai = VertexAIService()


@unified_bp.route('/api/unified/query', methods=['POST'])
def unified_query():
    """
    Unified query endpoint that works with both CSV and SQL sources
    
    Request JSON:
        {
            "userId": "user123",
            "question": "Compare sales.csv with the database"
        }
    
    Returns:
        JSON with answer, data, charts, and sources used
    """
    try:
        data = request.get_json()
        
        user_id = data.get('userId')
        question = data.get('question')
        
        if not all([user_id, question]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: userId, question'
            }), 400
        
        logger.info(f"Processing unified query for user {user_id}: {question}")
        
        # Step 1: Get user's available data sources
        available_sources = context_manager.get_user_context(user_id)
        
        if not available_sources['csvFiles'] and not available_sources['sqlDatabases']:
            return jsonify({
                'success': False,
                'message': 'No data sources available. Please upload a CSV or connect a database.'
            }), 400
        
        # Step 2: Use Orchestrator to detect which sources are needed
        decision = orchestrator.detect_sources(question, available_sources)
        
        logger.info(f"Orchestrator decision: {decision}")
        
        # Step 3: Query the appropriate agents
        csv_results = None
        sql_results = None
        
        # Query CSV sources if needed
        if 'csv' in decision['sources'] and decision['csv_targets']:
            csv_results = _query_csv_sources(
                user_id, 
                question, 
                decision['csv_targets'],
                available_sources['csvFiles']
            )
        
        # Query SQL sources if needed
        if 'sql' in decision['sources'] and decision['sql_targets']:
            sql_results = _query_sql_sources(
                user_id,
                question,
                decision['sql_targets'],
                available_sources['sqlDatabases']
            )
        
        # Step 4: Merge results
        merged_results = orchestrator.merge_results(
            csv_results=csv_results,
            sql_results=sql_results,
            question=question
        )
        
        # Step 5: Generate report if requested
        report_path = None
        report_filename = None
        if decision.get('generate_report', False):
            try:
                from services.report_writer_agent import report_writer_agent
                from datetime import datetime
                
                # Extract chart config if present in analysis
                chart_config = None
                analysis_text = merged_results['analysis']
                
                # Try to extract JSON chart config from analysis
                import json
                import re
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', analysis_text, re.DOTALL)
                if json_match:
                    try:
                        chart_config = json.loads(json_match.group(1))
                    except:
                        pass
                
                # Prepare report data
                report_data = {
                    'title': f"Data Analysis Report - {datetime.now().strftime('%Y-%m-%d')}",
                    'user_query': question,
                    'insights': analysis_text,
                    'data': merged_results['data'],
                    'chart_config': chart_config,
                    'metadata': {
                        'generated_by': user_id,
                        'timestamp': datetime.now().isoformat(),
                        'data_source': ', '.join(merged_results['sourcesUsed'])
                    }
                }
                
                # Generate report
                report_path = report_writer_agent.generate_report(report_data)
                report_filename = os.path.basename(report_path)
                logger.info(f"Report generated: {report_filename}")
                
            except Exception as e:
                logger.error(f"Error generating report: {str(e)}")
                # Continue without report if generation fails
        
        logger.info(f"Query completed. Sources used: {merged_results['sourcesUsed']}")
        
        response_data = {
            'success': True,
            'answer': merged_results['analysis'],
            'data': merged_results['data'],
            'rowCount': merged_results['rowCount'],
            'sourcesUsed': merged_results['sourcesUsed']
        }
        
        # Add report info if generated
        if report_filename:
            response_data['reportGenerated'] = True
            response_data['reportFilename'] = report_filename
            response_data['reportDownloadUrl'] = f"/api/reports/download/{report_filename}"
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error processing unified query: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def _query_csv_sources(user_id, question, target_files, available_files):
    """
    Query CSV sources using ChromaDB and Vertex AI
    
    Args:
        user_id: User identifier
        question: User's question
        target_files: List of target filenames
        available_files: List of available CSV files
        
    Returns:
        dict: CSV query results
    """
    try:
        # Find the dataset ID for the target file
        dataset_id = None
        for csv_file in available_files:
            if csv_file['name'] in target_files:
                dataset_id = csv_file['id']
                break
        
        if not dataset_id:
            logger.warning(f"CSV file not found: {target_files}")
            return None
        
        logger.info(f"Querying CSV dataset: {dataset_id}")
        
        # Get collection
        collection = chromadb.get_collection(dataset_id)
        
        # Search for relevant context
        results = chromadb.query_collection(collection, question, n_results=5)
        
        # Build context from results
        context = "\n\n".join(results['documents'][0]) if results['documents'] else ""
        
        # Generate response using Vertex AI
        response = vertex_ai.generate_response(question, context)
        
        return {
            'response': response,
            'data': [],  # Could parse data from context if needed
            'source': target_files[0]
        }
        
    except Exception as e:
        logger.error(f"Error querying CSV sources: {str(e)}")
        return None


def _query_sql_sources(user_id, question, target_databases, available_databases):
    """
    Query SQL sources using SQL Agent
    
    Args:
        user_id: User identifier
        question: User's question
        target_databases: List of target database names
        available_databases: List of available databases
        
    Returns:
        dict: SQL query results
    """
    try:
        # Find the connection ID for the target database
        connection_id = None
        for sql_db in available_databases:
            if sql_db['name'] in target_databases:
                connection_id = sql_db['id']
                break
        
        if not connection_id:
            logger.warning(f"SQL database not found: {target_databases}")
            return None
        
        logger.info(f"Querying SQL database: {connection_id}")
        
        # Use SQL Agent to query
        sql_agent = SQLAgent()
        result = sql_agent.query_database(connection_id, question)
        
        # Analyze results
        analysis = sql_agent.analyze_results(
            question,
            result['sql'],
            result['data']
        )
        
        return {
            'analysis': analysis,
            'data': result['data'],
            'sql': result['sql'],
            'source': target_databases[0]
        }
        
    except Exception as e:
        logger.error(f"Error querying SQL sources: {str(e)}")
        return None
