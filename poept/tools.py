import time
import speech_recognition as sr


def speech(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    prompt = recognizer.recognize_google(audio)
    return prompt

def record(timeout, fs, micindex, file, chunk):
    r = sr.Recognizer()
    mic = sr.Microphone(
        device_index=micindex, 
        sample_rate=fs, 
        chunk_size=chunk
    )
    with mic as source:
        audio = r.listen(source, timeout=timeout, phrase_time_limit=timeout)
    with open(file, "wb") as f:
        f.write(audio.get_wav_data())
    return file
