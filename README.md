# MCP_bot

A Python-based MCP (Model Context Protocol) bot with various tools including a powerful YouTube transcript generator.

## Features

- **Calculator Tool**: Mathematical calculations and unit conversions
- **Weather Tool**: Weather information retrieval
- **YouTube Transcript Tool**: Download YouTube videos and generate transcripts using OpenAI Whisper

## YouTube Transcript Tool

The YouTube Transcript Tool is a powerful feature that allows you to:
- Extract audio directly from YouTube streams (no video download)
- Generate high-quality transcripts using OpenAI Whisper
- Support multiple languages and model sizes
- Process audio efficiently with GPU acceleration when available
- Optimized for minimal bandwidth and storage usage

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MCP_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: The tool requires FFmpeg to be installed on your system:
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

### Usage

#### Basic Usage

```python
from core.tools.youtube_transcript import YouTubeTranscriptTool

# Initialize with default base model
tool = YouTubeTranscriptTool()

# Generate transcript
result = tool.generate_transcript("https://www.youtube.com/watch?v=VIDEO_ID")

if result.success:
    print(f"Title: {result.video_title}")
    print(f"Transcript: {result.transcript}")
    print(f"Language: {result.language}")
    print(f"Processing time: {result.processing_time:.2f}s")
else:
    print(f"Error: {result.error_message}")
```

#### Advanced Usage

```python
# Initialize with specific model size
tool = YouTubeTranscriptTool(model_size="large")  # Most accurate

# Generate transcript with specific language
result = tool.generate_transcript(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    language="en"  # Force English
)

# Change model size dynamically
tool.change_model("tiny")  # Fastest processing
```

#### Available Models

| Model | Parameters | Speed | Accuracy | Use Case |
|-------|------------|-------|----------|----------|
| `tiny` | 39M | Fastest | Lowest | Quick previews |
| `base` | 74M | Fast | Good | General use |
| `small` | 244M | Medium | Better | Quality focus |
| `medium` | 769M | Slow | High | Professional use |
| `large` | 1550M | Slowest | Highest | Best quality |

#### Supported Languages

The tool supports 99+ languages including:
- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Japanese (`ja`)
- Chinese (`zh`)
- And many more...

Use `auto` or leave empty for automatic language detection.

### Examples

#### Example 1: Basic Transcript Generation

```python
from core.tools.youtube_transcript import YouTubeTranscriptTool

tool = YouTubeTranscriptTool()
result = tool.generate_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if result.success:
    print(f"Video: {result.video_title}")
    print(f"Transcript: {result.transcript}")
```

#### Example 2: Multi-language Processing

```python
# Process Spanish video
result = tool.generate_transcript(
    "https://www.youtube.com/watch?v=SPANISH_VIDEO",
    language="es"
)
```

#### Example 3: Get Video Information

```python
# Get video details and audio format information
video_info = tool.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
print(f"Title: {video_info['title']}")
print(f"Duration: {video_info['duration']} seconds")
print(f"Uploader: {video_info['uploader']}")

# Show audio format details
if video_info.get('best_audio_format'):
    best_audio = video_info['best_audio_format']
    print(f"Best Audio: {best_audio['ext']} format, {best_audio.get('abr', 'Unknown')} kbps")

# Show processing time estimates
if video_info.get('estimated_processing_time'):
    est = video_info['estimated_processing_time']
    print(f"Estimated processing time: {est['total_time']:.1f} seconds")
```

### Running the Examples

1. **Basic Demo**:
```bash
python example_youtube_transcript_usage.py
```

2. **Test Tool**:
```bash
python test_youtube_transcript.py
```

### Performance Tips

1. **GPU Acceleration**: Install PyTorch with CUDA support for faster processing
2. **Model Selection**: Use `tiny` or `base` for quick results, `large` for best quality
3. **Language Specification**: Specify the language if known to improve accuracy
4. **Audio-Only Processing**: Tool automatically extracts only audio streams for efficiency
5. **Format Optimization**: Automatically selects best audio format (m4a, webm, mp3) and converts to WAV

### Optimization Benefits

The tool is optimized for efficiency:

- **Bandwidth**: Only downloads audio streams, not video
- **Storage**: Minimal temporary storage usage
- **Speed**: Direct audio extraction with format conversion
- **Quality**: Automatically selects highest quality audio format available
- **Estimation**: Provides processing time estimates before starting

### Troubleshooting

#### Common Issues

1. **FFmpeg not found**:
   - Install FFmpeg on your system
   - Ensure it's in your PATH

2. **CUDA out of memory**:
   - Use smaller model sizes (`tiny`, `base`)
   - Process shorter videos
   - Use CPU processing instead

3. **Download failures**:
   - Check internet connection
   - Verify YouTube URL is valid
   - Some videos may have download restrictions

4. **Import errors**:
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure Python 3.8+ is used

#### Error Handling

The tool provides detailed error messages and graceful fallbacks:

```python
result = tool.generate_transcript(video_url)

if not result.success:
    print(f"Error: {result.error_message}")
    print(f"Processing time: {result.processing_time:.2f}s")
```

### API Reference

#### YouTubeTranscriptTool Class

- `__init__(model_size: str = "base")`: Initialize with specified model size
- `generate_transcript(video_url: str, language: str = None) -> TranscriptResult`: Generate transcript
- `get_video_info(video_url: str) -> Dict[str, Any]`: Get video metadata
- `change_model(model_size: str) -> bool`: Change model size
- `get_supported_languages() -> Dict[str, str]`: Get supported languages
- `get_supported_models() -> Dict[str, str]`: Get supported models
- `get_device_info() -> Dict[str, str]`: Get device information

#### TranscriptResult Class

- `video_url: str`: Original video URL
- `video_title: str`: Video title
- `transcript: str`: Generated transcript text
- `language: str`: Detected language
- `confidence: float`: Transcription confidence score
- `processing_time: float`: Time taken to process
- `success: bool`: Whether transcription succeeded
- `error_message: str`: Error message if failed

### Contributing

Feel free to contribute improvements, bug fixes, or new features to the YouTube Transcript Tool!

## License

This project is licensed under the MIT License - see the LICENSE file for details.