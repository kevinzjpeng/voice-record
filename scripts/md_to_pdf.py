#!/usr/bin/env python3
"""
Convert Markdown files to PDF using WeasyPrint.

Usage:
    python md_to_pdf.py <markdown_file> [output_file]
    python md_to_pdf.py --batch <directory> [output_directory]
"""

import argparse
import sys
from pathlib import Path
from markdown import markdown
from weasyprint import HTML, CSS
from io import BytesIO


def md_to_pdf(md_file, output_file=None):
    """
    Convert a Markdown file to PDF.
    
    Args:
        md_file: Path to the Markdown file
        output_file: Path to save the PDF (default: same name with .pdf extension)
    
    Returns:
        bool: True if conversion was successful
    """
    md_path = Path(md_file)
    
    if not md_path.exists():
        print(f"Error: File not found: {md_file}")
        return False
    
    if not md_path.suffix.lower() in ['.md', '.markdown']:
        print(f"Error: File must be Markdown format (.md or .markdown): {md_file}")
        return False
    
    # Read the markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown(md_content, extensions=['extra', 'codehilite', 'toc'])
    
    # Create a full HTML document with styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{
                font-size: 2.5em;
                border-bottom: 3px solid #3498db;
                padding-bottom: 0.3em;
            }}
            h2 {{
                font-size: 2em;
                border-bottom: 1px solid #3498db;
                padding-bottom: 0.2em;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                border-left: 4px solid #3498db;
                padding: 12px;
                overflow-x: auto;
                border-radius: 3px;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin-left: 0;
                padding-left: 15px;
                color: #555;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            table th, table td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            table th {{
                background-color: #3498db;
                color: white;
            }}
            table tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            ul, ol {{
                margin: 1em 0;
                padding-left: 2em;
            }}
            li {{
                margin: 0.5em 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Determine output file path
    if output_file is None:
        output_file = md_path.with_suffix('.pdf')
    else:
        output_file = Path(output_file)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(str(output_file))
        print(f"✓ Successfully converted: {md_file} → {output_file}")
        return True
    except Exception as e:
        print(f"Error converting {md_file}: {e}")
        return False


def batch_convert(directory, output_directory=None):
    """
    Convert all Markdown files in a directory to PDF.
    
    Args:
        directory: Path to directory containing Markdown files
        output_directory: Path to save PDFs (default: same directory as source)
    """
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Directory not found: {directory}")
        return
    
    if output_directory is None:
        output_directory = directory
    else:
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)
    
    md_files = list(dir_path.glob('**/*.md')) + list(dir_path.glob('**/*.markdown'))
    
    if not md_files:
        print(f"No Markdown files found in: {directory}")
        return
    
    print(f"Found {len(md_files)} Markdown file(s)")
    successful = 0
    failed = 0
    
    for md_file in md_files:
        # Calculate relative output path
        rel_path = md_file.relative_to(dir_path)
        output_file = output_directory / rel_path.with_suffix('.pdf')
        
        if md_to_pdf(md_file, output_file):
            successful += 1
        else:
            failed += 1
    
    print(f"\nBatch conversion complete: {successful} successful, {failed} failed")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md_to_pdf.py transcripts/summary.md
  python md_to_pdf.py transcripts/summary.md output/summary.pdf
  python md_to_pdf.py --batch transcripts/
  python md_to_pdf.py --batch transcripts/ --output output/
        """
    )
    
    parser.add_argument('input', help='Input Markdown file or directory')
    parser.add_argument('output', nargs='?', help='Output PDF file or directory (optional)')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch convert all MD files in directory')
    
    args = parser.parse_args()
    
    if args.batch:
        batch_convert(args.input, args.output)
    else:
        success = md_to_pdf(args.input, args.output)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
