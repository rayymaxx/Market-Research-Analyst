import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def convert_md_to_pdf(md_content: str, output_path: str) -> str:
    """Convert Markdown content to PDF"""
    if not md_content or not md_content.strip():
        raise ValueError("Empty markdown content provided")
    
    print(f"Converting {len(md_content)} chars to PDF: {output_path}")
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
    
    # Add proper HTML structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Market Research Report</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Add CSS styling
    css_style = CSS(string="""
        @page { size: A4; margin: 1in; }
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        h1, h2, h3 { color: #2c3e50; margin-top: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        p { margin: 10px 0; }
    """)
    
    # Generate PDF
    HTML(string=full_html).write_pdf(output_path, stylesheets=[css_style])
    
    # Verify PDF was created
    if not Path(output_path).exists():
        raise Exception(f"PDF file was not created: {output_path}")
    
    file_size = Path(output_path).stat().st_size
    print(f"PDF created successfully: {file_size} bytes")
    
    return output_path