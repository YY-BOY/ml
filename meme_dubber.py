#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meme Dubber - A web application for generating audio from meme images
Uses Google Gemini API for text extraction and gTTS/ChatTTS for audio generation
"""

import os
import json
from io import BytesIO
from PIL import Image
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import Google Gemini SDK
from google import genai
from google.genai import types

# Get API key from environment
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file")


def extract_text_from_meme(image):
    """
    Extract text and language from meme image using Google Gemini API

    Args:
        image: PIL Image object

    Returns:
        tuple: (meme_text, lang_code)
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=GOOGLE_API_KEY)

        # Convert PIL Image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # System instruction for Gemini
        system_instruction = """
        You are an expert meme analyst.
        """

        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=img_byte_arr,
                    mime_type='image/png'
                ),
                """
                You are an expert meme analyst. Your task is to analyze the provided image.
                1.  First, determine if the image contains clear, readable text (e.g., captions, dialogue).
                2.  If it DOES contain text: Extract the text verbatim.
                3.  If it does NOT contain text (or the text is unreadable): Create a short, funny, meme-style dialogue that fits the scene, characters, and mood.
                4.  Identify the primary language of the extracted or generated text. Use standard language codes (e.g., 'en' for English, 'zh-tw' for Traditional Chinese, 'ja' for Japanese, 'es' for Spanish).
                5.  Return your response as a single JSON object with two keys: "language_code" and "text". Do not add any other explanatory text or formatting.

                Example for an English meme:
                {
                    "language_code": "en",
                    "text": "This is the text from the meme."
                }

                Example for a Japanese meme without text:
                {
                    "language_code": "ja",
                    "text": "面白いセリフを生成しました。"
                }
                """
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=1024
                ),
                temperature=0.7,
                response_mime_type="application/json"
            )
        )

        # Parse response
        print(f"Gemini response: {response.text}")  # Add debug info
        result = json.loads(response.text)
        meme_text = result.get('text', '')
        lang_code = result.get('language', 'en')
        
        # 確保返回有效的文本
        if not meme_text or meme_text.strip() == "":
            print("Warning: Empty text extracted from meme")
            return None, "en"

        return meme_text, lang_code

    except Exception as e:
        print(f"Error extracting text from meme: {e}")
        import traceback
        traceback.print_exc()
        return None, "en"  


def generate_audio_gtts(text, lang_code):
    """
    Generate audio using Google Text-to-Speech (gTTS)

    Args:
        text: Text to convert to speech
        lang_code: Language code (ISO 639-1)

    Returns:
        str: Path to generated audio file
    """
    try:
        from gtts import gTTS

        # Generate speech
        tts = gTTS(text=text, lang=lang_code)

        # Create full audio file path
        audio_filename = "meme_audio_gtts.mp3"
        audio_file = os.path.join(os.getcwd(), audio_filename)
        
        # Debug information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Audio file path: {audio_file}")
        print(f"Is directory: {os.path.isdir(audio_file)}")
        
        # Save audio file
        tts.save(audio_file)
        
        # Verify file was created
        if os.path.exists(audio_file):
            print(f"✓ Audio file created successfully: {audio_file}")
        else:
            print(f"✗ Failed to create audio file")
            return None

        return audio_file

    except Exception as e:
        print(f"Error generating audio with gTTS: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_audio_chattts(text, lang_code):
    """
    Generate audio using ChatTTS

    Args:
        text: Text to convert to speech
        lang_code: Language code (ISO 639-1)

    Returns:
        str: Path to generated audio file
    """
    try:
        import ChatTTS
        import soundfile as sf

        # Load ChatTTS model
        chat = ChatTTS.Chat()
        chat.load(compile=False)

        # Generate speech
        wavs = chat.infer([text])

        # Create full audio file path
        audio_filename = "meme_audio_chattts.wav"
        audio_file = os.path.join(os.getcwd(), audio_filename)
        
        # Debug information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Audio file path: {audio_file}")
        
        # Save audio file using soundfile
        sf.write(audio_file, wavs[0], 24000)
        
        # Verify file was created
        if os.path.exists(audio_file):
            print(f"✓ Audio file created successfully: {audio_file}")
        else:
            print(f"✗ Failed to create audio file")
            return None

        return audio_file

    except Exception as e:
        print(f"Error generating audio with ChatTTS: {e}")
        import traceback
        traceback.print_exc()
        return None


def process_meme(image, tts_engine):
    """
    Main function to process meme image and generate audio

    Args:
        image: PIL Image object from Gradio
        tts_engine: TTS engine to use ("gTTS" or "ChatTTS")

    Returns:
        tuple: (extracted_text, audio_file_path)
    """
    if image is None:
        return "**Error:** Please upload an image first.", None

    # Extract text from meme
    meme_text, lang_code = extract_text_from_meme(image)

    # 檢查文本提取是否成功
    if not meme_text or meme_text is None:
        return "**Error:** No text found in the image. Please try another image.", None

    # Generate audio based on selected TTS engine
    try:
        if tts_engine == "gTTS":
            audio_file = generate_audio_gtts(meme_text, lang_code)
        else:  # ChatTTS
            audio_file = generate_audio_chattts(meme_text, lang_code)
        
        # 檢查音檔是否生成成功
        if audio_file is None:
            result_text = f"**Extracted Text:** {meme_text}\n\n**Language:** {lang_code}\n\n**Error:** Failed to generate audio"
            return result_text, None
        
        result_text = f"**Extracted Text:** {meme_text}\n\n**Language:** {lang_code}"
        return result_text, audio_file
        
    except Exception as e:
        error_text = f"**Error generating audio:** {str(e)}\n\n**Extracted Text:** {meme_text}\n\n**Language:** {lang_code}"
        print(f"Error in process_meme: {e}")
        import traceback
        traceback.print_exc()
        return error_text, None


def create_gradio_interface():
    """
    Create and configure Gradio web interface

    Returns:
        gr.Blocks: Gradio interface
    """
    with gr.Blocks(title="Meme Dubber", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🎭 Meme Dubber

            Upload a meme image and generate audio dubbing using AI!

            **How it works:**
            1. Upload a meme image
            2. Select your preferred TTS engine (gTTS or ChatTTS)
            3. Click "Generate Audio Dub"
            4. Listen to the AI-generated voiceover!
            """
        )

        with gr.Row():
            with gr.Column():
                # Input components
                image_input = gr.Image(
                    label="Upload Meme Image",
                    type="pil",
                    sources=["upload", "clipboard"]
                )

                tts_selector = gr.Radio(
                    choices=["gTTS", "ChatTTS"],
                    value="gTTS",
                    label="TTS Engine",
                    info="gTTS: Fast and simple | ChatTTS: More natural sounding"
                )

                generate_btn = gr.Button("🎬 Generate Audio Dub", variant="primary", size="lg")

            with gr.Column():
                # Output components
                text_output = gr.Markdown(label="Extracted Text")
                audio_output = gr.Audio(label="Generated Audio", type="filepath")

        # Set up event handler
        generate_btn.click(
            fn=process_meme,
            inputs=[image_input, tts_selector],
            outputs=[text_output, audio_output]
        )

        gr.Markdown(
            """
            ---
            ### Notes:
            - **gTTS**: Google Text-to-Speech - Fast, cloud-based, supports many languages
            - **ChatTTS**: More natural sounding but requires more processing power
            - Supported languages: English, Chinese, Japanese, Spanish, and more!
            """
        )

    return demo


def main():
    """
    Main function to launch the application
    """
    print("Starting Meme Dubber...")
    print(f"API Key configured: {'✓' if GOOGLE_API_KEY else '✗'}")

    # Create and launch Gradio interface
    demo = create_gradio_interface()
    demo.launch(
        server_name="127.0.0.1",
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
