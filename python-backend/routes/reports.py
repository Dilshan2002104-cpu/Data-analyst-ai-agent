"""
Reports Routes
API endpoints for PDF report generation and management
"""

from flask import Blueprint, request, jsonify, send_file
from services.report_writer_agent import report_writer_agent
import logging
import os

logger = logging.getLogger(__name__)

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    Generate PDF report from query results
    
    Request Body:
    {
        "userId": "user123",
        "title": "Sales Analysis Report",
        "query": "Show me sales trends",
        "insights": "...",
        "data": [...],
        "chartConfig": {...},
        "dataSource": "sales_test_db"
    }
    
    Response:
    {
        "success": true,
        "reportPath": "/path/to/report.pdf",
        "filename": "report_20240101_120000.pdf"
    }
    """
    try:
        data = request.json
        logger.info(f"Generating report for user: {data.get('userId')}")
        
        # Prepare report data
        report_data = {
            'title': data.get('title', 'Data Analysis Report'),
            'user_query': data.get('query', ''),
            'insights': data.get('insights', ''),
            'data': data.get('data', []),
            'chart_config': data.get('chartConfig'),
            'metadata': {
                'generated_by': data.get('userId', 'unknown'),
                'timestamp': data.get('timestamp', ''),
                'data_source': data.get('dataSource', 'Unknown')
            }
        }
        
        # Generate report
        report_path = report_writer_agent.generate_report(report_data)
        
        return jsonify({
            'success': True,
            'reportPath': report_path,
            'filename': os.path.basename(report_path)
        })
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_bp.route('/download/<filename>', methods=['GET'])
def download_report(filename):
    """
    Download a specific report
    
    Args:
        filename: Name of the report file
    
    Returns:
        PDF file download
    """
    try:
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        filepath = os.path.join(reports_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'Report not found'
            }), 404
        
        return send_file(
            filepath,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error downloading report: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_bp.route('/list', methods=['GET'])
def list_reports():
    """
    List all available reports
    
    Returns:
        List of report files with metadata
    """
    try:
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        
        if not os.path.exists(reports_dir):
            return jsonify({
                'success': True,
                'reports': []
            })
        
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(reports_dir, filename)
                stat = os.stat(filepath)
                
                reports.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': stat.st_ctime,
                    'modified': stat.st_mtime
                })
        
        # Sort by creation time (newest first)
        reports.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports
        })
        
    except Exception as e:
        logger.error(f"Error listing reports: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
