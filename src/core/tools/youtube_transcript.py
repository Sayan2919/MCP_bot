import os
import tempfile
import logging
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import yt_dlp
import whisper
import torch
import sys
import time


@dataclass
class TranscriptResult:
    """Data class to hold transcript results"""
    video_url: str
    video_title: str
    transcript: str
    language: str
    confidence: float
    processing_time: float
    success: bool
    error_message: str = ""


class YouTubeTranscriptTool:
    """MCP tool for extracting YouTube audio and generating transcripts using Whisper
    
    This tool is optimized to:
    - Extract only audio streams (no video download)
    - Use efficient audio formats (m4a, webm, mp3)
    - Convert to WAV for optimal Whisper processing
    - Minimize bandwidth and storage usage
    """

    def __init__(self, model_size: str = "tiny"):
        """
        Initialize the YouTube Transcript Tool
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       Defaults to 'tiny' for faster processing
        """
        self.model_size = model_size
        self.whisper_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Supported model sizes
        self.supported_models = {
            'tiny': 'tiny.en',
            'base': 'base',
            'small': 'small',
            'medium': 'medium',
            'large': 'large'
        }
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def load_whisper_model(self) -> None:
        """Load the Whisper model (lazy loading)"""
        if self.whisper_model is None:
            try:
                self.logger.info(f"Loading Whisper model: {self.model_size}")
                self.whisper_model = whisper.load_model(
                    self.supported_models.get(self.model_size, 'base'),
                    device=self.device
                )
                self.logger.info(f"Whisper model loaded successfully on {self.device}")
            except Exception as e:
                self.logger.error(f"Failed to load Whisper model: {e}")
                raise

    def download_audio(self, video_url):
        """Download audio from YouTube video"""
        class YTDLPLogger:
            def debug(self, msg):
                if msg.startswith('[debug]'):
                    return
                print(msg, file=sys.stderr)
            def warning(self, msg):
                print(msg, file=sys.stderr)
            def error(self, msg):
                print(msg, file=sys.stderr)

        def progress_hook(d):
            if d['status'] == 'downloading':
                # Print progress to stderr to avoid interfering with MCP JSON
                if 'total_bytes' in d and d['total_bytes']:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    print(f"Downloading: {percent:.1f}%", file=sys.stderr)
                elif 'downloaded_bytes' in d:
                    print(f"Downloaded: {d['downloaded_bytes']} bytes", file=sys.stderr)
            elif d['status'] == 'finished':
                print("Download completed, processing audio...", file=sys.stderr)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'logger': YTDLPLogger(),
            'progress_hooks': [progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Starting YouTube download...", file=sys.stderr)
                info_dict = ydl.extract_info(video_url, download=True)
                audio_file = 'temp_audio.mp3'
                
                # Verify file exists
                if not os.path.exists(audio_file):
                    raise FileNotFoundError(f"Audio file {audio_file} was not created")
                
                print(f"Audio file ready: {audio_file}", file=sys.stderr)
                return audio_file
        except Exception as e:
            print(f"Download failed: {str(e)}", file=sys.stderr)
            raise

    def transcribe_audio(self, audio_file):
        """Transcribe audio file using Whisper"""
        try:
            print("Loading Whisper model...", file=sys.stderr)
            self.load_whisper_model()
            
            print("Starting transcription...", file=sys.stderr)
            result = self.whisper_model.transcribe(audio_file)
            print("Transcription completed!", file=sys.stderr)
            
            return result
        except Exception as e:
            print(f"Transcription failed: {str(e)}", file=sys.stderr)
            raise

    def get_transcript(self, video_url: str) -> TranscriptResult:
        """Get transcript for a YouTube video"""
        start_time = time.time()
        
        try:
            print(f"Starting transcript generation for: {video_url}", file=sys.stderr)
            
            # Download audio
            audio_file = self.download_audio(video_url)
            
            # Transcribe audio
            result = self.transcribe_audio(audio_file)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Clean up temporary files
            self.cleanup_temp_files()
            
            return TranscriptResult(
                video_url=video_url,
                video_title=result.get('text', 'Unknown'),
                transcript=result.get('text', ''),
                language=result.get('language', 'unknown'),
                confidence=result.get('confidence', 0.0),
                processing_time=processing_time,
                success=True,
                error_message=""
            )
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            print(f"Transcript generation failed: {error_msg}", file=sys.stderr)
            
            # Clean up on error too
            self.cleanup_temp_files()
            
            return TranscriptResult(
                video_url=video_url,
                video_title="",
                transcript="",
                language="",
                confidence=0,
                processing_time=processing_time,
                success=False,
                error_message=error_msg
            )

    def get_video_info(self, video_url: str) -> Dict[str, Any]:
        """Get video information without downloading (fast)"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown'),
                    'success': True
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_transcript_mcp(self, video_url: str) -> Dict[str, Any]:
        """MCP endpoint for getting transcript with better timeout handling"""
        try:
            print(f"Processing video: {video_url}", file=sys.stderr)
            
            # First get video info to estimate processing time
            video_info = self.get_video_info(video_url)
            if video_info.get('success'):
                duration = video_info.get('duration', 0)
                if duration > 600:  # 10 minutes
                    return {
                        "error": "Video too long (>10 minutes). Consider using a shorter video or smaller model.",
                        "estimated_time": f"{duration/60:.1f} minutes"
                    }
            
            result = self.get_transcript(video_url)
            return {
                "transcript": result.transcript,
                "title": result.video_title,
                "language": result.language,
                "confidence": result.confidence,
                "processing_time": result.processing_time,
                "success": result.success
            }
        except Exception as e:
            return {
                "error": f"Failed to process video: {str(e)}",
                "success": False
            }

    def estimate_processing_time(self, video_url: str) -> Dict[str, Any]:
        """Estimate processing time for a video without downloading"""
        try:
            video_info = self.get_video_info(video_url)
            if not video_info.get('success'):
                return video_info
            
            duration = video_info.get('duration', 0)
            
            # Rough estimates based on model size and video length
            model_times = {
                'tiny': {'download_factor': 0.1, 'transcribe_factor': 0.5},
                'base': {'download_factor': 0.1, 'transcribe_factor': 1.0},
                'small': {'download_factor': 0.1, 'transcribe_factor': 2.0},
                'medium': {'download_factor': 0.1, 'transcribe_factor': 4.0},
                'large': {'download_factor': 0.1, 'transcribe_factor': 8.0}
            }
            
            current_model = self.model_size
            current_estimate = (
                duration * model_times[current_model]['download_factor'] +
                duration * model_times[current_model]['transcribe_factor']
            )
            
            # Find fastest model
            fastest_model = min(model_times.keys(), 
                              key=lambda x: model_times[x]['transcribe_factor'])
            fastest_time = (
                duration * model_times[fastest_model]['download_factor'] +
                duration * model_times[fastest_model]['transcribe_factor']
            )
            
            return {
                'success': True,
                'video_duration': duration,
                'current_model': current_model,
                'estimated_time': current_estimate,
                'fastest_model': fastest_model,
                'fastest_time': fastest_time,
                'recommendation': f"Use '{fastest_model}' model for fastest processing" if fastest_model != current_model else f"'{current_model}' model is optimal for speed"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def change_model(self, new_model_size: str) -> Dict[str, Any]:
        """Change the Whisper model size"""
        if new_model_size not in self.supported_models:
            return {
                'success': False,
                'error': f"Unsupported model size. Available: {list(self.supported_models.keys())}"
            }
        
        try:
            self.model_size = new_model_size
            self.whisper_model = None  # Force reload
            return {
                'success': True,
                'message': f"Model changed to {new_model_size}",
                'new_model': new_model_size
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_device_info(self) -> Dict[str, Any]:
        """Get device information for debugging"""
        return {
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'current_model': self.model_size,
            'supported_models': list(self.supported_models.keys())
        }

    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            if os.path.exists('temp_audio.mp3'):
                os.remove('temp_audio.mp3')
                print("Temporary audio file cleaned up", file=sys.stderr)
        except Exception as e:
            print(f"Failed to cleanup temp files: {e}", file=sys.stderr)