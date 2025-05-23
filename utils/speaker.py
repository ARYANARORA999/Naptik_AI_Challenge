import edge_tts
import asyncio
import soundfile as sf
import sounddevice as sd

async def speak_async(text, output_file="response.wav"):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(output_file)
    data, samplerate = sf.read(output_file)
    sd.play(data, samplerate)
    sd.wait()

def speak_text(text, output_file="response.wav"):
    asyncio.run(speak_async(text, output_file))
