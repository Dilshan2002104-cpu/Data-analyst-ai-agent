"""
Dataset processing route
Handles file upload processing and embedding generation
"""

from flask import Blueprint, request, jsonify
from services import VertexAIService, ChromaDBService, DataProcessor
import logging

logger = logging.getLogger(__name__)

process_bp = Blueprint('process', __name__)

# Initialize services
vertex_ai = VertexAIService()
chromadb = ChromaDBService()
data_processor = DataProcessor()


@process_bp.route('/api/process', methods=['POST'])
def process_dataset():
    """
    Process uploaded dataset: read file, generate embeddings, store in ChromaDB
    
    Request JSON:
        {
            "datasetId": "uuid",
            "fileUrl": "signed_url",
            "fileName": "file.csv"
        }
    
    Returns:
        JSON with processing status and metadata
    """
    try:
        data = request.get_json()
        dataset_id = data.get('datasetId')
        file_url = data.get('fileUrl')
        file_name = data.get('fileName')
        
        logger.info(f"Processing dataset: {dataset_id}, file: {file_name}")
        
        # Validate inputs
        if not all([dataset_id, file_url, file_name]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: datasetId, fileUrl, fileName'
            }), 400
        
        # Step 1: Read the file
        df = data_processor.read_file(file_url, file_name)
        
        # Step 2: Profile the data
        profile = data_processor.profile_data(df)
        
        # Step 3: Create ChromaDB collection
        collection = chromadb.create_collection(dataset_id)
        
        # Step 4: Chunk the dataframe
        chunks = data_processor.chunk_dataframe(df, chunk_size=100)
        
        # Step 5: Generate embeddings for chunks
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = vertex_ai.generate_embeddings(chunk_texts)
        
        # Step 6: Store in ChromaDB
        metadatas = [
            {
                'start_row': chunk['start_row'],
                'end_row': chunk['end_row'],
                'row_count': chunk['row_count']
            }
            for chunk in chunks
        ]
        
        ids = [f"{dataset_id}_chunk_{i}" for i in range(len(chunks))]
        
        chromadb.add_documents(
            collection=collection,
            documents=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        # Step 7: Register with Context Manager
        from services import context_manager
        user_id = data.get('userId', 'default_user')  # Get from request
        context_manager.register_csv_file(
            user_id=user_id,
            dataset_id=dataset_id,
            filename=file_name,
            metadata={
                'rowCount': profile['row_count'],
                'columnCount': profile['column_count'],
                'columns': profile['columns']
            }
        )
        
        logger.info(f"Dataset processed successfully: {dataset_id}")
        
        return jsonify({
            'success': True,
            'message': 'Dataset processed successfully',
            'rowCount': profile['row_count'],
            'columnCount': profile['column_count'],
            'chunksCreated': len(chunks)
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing dataset: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
