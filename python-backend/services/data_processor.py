"""
Data Processor Service for CSV/Excel file handling
"""

import pandas as pd
import io
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    def __init__(self):
        """Initialize Data Processor"""
        pass

    def read_file(self, file_url, file_name):
        """
        Read CSV or Excel file from URL
        
        Args:
            file_url (str): Signed URL to the file
            file_name (str): Original file name
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            logger.info(f"Reading file: {file_name}")
            
            # Download file content
            response = requests.get(file_url)
            response.raise_for_status()
            
            file_content = response.content
            
            # Determine file type and read accordingly
            if file_name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                raise ValueError(f"Unsupported file type: {file_name}")
            
            logger.info(f"File loaded successfully. Shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise

    def profile_data(self, df):
        """
        Generate data profile with statistics
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            dict: Data profile information
        """
        try:
            logger.info("Generating data profile")
            
            profile = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'summary_stats': df.describe().to_dict() if len(df) > 0 else {}
            }
            
            logger.info(f"Data profile generated: {profile['row_count']} rows, {profile['column_count']} columns")
            return profile
            
        except Exception as e:
            logger.error(f"Error profiling data: {str(e)}")
            raise

    def chunk_dataframe(self, df, chunk_size=100):
        """
        Split dataframe into chunks for embedding
        
        Args:
            df (pd.DataFrame): Input dataframe
            chunk_size (int): Number of rows per chunk
            
        Returns:
            list: List of text chunks with metadata
        """
        try:
            logger.info(f"Chunking dataframe into chunks of {chunk_size} rows")
            
            chunks = []
            total_rows = len(df)
            
            for i in range(0, total_rows, chunk_size):
                chunk_df = df.iloc[i:i+chunk_size]
                
                # Convert chunk to text representation
                chunk_text = self.dataframe_to_text(chunk_df, start_row=i)
                
                chunks.append({
                    'text': chunk_text,
                    'start_row': i,
                    'end_row': min(i + chunk_size, total_rows),
                    'row_count': len(chunk_df)
                })
            
            logger.info(f"Created {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking dataframe: {str(e)}")
            raise

    def dataframe_to_text(self, df, start_row=0):
        """
        Convert dataframe to text representation for embedding
        
        Args:
            df (pd.DataFrame): Input dataframe
            start_row (int): Starting row number
            
        Returns:
            str: Text representation
        """
        try:
            # Create header
            text_parts = [f"Data rows {start_row} to {start_row + len(df) - 1}:"]
            text_parts.append(f"Columns: {', '.join(df.columns)}")
            text_parts.append("")
            
            # Add data rows
            for idx, row in df.iterrows():
                row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
                text_parts.append(row_text)
            
            return "\n".join(text_parts)
            
        except Exception as e:
            logger.error(f"Error converting dataframe to text: {str(e)}")
            raise

    def get_sample_data(self, df, n=5):
        """
        Get sample rows from dataframe
        
        Args:
            df (pd.DataFrame): Input dataframe
            n (int): Number of sample rows
            
        Returns:
            str: Text representation of sample data
        """
        try:
            sample_df = df.head(n)
            return self.dataframe_to_text(sample_df)
            
        except Exception as e:
            logger.error(f"Error getting sample data: {str(e)}")
            raise

    def format_for_llm(self, df, max_rows=100):
        """
        Format dataframe for LLM context
        
        Args:
            df (pd.DataFrame): Input dataframe
            max_rows (int): Maximum rows to include
            
        Returns:
            str: Formatted text for LLM
        """
        try:
            profile = self.profile_data(df)
            sample = self.get_sample_data(df, min(10, len(df)))
            
            formatted_text = f"""Dataset Information:
- Total Rows: {profile['row_count']}
- Total Columns: {profile['column_count']}
- Columns: {', '.join(profile['columns'])}

Sample Data:
{sample}

Column Data Types:
{chr(10).join([f"- {col}: {dtype}" for col, dtype in profile['dtypes'].items()])}
"""
            
            return formatted_text
            
        except Exception as e:
            logger.error(f"Error formatting for LLM: {str(e)}")
            raise
