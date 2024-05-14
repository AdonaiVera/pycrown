
from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD, ELEVENLABS_API_KEY
import os
import time
import pandas as pd

from modules.text_to_speech_stream import ElevenLabsTextToSpeech

# Initialize Neurosity SDK
neurosity = NeurositySDK({"device_id": NEUROSITY_DEVICE_ID})
neurosity.login({"email": NEUROSITY_EMAIL, "password": NEUROSITY_PASSWORD})


# Data collection function
def collect_brainwaves(duration: int, label: str):
    brainwave_data = []

    def callback(data):
        brainwave_data.append(data['data']['alpha'])

    unsubscribe = neurosity.brainwaves_power_by_band(callback)
    time.sleep(duration)
    unsubscribe()
    
    # Create DataFrame
    df = pd.DataFrame(brainwave_data, columns=['CP3', 'C3', 'F5', 'PO3', 'PO4', 'F6', 'C4', 'CP4'])
    df['label'] = label
    return df

# Main function to run the sessions
def run_sessions():
    tts = ElevenLabsTextToSpeech()

    # Training session
    tts.text_to_speech_stream("Hola Soy ALE. Por favor, relájate y piensa en cualquier cosa. Comenzaremos a recolectar datos en 15 segundos.")
    time.sleep(15)
    tts.text_to_speech_stream("Ahora comenzaremos a recolectar datos. Puedes seguir pensando en cualquier cosa.")
    training_data = collect_brainwaves(60, "training")
    tts.text_to_speech_stream("Gracias. Puedes detenerte ahora.")

    # Meditation session
    tts.text_to_speech_stream("Por favor, relájate e intenta meditar. Comenzaremos a recolectar datos en 15 segundos.")
    time.sleep(15)
    tts.text_to_speech_stream("Ahora comenzaremos a recolectar datos. Por favor, continúa meditando.")
    meditation_data = collect_brainwaves(60, "meditation")
    tts.text_to_speech_stream("Gracias. Puedes detenerte ahora.")


    # Combine and save data
    combined_data = pd.concat([training_data, meditation_data])
    combined_data.to_csv("data/brainwave_data_band.csv", index=False)

if __name__ == "__main__":
    run_sessions()
