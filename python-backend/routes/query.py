"""
Query route
Handles natural language queries with semantic search
"""

from flask import Blueprint, request, jsonify
from services import VertexAIService, ChromaDBService, DataProcessor
import logging

logger = logging.getLogger(__name__)

query_bp = Blueprint('query', __name__)

# Initialize services
vertex_ai = VertexAIService()
chromadb = ChromaDBService()
data_processor = DataProcessor()


@query_bp.route('/api/query', methods=['POST'])
def query_dataset():
    """
    Handle natural language query about a dataset
    
    Request JSON:
        {
            "datasetId": "uuid",
            "query": "What are the top 5 products?",
            "userId": "user_id"
        }
    
    Returns:
        JSON with AI-generated response
    """
    try:
        data = request.get_json()
        dataset_id = data.get('datasetId')
        query = data.get('query')
        user_id = data.get('userId')
        
        logger.info(f"Query request for dataset: {dataset_id}")
        
        # Validate inputs
        if not all([dataset_id, query]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: datasetId, query'
            }), 400
        
        # Step 1: Get the collection
        collection = chromadb.create_collection(dataset_id)
        
        # Check if collection has data
        doc_count = chromadb.get_collection_count(collection)
        if doc_count == 0:
            return jsonify({
                'success': False,
                'error': 'Dataset not processed yet or no data found'
            }), 404
        
        # Step 2: Generate query embedding
        query_embeddings = vertex_ai.generate_embeddings([query])
        query_embedding = query_embeddings[0]
        
        # Step 3: Perform semantic search
        search_results = chromadb.semantic_search(
            collection=collection,
            query_embedding=query_embedding,
            top_k=5
        )
        
        # Step 4: Build context from search results
        context_parts = []
        for i, doc in enumerate(search_results['documents']):
            metadata = search_results['metadatas'][i]
            context_parts.append(f"Data chunk (rows {metadata['start_row']}-{metadata['end_row']}):\n{doc}")
        
        context = "\n\n".join(context_parts)
        
        # Step 5: Generate AI response
        response_text = vertex_ai.generate_response(query, context)
        
        logger.info(f"Query processed successfully for dataset: {dataset_id}")
        
        return jsonify({
            'success': True,
            'response': response_text,
            'chunksUsed': len(search_results['documents'])
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@query_bp.route('/api/dataset/<dataset_id>/info', methods=['GET'])
def get_dataset_info(dataset_id):
    """
    Get information about a processed dataset
    
    Returns:
        JSON with dataset information
    """
    try:
        collection = chromadb.create_collection(dataset_id)
        doc_count = chromadb.get_collection_count(collection)
        
        return jsonify({
            'success': True,
            'datasetId': dataset_id,
            'documentCount': doc_count,
            'processed': doc_count > 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting dataset info: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
