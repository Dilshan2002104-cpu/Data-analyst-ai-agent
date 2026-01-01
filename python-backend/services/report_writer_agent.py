"""
Report Writer Agent
Generates professional PDF reports from data analysis results
"""

import logging
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportWriterAgent:
    def __init__(self):
        """Initialize Report Writer Agent"""
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        logger.info(f"Report Writer Agent initialized. Reports directory: {self.reports_dir}")
    
    def generate_report(self, report_data):
        """
        Generate PDF report from analysis results
        
        Args:
            report_data: {
                'title': str,
                'user_query': str,
                'insights': str,
                'data': list[dict],
                'chart_config': dict (optional),
                'metadata': {
                    'generated_by': str,
                    'timestamp': str,
                    'data_source': str
                }
            }
        
        Returns:
            str: Path to generated PDF
        """
        try:
            logger.info(f"Generating report: {report_data.get('title', 'Untitled')}")
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{timestamp}.pdf"
            filepath = os.path.join(self.reports_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build story (content)
            story = []
            styles = getSampleStyleSheet()
            
            # Add custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1e3a8a'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#1e40af'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title Page
            story.extend(self._create_title_page(report_data, title_style, styles))
            story.append(PageBreak())
            
            # Executive Summary
            story.extend(self._create_executive_summary(report_data, heading_style, styles))
            story.append(Spacer(1, 0.3 * inch))
            
            # Data Analysis Section
            story.extend(self._create_analysis_section(report_data, heading_style, styles))
            
            # Chart Section (if chart config provided)
            if report_data.get('chart_config'):
                story.append(PageBreak())
                chart_image = self._create_chart_section(report_data['chart_config'])
                if chart_image:
                    story.append(Paragraph("Data Visualization", heading_style))
                    story.append(Spacer(1, 0.2 * inch))
                    story.append(chart_image)
            
            # Data Table Section (if data provided)
            if report_data.get('data') and len(report_data['data']) > 0:
                story.append(PageBreak())
                story.extend(self._create_data_table_section(report_data, heading_style, styles))
            
            # Build PDF
            doc.build(story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
            
            logger.info(f"Report generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _create_title_page(self, report_data, title_style, styles):
        """Create title page content"""
        story = []
        
        # Add spacing from top
        story.append(Spacer(1, 2 * inch))
        
        # Title
        title = report_data.get('title', 'Data Analysis Report')
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.5 * inch))
        
        # Subtitle with query
        query = report_data.get('user_query', '')
        if query:
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#64748b'),
                alignment=TA_CENTER,
                spaceAfter=12
            )
            story.append(Paragraph(f"<i>Query: {query}</i>", subtitle_style))
        
        story.append(Spacer(1, 1 * inch))
        
        # Metadata
        metadata = report_data.get('metadata', {})
        meta_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#475569'),
            alignment=TA_CENTER
        )
        
        generated_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        story.append(Paragraph(f"<b>Generated:</b> {generated_date}", meta_style))
        story.append(Spacer(1, 0.1 * inch))
        
        data_source = metadata.get('data_source', 'Unknown')
        story.append(Paragraph(f"<b>Data Source:</b> {data_source}", meta_style))
        
        return story
    
    def _create_executive_summary(self, report_data, heading_style, styles):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        insights = report_data.get('insights', 'No insights available.')
        
        # Split insights into paragraphs
        paragraphs = insights.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))
        
        return story
    
    def _create_analysis_section(self, report_data, heading_style, styles):
        """Create detailed analysis section"""
        story = []
        
        story.append(Paragraph("Detailed Analysis", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Original query
        query = report_data.get('user_query', '')
        if query:
            story.append(Paragraph(f"<b>Original Query:</b> {query}", styles['Normal']))
            story.append(Spacer(1, 0.15 * inch))
        
        # Data source info
        metadata = report_data.get('metadata', {})
        data_source = metadata.get('data_source', 'Unknown')
        story.append(Paragraph(f"<b>Data Source:</b> {data_source}", styles['Normal']))
        story.append(Spacer(1, 0.15 * inch))
        
        # Row count if available
        data = report_data.get('data', [])
        if data:
            story.append(Paragraph(f"<b>Records Analyzed:</b> {len(data)}", styles['Normal']))
        
        return story
    
    def _create_chart_section(self, chart_config):
        """Create chart visualization using matplotlib"""
        try:
            chart_type = chart_config.get('type', 'bar').lower()
            data = chart_config.get('data', [])
            x_key = chart_config.get('xAxisKey', '')
            y_key = chart_config.get('yAxisKey', '')
            title = chart_config.get('title', 'Data Visualization')
            
            if not data or not x_key or not y_key:
                return None
            
            # Extract data for plotting
            x_values = [item.get(x_key, '') for item in data]
            y_values = [item.get(y_key, 0) for item in data]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 5))
            
            if chart_type == 'bar':
                ax.bar(x_values, y_values, color='#3b82f6')
            elif chart_type == 'line':
                ax.plot(x_values, y_values, marker='o', linewidth=2, color='#3b82f6')
            elif chart_type == 'area':
                ax.fill_between(range(len(x_values)), y_values, alpha=0.5, color='#3b82f6')
                ax.plot(x_values, y_values, linewidth=2, color='#1e40af')
            elif chart_type == 'pie':
                ax.pie(y_values, labels=x_values, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
            
            if chart_type != 'pie':
                ax.set_xlabel(x_key)
                ax.set_ylabel(y_key)
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45, ha='right')
            
            ax.set_title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Save to bytes buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            # Create ReportLab Image
            img = Image(img_buffer, width=6*inch, height=3.75*inch)
            return img
            
        except Exception as e:
            logger.error(f"Error creating chart: {str(e)}")
            return None
    
    def _create_data_table_section(self, report_data, heading_style, styles):
        """Create data table section"""
        story = []
        
        story.append(Paragraph("Data Table", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        data = report_data.get('data', [])
        if not data:
            return story
        
        # Limit to first 20 rows for PDF
        display_data = data[:20]
        
        # Get column headers
        headers = list(display_data[0].keys())
        
        # Build table data
        table_data = [headers]
        for row in display_data:
            table_data.append([str(row.get(col, '')) for col in headers])
        
        # Create table
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(table)
        
        if len(data) > 20:
            story.append(Spacer(1, 0.2 * inch))
            note_style = ParagraphStyle(
                'Note',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#64748b'),
                fontName='Helvetica-Oblique'
            )
            story.append(Paragraph(f"<i>Note: Showing first 20 of {len(data)} records</i>", note_style))
        
        return story
    
    def _add_footer(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        
        # Page number
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#64748b'))
        canvas.drawRightString(7.5*inch, 0.5*inch, text)
        
        # Generated by text
        canvas.drawString(inch, 0.5*inch, "Generated by Data Analyst AI Agent")
        
        canvas.restoreState()


# Global instance
report_writer_agent = ReportWriterAgent()
