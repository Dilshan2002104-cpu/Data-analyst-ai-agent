"""
Context Manager Service
Tracks all data sources (CSV files and SQL connections) for each user
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContextManager:
    def __init__(self):
        """Initialize Context Manager"""
        # In-memory storage (in production, use Firestore or Redis)
        self.user_contexts = {}
    
    def register_csv_file(self, user_id, dataset_id, filename, metadata=None):
        """
        Register a CSV file for a user
        
        Args:
            user_id: User identifier
            dataset_id: Dataset identifier
            filename: CSV filename
            metadata: Optional metadata (row count, columns, etc.)
        """
        try:
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = {
                    'csvFiles': [],
                    'sqlDatabases': []
                }
            
            csv_entry = {
                'id': dataset_id,
                'name': filename,
                'type': 'csv',
                'registeredAt': datetime.now().isoformat(),
                'metadata': metadata or {}
            }
            
            # Check if already exists
            existing = [f for f in self.user_contexts[user_id]['csvFiles'] if f['id'] == dataset_id]
            if not existing:
                self.user_contexts[user_id]['csvFiles'].append(csv_entry)
                logger.info(f"Registered CSV file for user {user_id}: {filename}")
            
        except Exception as e:
            logger.error(f"Error registering CSV file: {str(e)}")
            raise
    
    def register_sql_connection(self, user_id, connection_id, name, db_type, metadata=None):
        """
        Register a SQL connection for a user
        
        Args:
            user_id: User identifier
            connection_id: Connection identifier
            name: Friendly name for the connection
            db_type: 'mysql' or 'postgresql'
            metadata: Optional metadata (host, database name, etc.)
        """
        try:
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = {
                    'csvFiles': [],
                    'sqlDatabases': []
                }
            
            sql_entry = {
                'id': connection_id,
                'name': name,
                'type': db_type,
                'registeredAt': datetime.now().isoformat(),
                'metadata': metadata or {}
            }
            
            # Check if already exists
            existing = [db for db in self.user_contexts[user_id]['sqlDatabases'] if db['id'] == connection_id]
            if not existing:
                self.user_contexts[user_id]['sqlDatabases'].append(sql_entry)
                logger.info(f"Registered SQL connection for user {user_id}: {name}")
            
        except Exception as e:
            logger.error(f"Error registering SQL connection: {str(e)}")
            raise
    
    def get_user_context(self, user_id):
        """
        Get all data sources for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            dict: {
                'csvFiles': [...],
                'sqlDatabases': [...]
            }
        """
        try:
            # Fetch from Firestore (Source of Truth)
            from services.firestore_service import firestore_service
            
            context = firestore_service.get_user_context(user_id)
            
            # Update memory cache (optional, but good for debugging)
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = {'csvFiles': [], 'sqlDatabases': []}
            
            self.user_contexts[user_id] = context
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting user context: {str(e)}")
            # Fallback to memory if Firestore fails
            return self.user_contexts.get(user_id, {
                'csvFiles': [],
                'sqlDatabases': []
            })
    
    def remove_csv_file(self, user_id, dataset_id):
        """Remove a CSV file from user's context"""
        try:
            if user_id in self.user_contexts:
                self.user_contexts[user_id]['csvFiles'] = [
                    f for f in self.user_contexts[user_id]['csvFiles'] 
                    if f['id'] != dataset_id
                ]
                logger.info(f"Removed CSV file {dataset_id} for user {user_id}")
        except Exception as e:
            logger.error(f"Error removing CSV file: {str(e)}")
            raise
    
    def remove_sql_connection(self, user_id, connection_id):
        """Remove a SQL connection from user's context"""
        try:
            if user_id in self.user_contexts:
                self.user_contexts[user_id]['sqlDatabases'] = [
                    db for db in self.user_contexts[user_id]['sqlDatabases'] 
                    if db['id'] != connection_id
                ]
                logger.info(f"Removed SQL connection {connection_id} for user {user_id}")
        except Exception as e:
            logger.error(f"Error removing SQL connection: {str(e)}")
            raise
    
    def get_source_by_name(self, user_id, source_name):
        """
        Find a data source by name
        
        Args:
            user_id: User identifier
            source_name: Name of the source (filename or connection name)
            
        Returns:
            dict: Source information or None
        """
        try:
            context = self.get_user_context(user_id)
            
            # Check CSV files
            for csv_file in context['csvFiles']:
                if csv_file['name'].lower() == source_name.lower():
                    return {'type': 'csv', 'source': csv_file}
            
            # Check SQL databases
            for sql_db in context['sqlDatabases']:
                if sql_db['name'].lower() == source_name.lower():
                    return {'type': 'sql', 'source': sql_db}
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding source by name: {str(e)}")
            raise


# Global instance
context_manager = ContextManager()
