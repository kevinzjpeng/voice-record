#!/usr/bin/env python3
"""
Script to convert WAV files to MP3 format using ffmpeg.
Processes all WAV files recursively in the entire /opt/source/AI directory.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is installed and available."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        print("✓ ffmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg is not installed or not in PATH")
        return False

def convert_wav_to_mp3(input_path, output_path, quality='192k', delete_original=True):
    """
    Convert a single WAV file to MP3.
    
    Args:
        input_path (str): Path to input WAV file
        output_path (str): Path to output MP3 file
        quality (str): Audio bitrate (default: 192k)
        delete_original (bool): Whether to delete the original WAV file after conversion
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-codec:a', 'libmp3lame',
            '-b:a', quality,
            '-y',  # Overwrite output files without asking
            str(output_path)
        ]
        
        print(f"Converting {input_path.name} to MP3...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Successfully converted to {output_path.name}")
        
        # Delete original WAV file if requested
        if delete_original:
            try:
                input_path.unlink()
                print(f"  Deleted original: {input_path.name}")
            except OSError as e:
                print(f"  ⚠ Warning: Could not delete {input_path.name}: {e}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error converting {input_path.name}: {e.stderr}")
        return False

def main():
    """Main conversion process."""
    # Check if ffmpeg is available
    if not check_ffmpeg():
        sys.exit(1)
    
    # Get the AI project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent  # Go up to the AI directory
    
    # Check if AI directory exists
    if not project_root.exists():
        print(f"✗ Directory not found: {project_root}")
        sys.exit(1)
    
    # Find all WAV files recursively in the entire AI directory
    wav_files = list(project_root.rglob('*.wav'))
    
    if not wav_files:
        print(f"No WAV files found in {project_root} and its subdirectories")
        return
    
    print(f"Found {len(wav_files)} WAV file(s) to convert in {project_root}:")
    for wav_file in wav_files:
        # Display relative path for clarity
        relative_path = wav_file.relative_to(project_root)
        print(f"  - {relative_path}")
    
    # Convert each WAV file
    converted_count = 0
    for wav_file in wav_files:
        # Create output filename (same name but with .mp3 extension)
        mp3_file = wav_file.with_suffix('.mp3')
        
        if convert_wav_to_mp3(wav_file, mp3_file):
            converted_count += 1
    
    print(f"\nConversion complete: {converted_count}/{len(wav_files)} files successfully converted")

if __name__ == '__main__':
    main()