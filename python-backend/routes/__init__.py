"""
Routes initialization file
"""

from .health import health_bp
from .process import process_bp
from .query import query_bp
from .sql import sql_bp
from .unified import unified_bp
from .reports import reports_bp

__all__ = ['health_bp', 'process_bp', 'query_bp', 'sql_bp', 'unified_bp', 'reports_bp']
