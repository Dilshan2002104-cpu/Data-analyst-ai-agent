"""
SQL Service for database connectivity and query execution
Supports MySQL and PostgreSQL databases
"""

import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from cryptography.fernet import Fernet
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLService:
    def __init__(self):
        """Initialize SQL Service"""
        self.connections = {}  # Cache of active connections
        # In production, store this key securely (environment variable)
        self.cipher_key = Fernet.generate_key()
        self.cipher = Fernet(self.cipher_key)
    
    def _create_connection_string(self, db_type, host, port, database, username, password):
        """
        Create SQLAlchemy connection string
        
        Args:
            db_type: 'mysql' or 'postgresql'
            host: Database host
            port: Database port
            database: Database name
            username: Username
            password: Password
            
        Returns:
            str: Connection string
        """
        if db_type == 'mysql':
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == 'postgresql':
            return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def test_connection(self, db_type, host, port, database, username, password):
        """
        Test database connection
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            logger.info(f"Testing connection to {db_type} database: {host}:{port}/{database}")
            
            connection_string = self._create_connection_string(
                db_type, host, port, database, username, password
            )
            
            engine = create_engine(connection_string, pool_pre_ping=True)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("Connection test successful")
            return {'success': True, 'message': 'Connection successful'}
            
        except SQLAlchemyError as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {'success': False, 'message': f'Connection failed: {str(e)}'}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def create_connection(self, connection_id, db_type, host, port, database, username, password):
        """
        Create and cache a database connection
        
        Args:
            connection_id: Unique identifier for this connection
            
        Returns:
            bool: Success status
        """
        try:
            connection_string = self._create_connection_string(
                db_type, host, port, database, username, password
            )
            
            engine = create_engine(connection_string, pool_pre_ping=True, pool_size=5)
            
            self.connections[connection_id] = {
                'engine': engine,
                'db_type': db_type,
                'database': database
            }
            
            logger.info(f"Connection created: {connection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating connection: {str(e)}")
            return False
    
    def get_schema(self, connection_id):
        """
        Get database schema (tables and columns)
        
        Returns:
            dict: Schema information
        """
        try:
            if connection_id not in self.connections:
                # Try to recover from Firestore
                from services.firestore_service import firestore_service
                
                logger.info(f"Connection {connection_id} not found in memory (get_schema), attempting recovery from Firestore...")
                conn_data = firestore_service.get_connection(connection_id)
                
                if conn_data:
                    logger.info("Connection found in Firestore, restoring...")
                    self.create_connection(
                        conn_data['id'],
                        conn_data['type'],
                        conn_data['host'],
                        conn_data['port'],
                        conn_data['database'],
                        conn_data['username'],
                        conn_data['password']
                    )
                else:
                    raise ValueError(f"Connection not found: {connection_id}")
            
            engine = self.connections[connection_id]['engine']
            inspector = inspect(engine)
            
            schema = {}
            for table_name in inspector.get_table_names():
                columns = []
                for column in inspector.get_columns(table_name):
                    columns.append({
                        'name': column['name'],
                        'type': str(column['type'])
                    })
                schema[table_name] = columns
            
            logger.info(f"Schema retrieved for {connection_id}: {len(schema)} tables")
            return schema
            
        except Exception as e:
            logger.error(f"Error getting schema: {str(e)}")
            raise
    
    def validate_sql(self, sql):
        """
        Validate SQL query for security
        
        Args:
            sql: SQL query string
            
        Returns:
            dict: {'valid': bool, 'message': str}
        """
        sql_upper = sql.upper().strip()
        
        # Only allow SELECT statements
        if not sql_upper.startswith('SELECT'):
            return {'valid': False, 'message': 'Only SELECT queries are allowed'}
        
        # Block dangerous keywords
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE']
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return {'valid': False, 'message': f'Keyword {keyword} is not allowed'}
        
        return {'valid': True, 'message': 'Query is valid'}
    
    def get_db_type(self, connection_id):
        """Get database type for a connection"""
        if connection_id in self.connections:
            return self.connections[connection_id]['db_type']
        return 'mysql' # Default

    def execute_query(self, connection_id, sql, limit=1000):
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            connection_id: Connection identifier
            sql: SQL query
            limit: Maximum rows to return
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            # Validate query
            validation = self.validate_sql(sql)
            if not validation['valid']:
                raise ValueError(validation['message'])
            
            if connection_id not in self.connections:
                # Try to recover from Firestore
                from services.firestore_service import firestore_service
                
                logger.info(f"Connection {connection_id} not found in memory, attempting recovery from Firestore...")
                conn_data = firestore_service.get_connection(connection_id)
                
                if conn_data:
                    logger.info("Connection found in Firestore, restoring...")
                    self.create_connection(
                        conn_data['id'],
                        conn_data['type'],
                        conn_data['host'],
                        conn_data['port'],
                        conn_data['database'],
                        conn_data['username'],
                        conn_data['password']
                    )
                else:
                    raise ValueError(f"Connection not found: {connection_id}")
            
            conn_info = self.connections[connection_id]
            engine = conn_info['engine']
            db_type = conn_info.get('db_type', 'mysql')
            
            # Add LIMIT if not present
            if 'LIMIT' not in sql.upper():
                sql = f"{sql} LIMIT {limit}"
            
            logger.info(f"Executing query on {connection_id}: {sql[:100]}...")
            
            # Execute query
            # For MySQL, we need to handle % characters if they exist (used in DATE_FORMAT)
            # SQLAlchemy/Pandas might treat them as parameter placeholders
            if db_type == 'mysql' and '%' in sql:
                # If we are not using parameters, we should double escape % to %%
                # But pandas read_sql might not need this if not passing params?
                # Actually, the error 'unsupported format character' suggests it DOES try to format.
                # So we escape % -> %%
                sql = sql.replace('%', '%%')

            df = pd.read_sql(sql, engine)
            
            logger.info(f"Query executed successfully. Rows returned: {len(df)}")
            return df
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def close_connection(self, connection_id):
        """Close and remove a connection"""
        if connection_id in self.connections:
            self.connections[connection_id]['engine'].dispose()
            del self.connections[connection_id]
            logger.info(f"Connection closed: {connection_id}")


# Global instance
sql_service = SQLService()
