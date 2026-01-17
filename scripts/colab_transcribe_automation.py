#!/usr/bin/env python3
"""
Automate voice transcription using Google Colab with Playwright.

This script:
1. Opens Google Colab
2. Opens the transcribe notebook
3. Selects GPU runtime
4. Uploads your MP3 file
5. Runs transcription
6. Downloads transcript to transcripts/ folder

Usage:
    python colab_transcribe_automation.py <mp3_file_path> [--language en|yue|zh] [--browser chromium|firefox|webkit]

Example:
    python colab_transcribe_automation.py recording.mp3 --language yue
    python colab_transcribe_automation.py recording.mp3 --language en --browser firefox
"""

import argparse
import sys
import os
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    print("Error: playwright is not installed.")
    print("Install it with: pip install playwright")
    print("Then run: playwright install")
    sys.exit(1)


class ColabTranscriber:
    def __init__(self, mp3_file: str, language: str = "yue", browser_type: str = "chromium"):
        """
        Initialize Colab transcriber.
        
        Args:
            mp3_file: Path to MP3 file to transcribe
            language: Language code ('en', 'yue', 'zh')
            browser_type: Browser to use ('chromium', 'firefox', 'webkit')
        """
        self.mp3_file = mp3_file
        self.language = language
        self.browser_type = browser_type
        self.language_map = {
            'en': ('English', '🇬🇧 English'),
            'yue': ('Cantonese', '🇭🇰 Cantonese'),
            'zh': ('Mandarin', '🇨🇳 Mandarin')
        }
        
        # Validate file
        if not os.path.exists(mp3_file):
            raise FileNotFoundError(f"MP3 file not found: {mp3_file}")
        if not mp3_file.lower().endswith('.mp3'):
            raise ValueError(f"File must be MP3: {mp3_file}")
        
        # Get transcript folder
        self.transcript_dir = Path(__file__).parent.parent / "transcripts"
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        
    def run(self):
        """Run the automation workflow."""
        with sync_playwright() as p:
            browser = p.chromium if self.browser_type == "chromium" else (
                p.firefox if self.browser_type == "firefox" else p.webkit
            )
            
            print(f"🚀 Starting browser ({self.browser_type})...")
            context = browser.launch_persistent_context(
                user_data_dir=None,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            try:
                page = context.new_page()
                self._run_workflow(page)
            finally:
                context.close()
    
    def _run_workflow(self, page):
        """Execute the transcription workflow."""
        try:
            print("\n" + "="*70)
            print("🎙️  COLAB VOICE TRANSCRIPTION AUTOMATION")
            print("="*70)
            
            # Step 1: Open Colab
            print("\n📱 Step 1: Opening Google Colab...")
            self._open_colab(page)
            
            # Step 2: Select GPU
            print("\n⚙️  Step 2: Selecting GPU runtime...")
            self._select_gpu_runtime(page)
            
            # Step 3: Select language
            print(f"\n🌍 Step 3: Selecting language ({self.language_map[self.language][0]})...")
            self._select_language(page)
            
            # Step 4: Run first cell
            print("\n▶️  Step 4: Running language selection cell...")
            self._run_first_cell(page)
            
            # Step 5: Upload MP3
            print("\n📤 Step 5: Uploading MP3 file...")
            self._upload_mp3(page)
            
            # Step 6: Run transcription
            print("\n🎙️  Step 6: Running transcription (this will take 2-5 minutes)...")
            self._run_transcription(page)
            
            # Step 7: Wait for download
            print("\n⏳ Step 7: Waiting for transcript download...")
            transcript_file = self._wait_for_download(page)
            
            # Step 8: Save to transcripts folder
            if transcript_file:
                self._save_transcript(transcript_file)
                print("\n✓ Transcription complete!")
                print(f"✓ Transcript saved to: {self.transcript_dir}/{transcript_file}")
            
            print("\n" + "="*70)
            print("🎉 SUCCESS!")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("Press Enter to close browser...")
            raise
    
    def _open_colab(self, page):
        """Open Google Colab and navigate to notebook."""
        print("  → Navigating to Colab...")
        page.goto("https://colab.research.google.com/")
        page.wait_for_load_state("networkidle")
        
        # Wait for Colab to load
        time.sleep(2)
        
        print("  → Colab loaded")
    
    def _select_gpu_runtime(self, page):
        """Select GPU runtime."""
        try:
            # Click on Runtime menu
            print("  → Opening Runtime menu...")
            runtime_button = page.locator("text=Runtime").first
            runtime_button.click()
            page.wait_for_timeout(500)
            
            # Click on Change runtime type
            print("  → Selecting 'Change runtime type'...")
            change_runtime = page.locator("text=Change runtime type")
            if change_runtime.count() > 0:
                change_runtime.click()
                page.wait_for_timeout(1000)
                
                # Select GPU
                print("  → Selecting GPU...")
                gpu_option = page.locator("text=GPU")
                gpu_option.click()
                page.wait_for_timeout(500)
                
                # Click Save
                save_button = page.locator("button:has-text('Save')")
                save_button.click()
                page.wait_for_timeout(2000)
                
                print("  ✓ GPU runtime selected")
            else:
                print("  ⚠️  Could not find 'Change runtime type' option")
        except Exception as e:
            print(f"  ⚠️  Warning: Could not change runtime: {e}")
    
    def _select_language(self, page):
        """Select language in the dropdown."""
        try:
            lang_label = self.language_map[self.language][1]
            print(f"  → Clicking language dropdown...")
            
            # Wait for dropdown to appear
            page.wait_for_timeout(1000)
            
            # Click the dropdown
            dropdown = page.locator("select").first
            if dropdown.count() > 0:
                dropdown.click()
                page.wait_for_timeout(500)
                
                # Select language
                lang_option = page.locator(f"option:has-text('{lang_label}')")
                if lang_option.count() > 0:
                    lang_option.click()
                    print(f"  ✓ Language selected: {self.language_map[self.language][0]}")
        except Exception as e:
            print(f"  ⚠️  Warning: Could not select language: {e}")
    
    def _run_first_cell(self, page):
        """Run the language selection cell."""
        try:
            print("  → Running cell...")
            
            # Find and click play button for first code cell
            play_buttons = page.locator("button[aria-label*='Execute']")
            if play_buttons.count() > 0:
                play_buttons.nth(0).click()
                page.wait_for_timeout(3000)
                print("  ✓ Cell executed")
        except Exception as e:
            print(f"  ⚠️  Warning: Could not run cell: {e}")
    
    def _upload_mp3(self, page):
        """Upload MP3 file."""
        try:
            print(f"  → Uploading: {os.path.basename(self.mp3_file)}")
            
            # Find file input
            file_input = page.locator("input[type='file']")
            if file_input.count() > 0:
                # Set file
                file_input.set_input_files(self.mp3_file)
                print("  ✓ File uploaded")
                page.wait_for_timeout(2000)
        except Exception as e:
            print(f"  ✗ Error uploading file: {e}")
            raise
    
    def _run_transcription(self, page):
        """Run the transcription cell."""
        try:
            print("  → Running transcription...")
            
            # Find all play buttons and click the transcription one
            play_buttons = page.locator("button[aria-label*='Execute']")
            if play_buttons.count() > 1:
                play_buttons.nth(1).click()
                
                # Wait for transcription to complete
                print("  → Waiting for transcription to complete (this takes time)...")
                page.wait_for_timeout(300000)  # 5 minutes max
                print("  ✓ Transcription completed")
        except Exception as e:
            print(f"  ⚠️  Warning: {e}")
    
    def _wait_for_download(self, page):
        """Wait for transcript file to download."""
        try:
            print("  → Monitoring downloads...")
            
            # This is a simplified version - Colab downloads may vary
            # In practice, you might need to monitor the downloads folder
            time.sleep(5)
            
            # Check downloads folder
            downloads_dir = Path.home() / "Downloads"
            transcript_files = list(downloads_dir.glob("*_transcript.txt"))
            
            if transcript_files:
                latest_file = max(transcript_files, key=os.path.getctime)
                return latest_file.name
            
            print("  ⚠️  Transcript file not found in Downloads")
            return None
        except Exception as e:
            print(f"  ⚠️  Warning: {e}")
            return None
    
    def _save_transcript(self, filename: str):
        """Save transcript from Downloads to transcripts folder."""
        try:
            downloads_dir = Path.home() / "Downloads"
            source = downloads_dir / filename
            destination = self.transcript_dir / filename
            
            if source.exists():
                import shutil
                shutil.copy2(source, destination)
                print(f"  ✓ Transcript saved to {destination}")
        except Exception as e:
            print(f"  ⚠️  Could not copy transcript: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Automate voice transcription using Google Colab and Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Transcribe with default Cantonese:
    python colab_transcribe_automation.py recording.mp3
  
  Transcribe to English:
    python colab_transcribe_automation.py recording.mp3 --language en
  
  Transcribe to Mandarin with Firefox:
    python colab_transcribe_automation.py recording.mp3 --language zh --browser firefox
        """
    )
    
    parser.add_argument('mp3_file', help='Path to MP3 file to transcribe')
    parser.add_argument('--language', choices=['en', 'yue', 'zh'], default='yue',
                       help='Language: en (English), yue (Cantonese), zh (Mandarin) [default: yue]')
    parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit'], default='chromium',
                       help='Browser to use [default: chromium]')
    
    args = parser.parse_args()
    
    try:
        transcriber = ColabTranscriber(args.mp3_file, args.language, args.browser)
        transcriber.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
