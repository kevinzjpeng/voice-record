#!/usr/bin/env python3
"""
Prepare the Colab notebook for remote execution.
This modifies the notebook to work in a non-interactive mode.
"""

import json
import nbformat
from pathlib import Path

def prepare_notebook():
    """Prepare the Colab notebook for automated execution."""
    
    # Read the original notebook
    notebook_path = Path('transcribe_cantonese.ipynb')
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Create a modified version for automated execution
    automated_nb = nbformat.v4.new_notebook()
    automated_nb.metadata = nb.metadata.copy()
    
    # Read the list of changed files
    changed_files = []
    if Path('changed_files.txt').exists():
        with open('changed_files.txt', 'r') as f:
            changed_files = [line.strip() for line in f if line.strip()]
    
    # Add cells from original notebook, but modify the upload cell
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            automated_nb.cells.append(cell)
        elif cell.cell_type == 'code':
            # Skip the interactive upload cell
            if 'files.upload()' in cell.source:
                # Replace with automatic file loading
                new_cell = nbformat.v4.new_code_cell()
                new_cell.source = f"""# Automatically load files from repository
import os

uploaded = {{}}
audio_files = {changed_files}

print(f"Loading {{len(audio_files)}} file(s) from repository:")
for filepath in audio_files:
    if os.path.exists(filepath):
        filename = os.path.basename(filepath)
        # Copy to current directory for processing
        import shutil
        shutil.copy(filepath, filename)
        uploaded[filename] = True
        print(f"  - {{filename}}")
"""
                automated_nb.cells.append(new_cell)
            # Skip the download cell (we'll commit to git instead)
            elif 'files.download' in cell.source:
                new_cell = nbformat.v4.new_code_cell()
                new_cell.source = """# Transcripts will be committed to git
print("✓ Transcripts generated successfully!")
print("Files will be committed back to the repository.")
"""
                automated_nb.cells.append(new_cell)
            else:
                automated_nb.cells.append(cell)
    
    # Save the automated notebook
    output_path = Path('transcribe_automated.ipynb')
    with open(output_path, 'w') as f:
        nbformat.write(automated_nb, f)
    
    print(f"✓ Prepared automated notebook: {output_path}")
    print(f"  Will process {len(changed_files)} file(s)")

if __name__ == "__main__":
    prepare_notebook()
