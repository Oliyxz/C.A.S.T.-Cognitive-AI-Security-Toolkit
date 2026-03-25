import os
from faster_whisper import WhisperModel

# Use a lightweight model for CPU speed (approx 150MB download on first run)
MODEL_SIZE = "tiny.en" 

def transcribe_audio(audio_path):
    print("Initializing Offline Audio Transcriber (Whisper)...")
    try:
        # Use CPU to avoid complex CUDA/GPU installation nightmares for the user
        model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        
        print(f"Transcribing audio file: {audio_path}")
        # beam_size=5 provides highly accurate transcription
        segments, info = model.transcribe(audio_path, beam_size=5)
        
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "
            
        return full_text.strip()
        
    except Exception as e:
        print(f"Transcription Error: {e}")
        return f"AUDIO ERROR: {str(e)}\n\n(Note: If you get an ffmpeg error, you must install ffmpeg on your Windows system!)"
