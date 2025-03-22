import logging
import math
import subprocess
from faster_whisper import WhisperModel
import whisper
from datetime import timedelta


def convert_mp3_to_wav(mp3_path):
    wav_path = mp3_path.replace(".mp3", ".wav")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", mp3_path, "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return wav_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {mp3_path} to WAV: {e.stderr.decode()}")
        return None


def transcribe_audio(audio):
    wav_audio = convert_mp3_to_wav(audio)
    if not wav_audio:
        logging.error(f"Failed to convert {audio} to WAV")
        return []

    model = WhisperModel("small")
    segments, info = model.transcribe(
        wav_audio,
        word_timestamps=True,
        vad_filter=False
    )

    all_segments = []
    for segment in segments:
        for word in segment.words:
            cleaned_word = word.word.replace(",", "").replace(".", "").upper()
            all_segments.append((word.start, word.end, cleaned_word))

    return all_segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    minutes = math.floor(seconds / 60) % 60
    secs = math.floor(seconds % 60)
    ms = round((seconds - math.floor(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

def generate_srt_file(segments, audio_path):
    srt_path = audio_path.replace(".mp3", ".srt")
    try:
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, (start, end, text) in enumerate(segments, 1):
                f.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")
        return srt_path
    except Exception as e:
        logging.error(f"Error generating SRT file for {audio_path}: {e}")
        return None


def extract_image_durations(mp3_path):
    # Load Whisper model (using 'small' for efficiency, can switch to 'medium' or 'large')
    model = whisper.load_model("small")

    # Transcribe audio
    result = model.transcribe(mp3_path)

    # Print transcription result for debugging
    print("Transcription result:")
    for segment in result["segments"]:
        start_time = timedelta(seconds=segment["start"])
        end_time = timedelta(seconds=segment["end"])
        text = segment["text"]
        print(f"Start: {start_time}, End: {end_time}, Text: {text}")

    # Get the total duration of the audio
    audio_end = timedelta(seconds=result["segments"][-1]["end"])

    # Find all "Step" timestamps dynamically
    step_starts = []
    for segment in result["segments"]:
        start_time = timedelta(seconds=segment["start"])
        text = segment["text"].strip()
        if "Step" in text:
            step_starts.append(start_time)

    # Since there are always at least 3 steps, take the first 3
    step_starts = step_starts[:3]  # Limit to Step 1, Step 2, Step 3

    # Determine the start of the final image (last segment)
    if len(result["segments"]) < 1:
        raise ValueError("Audio must have at least 1 segment.")
    final_image_start = timedelta(seconds=result["segments"][-1]["start"])  # Start of the last segment

    # Define timestamps for 5 images
    timestamps = [
        timedelta(seconds=0),       # Start of intro
        step_starts[0],             # Start of Step 1 (end of intro)
        step_starts[1],             # Start of Step 2
        step_starts[2],             # Start of Step 3
        final_image_start,          # End of Step 3, start of final image (last segment)
        audio_end                   # End of audio
    ]

    # Calculate durations for 5 images
    image_durations = []
    for i in range(len(timestamps) - 1):
        duration = (timestamps[i + 1] - timestamps[i]).total_seconds()
        image_durations.append(duration)

    return image_durations


