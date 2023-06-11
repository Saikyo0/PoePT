import speech_recognition as sr
import time


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

def find(driver, by, id):
    try:
        element = driver.find_element(by, id)
        return element
    except:
        return False

def click(driver, by, id):
    count = 0
    while count<5:
        count+=1
        try:
            button = find(driver, by, id)
            button.click()
            return button
        except:
            time.sleep(0.1)
    print(f"Unable to click {id}")
    return False

def enter(driver, by, id, data):
    count = 0
    while count<5:
        count+=1
        try:
            area = find(driver, by, id)
            area.send_keys(data)
            return area
        except:
            time.sleep(0.1)
    print(f"Unable to input value to {id}")
    return False
