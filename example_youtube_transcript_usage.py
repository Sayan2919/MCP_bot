#!/usr/bin/env python3
"""
Example usage of the YouTube Transcript Tool

This script demonstrates how to use the YouTubeTranscriptTool to:
1. Download YouTube videos
2. Generate transcripts using OpenAI Whisper
3. Handle different model sizes and languages
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from core.tools.youtube_transcript import YouTubeTranscriptTool


def main():
    """Main function demonstrating the YouTube Transcript Tool"""
    
    print("🎥 YouTube Transcript Tool Demo")
    print("=" * 50)
    
    # Initialize the tool with base model (good balance of speed/accuracy)
    print("\n📱 Initializing tool...")
    tool = YouTubeTranscriptTool(model_size="base")
    
    # Display device information
    device_info = tool.get_device_info()
    print(f"🖥️  Device: {device_info['device']}")
    print(f"🚀 CUDA Available: {device_info['cuda_available']}")
    
    # Display supported models
    print("\n🤖 Supported Whisper Models:")
    models = tool.get_supported_models()
    for size, description in models.items():
        print(f"  • {size}: {description}")
    
    # Display supported languages
    print("\n🌍 Supported Languages:")
    languages = tool.get_supported_languages()
    for code, name in list(languages.items())[:10]:  # Show first 10
        print(f"  • {code}: {name}")
    print("  • ... and more")
    
    # Example YouTube URL (replace with your own)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll example
    
    print(f"\n🎬 Processing video: {video_url}")
    print("⏳ This may take a few minutes depending on video length and model size...")
    
    try:
        # Generate transcript
        result = tool.generate_transcript(video_url, language="en")
        
        if result.success:
            print("\n✅ Transcript generated successfully!")
            print(f"📺 Video Title: {result.video_title}")
            print(f"🌍 Detected Language: {result.language}")
            print(f"🎯 Confidence: {result.confidence:.2f}")
            print(f"⏱️  Processing Time: {result.processing_time:.2f} seconds")
            print(f"\n📝 Transcript:")
            print("-" * 40)
            print(result.transcript)
            print("-" * 40)
        else:
            print(f"\n❌ Failed to generate transcript: {result.error_message}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
    
    # Example of changing model size
    print("\n🔄 Changing to tiny model for faster processing...")
    if tool.change_model("tiny"):
        print("✅ Model changed to tiny successfully")
    else:
        print("❌ Failed to change model")
    
    # Example of getting video info without downloading
    print("\n📊 Getting video information...")
    try:
        video_info = tool.get_video_info(video_url)
        print(f"📺 Title: {video_info['title']}")
        print(f"⏱️  Duration: {video_info['duration']} seconds")
        print(f"👤 Uploader: {video_info['uploader']}")
        print(f"👀 Views: {video_info['view_count']:,}")
        print(f"📅 Upload Date: {video_info['upload_date']}")
        
        # Show audio format information
        if video_info.get('best_audio_format'):
            best_audio = video_info['best_audio_format']
            print(f"🎵 Best Audio: {best_audio['ext']} format, {best_audio.get('abr', 'Unknown')} kbps")
        
        # Show processing time estimates
        if video_info.get('estimated_processing_time'):
            est = video_info['estimated_processing_time']
            print(f"⏱️  Estimated processing time: {est['total_time']:.1f} seconds")
            print(f"   - Audio extraction: {est['download_time']:.1f}s")
            print(f"   - Transcription: {est['transcription_time']:.1f}s")
    except Exception as e:
        print(f"❌ Failed to get video info: {e}")


def demo_with_custom_video():
    """Demo function for custom video URL"""
    
    print("\n" + "=" * 60)
    print("🎬 Custom Video Demo")
    print("=" * 60)
    
    # Get video URL from user
    video_url = input("Enter YouTube video URL: ").strip()
    
    if not video_url:
        print("❌ No URL provided")
        return
    
    # Get language preference
    language = input("Enter language code (e.g., 'en', 'es', 'fr') or press Enter for auto-detect: ").strip()
    if not language:
        language = None
    
    # Get model size preference
    print("\nAvailable models:")
    models = ["tiny", "base", "small", "medium", "large"]
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    
    try:
        choice = int(input("Select model (1-5): ")) - 1
        if 0 <= choice < len(models):
            model_size = models[choice]
        else:
            model_size = "base"
            print("Invalid choice, using 'base' model")
    except ValueError:
        model_size = "base"
        print("Invalid input, using 'base' model")
    
    print(f"\n🚀 Initializing with {model_size} model...")
    tool = YouTubeTranscriptTool(model_size=model_size)
    
    try:
        print("⏳ Generating transcript...")
        result = tool.generate_transcript(video_url, language=language)
        
        if result.success:
            print("\n✅ Success!")
            print(f"📺 Title: {result.video_title}")
            print(f"🌍 Language: {result.language}")
            print(f"⏱️  Time: {result.processing_time:.2f}s")
            print(f"\n📝 Transcript:")
            print("-" * 50)
            print(result.transcript)
            print("-" * 50)
        else:
            print(f"\n❌ Failed: {result.error_message}")
            
    except Exception as e:
        print(f"\n💥 Error: {e}")


if __name__ == "__main__":
    try:
        main()
        
        # Ask if user wants to try with custom video
        print("\n" + "=" * 60)
        custom = input("Would you like to try with a custom video? (y/n): ").strip().lower()
        if custom in ['y', 'yes']:
            demo_with_custom_video()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Make sure you have installed all required dependencies:")
        print("pip install -r requirements.txt")
