import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def convert_md_to_pdf(md_content: str, output_path: str) -> str:
    """Convert Markdown content to PDF"""
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
    
    # Add CSS styling
    css_style = CSS(string="""
        @page { size: A4; margin: 1in; }
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1, h2, h3 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #f2f2f2; }
    """)
    
    # Generate PDF
    HTML(string=html_content).write_pdf(output_path, stylesheets=[css_style])
    return output_path