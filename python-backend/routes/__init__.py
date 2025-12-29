"""
Routes initialization file
"""

from .health import health_bp
from .process import process_bp
from .query import query_bp

__all__ = ['health_bp', 'process_bp', 'query_bp']
