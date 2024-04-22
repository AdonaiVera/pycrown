import threading
import time
from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
import os
from modules.text_generation import DynamicTextGenerator

class NeurosityReader:
    def __init__(self, env_file="my.env"):
        self.neurosity = NeurositySDK({
            "device_id": NEUROSITY_DEVICE_ID
        })
        self.neurosity.login({
            "email": NEUROSITY_EMAIL,
            "password": NEUROSITY_PASSWORD
        })
        self.running = True

        self.text_generator = DynamicTextGenerator()

    def callback(self, data):
        actions = ['Sleep']  # Example actions derived from data
        speaker_info = "Habla con una voz tranquila y segura"
        text = self.text_generator.generate_dynamic_text(actions, speaker_info)

        print(text)
        
        time.sleep(20)
        '''
        
        # Analyze data and determine if text generation is needed
        if data['probability'] > threshold:
            actions = ['Eat', 'Sleep']  # Example actions derived from data
            speaker_info = "Adonai, with a confident and calm voice"
            text = generate_dynamic_text(actions, speaker_info)
            if text is not None:
                print(text)
        '''

    def read_brainwaves(self):
        unsubscribe = self.neurosity.brainwaves_raw(self.callback)
        try:
            while self.running:
                time.sleep(1)  # Sleep to prevent this loop from consuming too much CPU
        finally:
            unsubscribe()

    def start(self):
        self.thread = threading.Thread(target=self.read_brainwaves)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()