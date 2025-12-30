"""
SQL Agent Service
Generates SQL queries from natural language using Gemini
"""

import logging
from services.vertex_ai_service import VertexAIService
from services.sql_service import sql_service
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLAgent:
    def __init__(self):
        """Initialize SQL Agent"""
        self.vertex_ai = VertexAIService()
        self.sql_service = sql_service
    
    def _format_schema_for_prompt(self, schema):
        """
        Format database schema for LLM prompt
        
        Args:
            schema: Dictionary of tables and columns
            
        Returns:
            str: Formatted schema description
        """
        schema_text = []
        for table_name, columns in schema.items():
            cols = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
            schema_text.append(f"Table: {table_name}\nColumns: {cols}")
        
        return "\n\n".join(schema_text)
    
    def generate_sql(self, connection_id, question, schema=None):
        """
        Generate SQL query from natural language question
        
        Args:
            connection_id: Database connection ID
            question: Natural language question
            schema: Optional schema dict (if not provided, will fetch)
            
        Returns:
            dict: {'sql': str, 'explanation': str}
        """
        try:
            # Get schema if not provided
            if schema is None:
                schema = self.sql_service.get_schema(connection_id)
            
            # Format schema for prompt
            schema_text = self._format_schema_for_prompt(schema)
            
            # Get database type
            db_type = self.sql_service.get_db_type(connection_id)
            
            # Create prompt for SQL generation
            prompt = f"""You are a SQL expert. Generate a SQL query based on the user's question.
            
Target Database: {db_type.upper()}

Database Schema:
{schema_text}

User Question: {question}

IMPORTANT RULES:
1. Generate ONLY a SELECT query
2. Use proper JOINs when needed
3. Include appropriate WHERE clauses
4. Add LIMIT clause if not specified (default LIMIT 100)
5. Return ONLY the SQL query, no explanations or markdown
6. Use syntax specific to {db_type} (e.g. for dates: use DATE_FORMAT for MySQL, TO_CHAR for PostgreSQL)

SQL Query:"""

            logger.info(f"Generating SQL for question: {question}")
            
            # Generate SQL using Gemini
            sql_response = self.vertex_ai.gemini_model.generate_content(prompt)
            sql_query = sql_response.text.strip()
            
            # Clean up the response (remove markdown if present)
            if sql_query.startswith('```sql'):
                sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            elif sql_query.startswith('```'):
                sql_query = sql_query.replace('```', '').strip()
            
            logger.info(f"Generated SQL: {sql_query}")
            
            # Validate the generated SQL
            validation = self.sql_service.validate_sql(sql_query)
            if not validation['valid']:
                raise ValueError(f"Generated invalid SQL: {validation['message']}")
            
            return {
                'sql': sql_query,
                'explanation': f"Generated query to answer: {question}"
            }
            
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            raise
    
    def query_database(self, connection_id, question):
        """
        Complete workflow: Generate SQL from question and execute it
        
        Args:
            connection_id: Database connection ID
            question: Natural language question
            
        Returns:
            dict: {
                'sql': str,
                'data': list,
                'rowCount': int,
                'explanation': str
            }
        """
        try:
            logger.info(f"Processing natural language query: {question}")
            
            # Generate SQL
            sql_result = self.generate_sql(connection_id, question)
            sql_query = sql_result['sql']
            
            # Execute SQL
            df = self.sql_service.execute_query(connection_id, sql_query)
            
            # Convert to records
            data = df.to_dict('records')
            
            logger.info(f"Query executed successfully. Rows returned: {len(data)}")
            
            return {
                'sql': sql_query,
                'data': data,
                'rowCount': len(data),
                'explanation': sql_result['explanation']
            }
            
        except Exception as e:
            logger.error(f"Error in query_database: {str(e)}")
            raise
    
    def analyze_results(self, question, sql_query, data):
        """
        Use LLM to analyze query results and generate insights
        
        Args:
            question: Original question
            sql_query: SQL query that was executed
            data: Query results (list of dicts)
            
        Returns:
            str: Natural language analysis
        """
        try:
            # Convert data to text format
            if not data:
                return "No results found for your query."
            
            # Limit data for prompt (first 10 rows)
            sample_data = data[:10]
            # Use default=str to handle date/datetime objects that aren't serializable
            data_text = json.dumps(sample_data, indent=2, default=str)
            
            prompt = f"""You are a data analyst. Analyze the following query results and provide insights.

Original Question: {question}

SQL Query Executed:
{sql_query}

Query Results (showing first {len(sample_data)} of {len(data)} rows):
{data_text}

Provide a clear, concise analysis that:
1. Directly answers the user's question
2. Highlights key findings from the data
3. Mentions any notable patterns or trends

If the user asked for a chart, include a JSON chart configuration at the end.
The JSON must follow this EXACT format:
```json
{{
  "type": "bar", // or line, pie, area
  "title": "Chart Title",
  "xAxisKey": "column_name_for_x_axis",
  "yAxisKey": "column_name_for_y_axis",
  "data": [
    // Include the RELEVANT data rows here as an array of objects
    {{"column_name_for_x_axis": "value", "column_name_for_y_axis": 100}},
    ...
  ]
}}
```
Ensure "data" is an Array of objects, not an object.

Analysis:"""

            logger.info("Generating analysis of query results")
            
            response = self.vertex_ai.gemini_model.generate_content(prompt)
            analysis = response.text.strip()
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing results: {str(e)}")
            # Return basic summary if analysis fails
            return f"Query returned {len(data)} rows."
