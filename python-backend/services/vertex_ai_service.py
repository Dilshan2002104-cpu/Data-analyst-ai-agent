"""
Vertex AI Service for Gemini 2.0 Flash integration
Handles embeddings generation and natural language query responses
"""

import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VertexAIService:
    def __init__(self):
        """Initialize Vertex AI with credentials"""
        try:
            # Set credentials
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE_APPLICATION_CREDENTIALS
            
            # Initialize Vertex AI
            vertexai.init(
                project=config.GCP_PROJECT_ID,
                location=config.GCP_LOCATION
            )
            
            # Initialize models
            self.gemini_model = GenerativeModel(config.GEMINI_MODEL)
            self.embedding_model = TextEmbeddingModel.from_pretrained(config.EMBEDDING_MODEL)
            
            logger.info(f"Vertex AI initialized successfully with project: {config.GCP_PROJECT_ID}")
            
        except Exception as e:
            logger.error(f"Error initializing Vertex AI: {str(e)}")
            raise

    def generate_embeddings(self, texts):
        """
        Generate embeddings for a list of texts
        
        Args:
            texts (list): List of text strings to embed
            
        Returns:
            list: List of embedding vectors
        """
        try:
            if not texts:
                return []
            
            # Ensure texts is a list
            if isinstance(texts, str):
                texts = [texts]
            
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            # Generate embeddings
            embeddings = self.embedding_model.get_embeddings(texts)
            
            # Extract vectors
            vectors = [embedding.values for embedding in embeddings]
            
            logger.info(f"Generated {len(vectors)} embeddings successfully")
            return vectors
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def generate_response(self, prompt, context=None):
        """
        Generate AI response using Gemini 2.0 Flash
        
        Args:
            prompt (str): User's query
            context (str, optional): Additional context for the query
            
        Returns:
            str: AI-generated response
        """
        try:
            # Build the full prompt
            if context:
                full_prompt = f"""You are a helpful data analyst assistant. Use the following context to answer the user's question.

Context:
{context}

Question: {prompt}

Provide a clear, concise, and accurate answer based on the context provided.

IMPORTANT: If the user asks for a chart, graph, or visualization, OR if the answer involves comparing categories or trends, YOU MUST INCLUDE A JSON OBJECT at the very end of your response inside a ```json``` code block.

The JSON format must be compatible with Recharts and follow this structure:
```json
{{
  "type": "bar", // options: "bar", "line", "pie", "area"
  "title": "Chart Title",
  "data": [
    {{ "name": "Category A", "value": 10 }},
    {{ "name": "Category B", "value": 20 }}
  ],
  "xAxisKey": "name", // Valid key from data object for X-axis
  "yAxisKey": "value", // Valid key from data object for Y-axis (values)
  "colors": ["#8884d8", "#82ca9d", "#ffc658"] // Optional custom colors
}}
```

If no chart is needed, do NOT include any JSON."""
            else:
                full_prompt = prompt
            
            logger.info("Generating AI response")
            
            # Generate response
            response = self.gemini_model.generate_content(full_prompt)
            
            # Extract text from response
            response_text = response.text
            
            logger.info("AI response generated successfully")
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise

    def analyze_data(self, data_summary, query):
        """
        Analyze data and answer queries about it
        
        Args:
            data_summary (str): Summary or sample of the data
            query (str): User's question about the data
            
        Returns:
            str: Analysis and answer
        """
        try:
            prompt = f"""You are an expert data analyst. Analyze the following data and answer the question.

Data Summary:
{data_summary}

Question: {query}

Provide a detailed analysis with:
1. Direct answer to the question
2. Key insights from the data
3. Any relevant statistics or patterns

IMPORTANT: If the user asks for a chart, graph, or visualization, OR if the answer involves comparing categories or trends, YOU MUST INCLUDE A JSON OBJECT at the very end of your response inside a ```json``` code block.

The JSON format must be compatible with Recharts and follow this structure:
```json
{
  "type": "bar", // options: "bar", "line", "pie", "area"
  "title": "Chart Title",
  "data": [
    { "name": "Category A", "value": 10 },
    { "name": "Category B", "value": 20 }
  ],
  "xAxisKey": "name", // Valid key from data object for X-axis
  "yAxisKey": "value", // Valid key from data object for Y-axis (values)
  "colors": ["#8884d8", "#82ca9d", "#ffc658"] // Optional custom colors
}
```

If no chart is needed, do NOT include any JSON."""

            return self.generate_response(prompt)
            
        except Exception as e:
            logger.error(f"Error analyzing data: {str(e)}")
            raise
