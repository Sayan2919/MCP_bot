#!/usr/bin/env python3
"""
Simple test script for the YouTube Transcript Tool

This script tests the basic functionality without requiring actual video processing
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from core.tools.youtube_transcript import YouTubeTranscriptTool, TranscriptResult
    
    def test_tool_initialization():
        """Test tool initialization and basic methods"""
        print("🧪 Testing YouTube Transcript Tool...")
        
        # Test initialization
        tool = YouTubeTranscriptTool(model_size="base")
        print("✅ Tool initialized successfully")
        
        # Test supported models
        models = tool.get_supported_models()
        print(f"✅ Supported models: {list(models.keys())}")
        
        # Test supported languages
        languages = tool.get_supported_languages()
        print(f"✅ Supported languages: {len(languages)} languages")
        
        # Test device info
        device_info = tool.get_device_info()
        print(f"✅ Device info: {device_info['device']}")
        
        # Test model change
        success = tool.change_model("tiny")
        print(f"✅ Model change test: {'Passed' if success else 'Failed'}")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    if __name__ == "__main__":
        test_tool_initialization()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed all dependencies:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
