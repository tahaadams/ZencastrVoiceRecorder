from io import BytesIO
from pathlib import Path
import wave
import av
import numpy as np
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from faster_whisper import WhisperModel
from .models import Recording


model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

def normalize_audio(audio_path):
    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    frames = [] 
    with av.open(audio_path, mode="r") as container:
        audio_stream = next((stream for stream in container.streams if stream.type == "audio"), None)
        if audio_stream is None:
            raise ValueError("The uploaded file contains no audio stream.")
        for frame in container.decode(audio_stream):
            frames.extend(resampler.resample(frame))
    frames.extend(resampler.resample(None))
    if not frames:
        raise ValueError("The uploaded recording contains no audio data.")

    pcm = np.concatenate([frame.to_ndarray().reshape(-1) for frame in frames])
    wav_buffer = BytesIO()
    with wave.open(wav_buffer, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(16000)
        output.writeframes(pcm.tobytes())
    return pcm.astype(np.float32) / 32768.0, wav_buffer.getvalue()


def home(request):
    if request.method == "POST":
        audio_file = request.FILES["audio"]
        rec = Recording.objects.create(title=audio_file.name, audio_file=audio_file)
        audio_samples, wav_data = normalize_audio(rec.audio_file.path)
        segments, _ = model.transcribe(audio_samples)
        rec.transcript = " ".join(s.text.strip() for s in segments)
        wav_name = f"{Path(audio_file.name).stem}.wav"
        rec.audio_file.delete(save=False)
        rec.audio_file.save(wav_name, ContentFile(wav_data), save=False)
        rec.save()
        return HttpResponse()
    return render(request, "home.html", {"recordings": Recording.objects.order_by("created_at")})