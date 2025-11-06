#!/usr/bin/env python3
"""
Transcribe audio files to Cantonese using OpenAI Whisper Large model.
"""

import os
import sys
import whisper
from pathlib import Path

def transcribe_audio_file(audio_path, model):
    """
    Transcribe a single audio file to Cantonese.
    
    Args:
        audio_path: Path to the audio file
        model: Loaded Whisper model
    """
    print(f"\n{'='*60}")
    print(f"Transcribing: {audio_path}")
    print(f"{'='*60}")
    
    try:
        # Transcribe with Cantonese language specified
        # Using language='zh' for Chinese, and Whisper will detect Cantonese
        result = model.transcribe(
            str(audio_path),
            language='zh',  # Chinese (includes Cantonese)
            task='transcribe',
            verbose=True
        )
        
        # Create transcript file path (same name as audio, but .txt extension)
        transcript_path = audio_path.with_suffix('.txt')
        
        # Write transcript to file
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(f"Transcript of: {audio_path.name}\n")
            f.write(f"Language: Cantonese/Chinese\n")
            f.write(f"{'='*60}\n\n")
            f.write(result['text'].strip())
            f.write("\n\n")
            f.write(f"{'='*60}\n")
            f.write("Detailed segments:\n\n")
            
            # Write detailed segments with timestamps
            for segment in result['segments']:
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                text = segment['text'].strip()
                f.write(f"[{start_time} -> {end_time}] {text}\n")
        
        print(f"\n✓ Transcript saved to: {transcript_path}")
        print(f"Text: {result['text'][:200]}..." if len(result['text']) > 200 else f"Text: {result['text']}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error transcribing {audio_path}: {str(e)}")
        return False

def format_timestamp(seconds):
    """Format seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def main():
    """Main function to process all changed audio files."""
    
    # Load Whisper large model
    print("Loading Whisper large model...")
    print("This may take a few minutes on first run...")
    model = whisper.load_model("large")
    print("✓ Model loaded successfully!\n")
    
    # Read changed files from the text file created in GitHub Actions
    changed_files_path = Path('changed_files.txt')
    
    if not changed_files_path.exists():
        print("No changed_files.txt found. Scanning voice-record directory...")
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        audio_files = []
        voice_record_dir = Path('voice-record')
        
        if voice_record_dir.exists():
            for ext in audio_extensions:
                audio_files.extend(voice_record_dir.rglob(f'*{ext}'))
        
        if not audio_files:
            print("No audio files found.")
            return
    else:
        # Read the list of changed files
        with open(changed_files_path, 'r') as f:
            changed_files = [line.strip() for line in f if line.strip()]
        
        if not changed_files:
            print("No audio files to transcribe.")
            return
        
        audio_files = [Path(f) for f in changed_files if Path(f).exists()]
    
    print(f"Found {len(audio_files)} audio file(s) to transcribe:\n")
    for audio_file in audio_files:
        print(f"  - {audio_file}")
    
    # Transcribe each audio file
    success_count = 0
    for audio_file in audio_files:
        if transcribe_audio_file(audio_file, model):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Transcription complete!")
    print(f"Successfully transcribed {success_count}/{len(audio_files)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
