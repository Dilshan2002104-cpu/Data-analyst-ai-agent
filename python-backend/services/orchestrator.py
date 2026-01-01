"""
Orchestrator Agent Service
Routes queries to appropriate agents (CSV or SQL) based on user question
"""

import logging
from services.vertex_ai_service import VertexAIService
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self):
        """Initialize Orchestrator"""
        self.vertex_ai = VertexAIService()
    
    def detect_sources(self, question, available_sources):
        """
        Analyze question and determine which data sources are needed
        
        Args:
            question: User's natural language question
            available_sources: Dict with 'csvFiles' and 'sqlDatabases' lists
            
        Returns:
            dict: {
                'sources': ['csv', 'sql'],
                'csv_targets': ['file1.csv'],
                'sql_targets': ['db1']
            }
        """
        try:
            # Format available sources for prompt
            csv_list = ", ".join([f['name'] for f in available_sources.get('csvFiles', [])])
            sql_list = ", ".join([db['name'] for db in available_sources.get('sqlDatabases', [])])
            
            prompt = f"""You are a routing agent. Analyze the user's question and determine which data sources are needed.

Available Data Sources:
- CSV Files: {csv_list if csv_list else 'None'}
- SQL Databases: {sql_list if sql_list else 'None'}

User Question: "{question}"

Determine which source(s) this question requires. Return ONLY a JSON object with this exact format:
{{
  "sources": ["csv", "sql"],
  "csv_targets": ["filename.csv"],
  "sql_targets": ["database_name"]
}}

Rules:
- If question mentions a specific file name, include it in csv_targets
- If question mentions "database" or "live data", include sql
- If question asks to "compare" sources, include both
- If unclear, default to csv if files exist, otherwise sql

JSON Response:"""

            logger.info(f"Detecting sources for question: {question}")
            
            response = self.vertex_ai.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response (remove markdown if present)
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Parse JSON
            decision = json.loads(response_text)
            
            # Check if user wants a report generated
            report_keywords = ['report', 'pdf', 'document', 'generate report', 'create report', 'download report']
            generate_report = any(keyword in question.lower() for keyword in report_keywords)
            decision['generate_report'] = generate_report
            
            logger.info(f"Source detection result: {decision}")
            
            return decision
            
        except Exception as e:
            logger.error(f"Error detecting sources: {str(e)}")
            # Default fallback: use CSV if available, otherwise SQL
            if available_sources.get('csvFiles'):
                return {
                    'sources': ['csv'],
                    'csv_targets': [available_sources['csvFiles'][0]['name']],
                    'sql_targets': [],
                    'generate_report': False
                }
            else:
                return {
                    'sources': ['sql'],
                    'csv_targets': [],
                    'sql_targets': [available_sources['sqlDatabases'][0]['name']] if available_sources.get('sqlDatabases') else [],
                    'generate_report': False
                }
    
    def merge_results(self, csv_results=None, sql_results=None, question=""):
        """
        Merge results from multiple agents
        
        Args:
            csv_results: Results from CSV agent
            sql_results: Results from SQL agent
            question: Original question
            
        Returns:
            dict: Merged results with combined analysis
        """
        try:
            merged_data = []
            sources_used = []
            
            if csv_results:
                merged_data.extend(csv_results.get('data', []))
                sources_used.append('CSV')
            
            if sql_results:
                merged_data.extend(sql_results.get('data', []))
                sources_used.append('SQL Database')
            
            # Generate combined analysis if both sources used
            if csv_results and sql_results:
                analysis = self._generate_comparison_analysis(
                    question, csv_results, sql_results
                )
            elif csv_results:
                analysis = csv_results.get('analysis', csv_results.get('response', ''))
            elif sql_results:
                analysis = sql_results.get('analysis', '')
            else:
                analysis = "No results found."
            
            return {
                'data': merged_data,
                'analysis': analysis,
                'sourcesUsed': sources_used,
                'rowCount': len(merged_data)
            }
            
        except Exception as e:
            logger.error(f"Error merging results: {str(e)}")
            raise
    
    def _generate_comparison_analysis(self, question, csv_results, sql_results):
        """
        Generate analysis comparing CSV and SQL results
        
        Args:
            question: Original question
            csv_results: CSV agent results
            sql_results: SQL agent results
            
        Returns:
            str: Comparison analysis
        """
        try:
            prompt = f"""You are a data analyst. Compare results from two different data sources.

Original Question: {question}

CSV File Results:
{json.dumps(csv_results.get('data', [])[:5], indent=2)}
(Showing first 5 of {len(csv_results.get('data', []))} rows)

SQL Database Results:
{json.dumps(sql_results.get('data', [])[:5], indent=2)}
(Showing first 5 of {len(sql_results.get('data', []))} rows)

Provide a comparison analysis that:
1. Highlights similarities and differences
2. Identifies any discrepancies
3. Provides insights from both sources
4. Answers the original question

If appropriate, include a JSON chart configuration to visualize the comparison.

Analysis:"""

            logger.info("Generating comparison analysis")
            
            response = self.vertex_ai.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating comparison: {str(e)}")
            return f"CSV returned {len(csv_results.get('data', []))} rows. SQL returned {len(sql_results.get('data', []))} rows."
