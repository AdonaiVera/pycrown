import threading
import time
from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
import os
from modules.text_generation import DynamicTextGenerator

class NeurosityReader:
    def __init__(self):
        self.neurosity = NeurositySDK({
            "device_id": NEUROSITY_DEVICE_ID
        })
        self.neurosity.login({
            "email": NEUROSITY_EMAIL,
            "password": NEUROSITY_PASSWORD
        })
        self.running = True

        self.text_generator = DynamicTextGenerator()
        self.threshold = 0.8


    def callback(self, data):
        prediction_calm = int(data["probability"] * 100)
        self.text_generator.generate_dynamic_text(prediction_calm)

    def read_brainwaves(self):
        #unsubscribe = self.neurosity.kinesis_predictions("push", self.callback)
        unsubscribe = self.neurosity.calm(self.callback)
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