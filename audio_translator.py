"""
audio_translator.py — Push-to-talk audio translator
English ↔ German using:
  - sounddevice     : mic recording
  - faster-whisper  : local speech-to-text (free, fast on CPU)
  - Ollama/Groq     : translation
  - gTTS            : text-to-speech output

Install:
    pip install faster-whisper sounddevice gTTS pygame numpy
"""

import io
import os
import tempfile
import threading
import numpy as np

# ── Lazy loaders ──────────────────────────────────────────────────────────────
_whisper_model = None
_whisper_lock  = threading.Lock()

def get_whisper(model_size="base"):
    """Load faster-whisper model (downloads ~150MB on first use for 'base')."""
    global _whisper_model
    with _whisper_lock:
        if _whisper_model is None:
            try:
                from faster_whisper import WhisperModel
                # base = good balance of speed/accuracy on CPU
                # tiny = faster but less accurate
                # small = better accuracy, slower
                _whisper_model = WhisperModel(
                    model_size,
                    device="cpu",
                    compute_type="int8"  # fastest on CPU
                )
            except Exception as e:
                return None, str(e)
    return _whisper_model, None


def check_dependencies():
    status = {}
    for pkg, key in [
        ("faster_whisper", "whisper"),
        ("sounddevice",    "sounddevice"),
        ("gtts",           "gtts"),
        ("pygame",         "pygame"),
        ("numpy",          "numpy"),
    ]:
        try:
            __import__(pkg)
            status[key] = True
        except ImportError:
            status[key] = False
    return status


# ── Recording ─────────────────────────────────────────────────────────────────
def record_audio(duration_seconds=5, sample_rate=16000):
    """
    Record audio from the default microphone.
    Returns numpy array of float32 samples.
    """
    import sounddevice as sd
    audio = sd.rec(
        int(duration_seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )
    sd.wait()  # block until recording is done
    return audio.flatten(), sample_rate


def record_until_silence(max_seconds=10, sample_rate=16000, silence_threshold=0.01, silence_duration=1.2):
    """
    Record until silence is detected or max_seconds reached.
    Returns numpy array of float32 samples.
    
    silence_threshold: RMS below this = silence
    silence_duration: seconds of silence before stopping
    """
    import sounddevice as sd

    chunk_size = int(sample_rate * 0.1)  # 100ms chunks
    max_chunks = int(max_seconds * sample_rate / chunk_size)
    silence_chunks = int(silence_duration * sample_rate / chunk_size)

    audio_chunks = []
    silent_count = 0
    has_speech   = False

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32") as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_size)
            audio_chunks.append(chunk.flatten())
            rms = float(np.sqrt(np.mean(chunk ** 2)))

            if rms > silence_threshold:
                has_speech   = True
                silent_count = 0
            elif has_speech:
                silent_count += 1
                if silent_count >= silence_chunks:
                    break  # speech ended

    return np.concatenate(audio_chunks), sample_rate


# ── Transcription ──────────────────────────────────────────────────────────────
def transcribe(audio_array, sample_rate=16000, language=None):
    """
    Transcribe audio using faster-whisper.
    language: "en", "de", or None (auto-detect)
    Returns (text, detected_language)
    """
    model, err = get_whisper()
    if err:
        return "", err, "unknown"

    # Save to temp WAV file (faster-whisper needs a file path)
    import wave
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name

    try:
        audio_int16 = (audio_array * 32767).astype(np.int16)
        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())

        kwargs = {"beam_size": 3}
        if language:
            kwargs["language"] = language

        segments, info = model.transcribe(tmp_path, **kwargs)
        text = " ".join(seg.text.strip() for seg in segments).strip()
        detected_lang = info.language
        return text, None, detected_lang
    finally:
        os.unlink(tmp_path)


# ── Translation ────────────────────────────────────────────────────────────────
def translate(text, source_lang, target_lang, llm_module):
    """
    Translate text using Ollama/Groq.
    source_lang / target_lang: "English" or "German"
    """
    if not text.strip():
        return ""

    system = "You are a precise translator. Reply with ONLY the translation, nothing else. No explanations, no notes."
    prompt = f"Translate this {source_lang} text to {target_lang}:\n\n{text}"
    msgs   = [{"role": "user", "content": prompt}]

    result = llm_module.chat(msgs, system=system)
    # Strip any accidental preamble like "Translation:" or "German:"
    for prefix in ["Translation:", "German:", "English:", "Übersetzung:"]:
        if result.startswith(prefix):
            result = result[len(prefix):].strip()
    return result.strip()


# ── Text-to-speech ────────────────────────────────────────────────────────────
def speak(text, lang="de"):
    """
    Convert text to speech and play it.
    lang: "de" for German, "en" for English
    Returns audio bytes (MP3) for Streamlit playback.
    """
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read(), None
    except Exception as e:
        return None, str(e)


# ── Convenience: full pipeline ────────────────────────────────────────────────
def translate_speech(
    audio_array,
    sample_rate,
    direction,        # "en→de" or "de→en"
    llm_module,
    auto_detect=False
):
    """
    Full pipeline: audio → text → translation → TTS audio bytes.
    Returns dict with all intermediate results.
    """
    # 1. Transcribe
    src_lang = None if auto_detect else ("en" if direction == "en→de" else "de")
    original_text, err, detected = transcribe(audio_array, sample_rate, language=src_lang)

    if err:
        return {"error": err}
    if not original_text:
        return {"error": "No speech detected. Try speaking louder or closer to the mic."}

    # 2. Translate
    if direction == "en→de":
        translated = translate(original_text, "English", "German", llm_module)
        tts_lang   = "de"
    else:
        translated = translate(original_text, "German", "English", llm_module)
        tts_lang   = "en"

    # 3. TTS
    audio_bytes, tts_err = speak(translated, lang=tts_lang)

    return {
        "original":    original_text,
        "translated":  translated,
        "direction":   direction,
        "detected_lang": detected,
        "audio_bytes": audio_bytes,
        "tts_error":   tts_err,
        "error":       None,
    }
