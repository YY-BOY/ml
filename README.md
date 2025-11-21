# 🎭 Meme Dubber

A web application that uses AI to extract text from meme images and generate audio dubbing using Google Gemini API and text-to-speech engines.

## Features

- Upload meme images via web interface or clipboard
- AI-powered text extraction using Google Gemini 2.5 Flash
- Smart text detection - extracts existing text or generates meme-style dialogue
- Multiple TTS engines:
  - **gTTS**: Fast, cloud-based Google Text-to-Speech
  - **ChatTTS**: More natural-sounding voice synthesis with local processing
- Automatic language detection and multi-language support
- Download generated audio files (MP3 for gTTS, WAV for ChatTTS)
- User-friendly Gradio web interface

## Prerequisites

- Python 3.8 or higher (3.12 recommended)
- Anaconda or Miniconda installed (recommended for environment management)
- Google API key for Gemini API ([Get one here](https://aistudio.google.com/app/apikey))
- Internet connection (required for gTTS and Gemini API)
- At least 2GB of free disk space (for ChatTTS models)

## Installation

1. **Clone the repository** (or download the files):
   ```bash
   git clone <repository-url>
   cd ml
   ```

2. **Create and activate conda environment**:
   ```bash
   conda create -n ml python=3.12
   conda activate ml
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

   **Important:** Never commit your `.env` file to version control!

## Usage

**Important:** Make sure your conda environment is activated before running:
```bash
conda activate ml
```

1. **Start the application**:
   ```bash
   python meme_dubber.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:7860
   ```

3. **Generate audio**:
   - Upload a meme image (or paste from clipboard)
   - Select your preferred TTS engine:
     - **gTTS**: Faster, requires internet
     - **ChatTTS**: Better quality, works offline (after initial setup)
   - Click "🎬 Generate Audio Dub"
   - View the extracted/generated text
   - Listen to and download the generated audio!

## TTS Engine Comparison

| Feature | gTTS | ChatTTS |
|---------|------|---------|
| Speed | ⚡ Fast | 🐢 Slower (first run requires model download) |
| Quality | ✅ Good | ⭐ Excellent, more natural |
| Languages | 🌍 Many (100+) | 🌏 Focus on Chinese/English |
| Requirements | 💻 Lightweight (~10MB) | 🖥️ Requires more resources (~2GB models) |
| Network | ☁️ Cloud-based (requires internet) | 💾 Local processing (offline after setup) |
| Output Format | MP3 | WAV (24kHz) |
| First-time Setup | ✅ Ready to use | ⏳ Downloads models (~2GB) |

## Supported Languages

The application automatically detects the language in your meme and generates audio accordingly. Supported languages include:

- English (en)
- Traditional Chinese (zh-tw)
- Simplified Chinese (zh-cn)
- Japanese (ja)
- Spanish (es)
- And many more!

## Project Structure

```
ml/
├── meme_dubber.py          # Main application script
├── requirements.txt         # Python dependencies
├── .env                    # API keys (create this, not tracked by git)
├── README.md               # Project documentation
├── asset/                  # ChatTTS model files (auto-downloaded)
│   ├── Decoder.safetensors
│   ├── DVAE.safetensors
│   ├── Embed.safetensors
│   ├── Vocos.safetensors
│   ├── gpt/
│   └── tokenizer/
├── meme_audio_gtts.mp3     # Output from gTTS
├── meme_audio_chattts.wav  # Output from ChatTTS
└── __pycache__/            # Python cache files
```

## Managing Conda Environment

**List all conda environments:**
```bash
conda env list
```

**Activate the ml environment:**
```bash
conda activate ml
```

**Deactivate environment:**
```bash
conda deactivate
```

**Remove environment (if needed):**
```bash
conda env remove -n ml
```

## Troubleshooting

### "GOOGLE_API_KEY not found" error
- Make sure you created a `.env` file in the project root
- Verify your API key is correctly set in the `.env` file: `GOOGLE_API_KEY=your_key_here`
- Check there are no extra spaces or quotes around the key
- Restart the application after creating/modifying `.env`

### "No text found in the image" error
- The image may not contain readable text
- Try a different meme image with clearer text
- The AI will attempt to generate meme-style dialogue if no text is detected

### "conda: command not found"
- Make sure Anaconda or Miniconda is installed
- Restart your terminal after installation
- Check conda installation: `conda --version`
- macOS: You may need to run `conda init zsh` and restart terminal

### Wrong conda environment
- Check active environment: `conda env list` (active one has an asterisk *)
- Activate the ml environment: `conda activate ml`
- Verify Python location: `which python` (should point to conda's ml environment)

### ChatTTS model download issues
- ChatTTS downloads models (~2GB) on first use to `asset/` directory
- Ensure you have stable internet connection
- Make sure you have at least 2GB free disk space
- Check write permissions in the project directory
- If download fails, delete `asset/` folder and try again

### ChatTTS fails to load or crashes
- ChatTTS requires more system resources and dependencies
- Ensure PyTorch is properly installed: `python -c "import torch; print(torch.__version__)"`
- Try using gTTS as a faster alternative
- Check if you have enough RAM (recommended: 4GB+)
- Verify all dependencies are installed in the conda environment

### Network errors with gTTS
- gTTS requires internet connection to Google's TTS service
- Check your network connectivity
- If behind a proxy, configure proxy settings
- Consider using ChatTTS for offline processing (after initial model download)

### "Audio file failed to create" error
- Check disk space availability
- Verify write permissions in the project directory
- Try the alternative TTS engine
- Check terminal output for detailed error messages

### Gradio interface won't open
- Make sure port 7860 is not in use: `lsof -i :7860`
- Try accessing via http://localhost:7860 instead of 127.0.0.1
- Check firewall settings
- Look for error messages in terminal output

## Development

This project converts a Colab notebook into a standalone local web application with the following changes:


### Key Technologies:
- **Google Gemini 2.5 Flash**: Advanced multimodal AI for image analysis
- **Thinking Mode**: Uses extended thinking budget (1024 tokens) for better text extraction
- **Gradio**: Modern web UI framework with Soft theme
- **PyTorch**: Powers ChatTTS's neural TTS engine
- **Transformers**: Hugging Face library for model management

## How It Works

### Text Extraction Process:
1. **Image Upload**: User uploads meme image via web interface
2. **AI Analysis**: Google Gemini 2.5 Flash analyzes the image with thinking mode
3. **Smart Detection**: 
   - If readable text exists → Extracts it verbatim
   - If no clear text → Generates meme-style dialogue fitting the scene
4. **Language Detection**: Automatically identifies the language (en, zh-tw, ja, es, etc.)
5. **JSON Response**: Returns structured data with text and language code

### Audio Generation Process:
1. **TTS Selection**: User chooses between gTTS or ChatTTS
2. **Audio Synthesis**:
   - **gTTS**: Sends text to Google's cloud TTS service → Returns MP3
   - **ChatTTS**: Uses local neural network → Generates WAV at 24kHz
3. **Output**: Audio file saved in project directory and displayed in browser
4. **Download**: User can play and download the generated audio



This project is provided as-is for educational and personal use.

## Credits

- [Google Gemini API](https://ai.google.dev/) - Multimodal AI for text extraction
- [gTTS](https://github.com/pndurette/gTTS) - Google Text-to-Speech
- [ChatTTS](https://github.com/2noise/ChatTTS) - Generative text-to-speech model
- [Gradio](https://www.gradio.app/) - Web interface framework
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [Transformers](https://huggingface.co/transformers/) - Hugging Face library

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Ideas for Contributions:
- Add support for more TTS engines
- Improve text extraction accuracy
- Add video support (extract frames and dub)
- Add voice customization options
- Multi-language UI
- Batch processing for multiple images
- Audio effects and filters
