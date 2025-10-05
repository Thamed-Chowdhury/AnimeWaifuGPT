import asyncio
from deep_translator import GoogleTranslator
import edge_tts
import io

async def generate_audio(TEXT):
    """
    Generate speech audio in memory and return as BytesIO object.
    """
    print("Running TTS (in-memory)...")

    # Translate text to Japanese
    JP_TEXT = GoogleTranslator(source='auto', target='ja').translate(TEXT)
    VOICE = "ja-JP-NanamiNeural"

    # Generate audio and keep it in memory instead of saving to file
    mp3_data = io.BytesIO()
    communicate = edge_tts.Communicate(
        JP_TEXT, VOICE, rate="+30%", volume="-50%", pitch="+25Hz"
    )

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_data.write(chunk["data"])
    mp3_data.seek(0)  # rewind to start
    return mp3_data
