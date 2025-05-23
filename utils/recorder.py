import sounddevice as sd
import soundfile as sf

def record_audio(filename="input.wav", duration=5, samplerate=16000):
    print("🎤 Recording...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, audio, samplerate)
