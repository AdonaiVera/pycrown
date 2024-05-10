# You need to install the python dashing if you want to run this code
try:
    from dashing import HSplit, VSplit, HGauge, VGauge, HBrailleChart, Log
except ImportError:
    print("The dashing module is not installed. Please install it using:")
    print("pip install dashing")
    exit(1)  # Exit the script if dashing is not installed

import threading
import time
from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
import os
from modules.text_generation import DynamicTextGenerator

# UI field paths for displaying brainwave band powers
FIELD_PATHS = {
    "alpha": (0, 1, 0),
    "beta": (0, 1, 1),
    "delta": (0, 1, 2),
    "gamma": (0, 1, 3),
    "theta": (0, 1, 4)
}

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
        self.text_generation_lock = threading.Lock()
        self.threshold = 0.8

        self.setup_ui()
        self.split_and_append("Hola, soy ALE, tu guía espiritual en este viaje de meditación. ¿Cómo te sientes hoy y qué tipo de meditación te gustaría hacer?")

    def split_and_append(self, text):
        words = text.split()
        # Group every 6 words together
        chunks = [' '.join(words[i:i+6]) for i in range(0, len(words),6)]
        
        # Append each chunk to the UI element
        for chunk in chunks:
            self.ui.items[0].items[0].items[0].append(chunk)
        
        self.ui.items[0].items[0].items[0].append("")
        self.ui.items[0].items[0].items[0].append("...")
        self.ui.items[0].items[0].items[0].append("")


    def setup_ui(self):
        """Set up the user interface."""
        self.ui = HSplit(
            VSplit(
                HSplit(
                    Log(title='ALE', border_color=2, color= 4),
                    VGauge(val=5, title="Meditation", border_color=2, color=3),
                ),
                HSplit(
                    VGauge(val=0, title="Alpha", border_color=2, color=1),
                    VGauge(val=0, title="Beta", border_color=2, color=2),
                    VGauge(val=0, title="Delta", border_color=2, color=3),
                    VGauge(val=0, title="Gamma", border_color=2, color=4),
                    VGauge(val=0, title="Theta", border_color=2, color=5),
                )  
            ),
            VSplit(
                HBrailleChart(border_color=2, color=1, title="CP6"),
                HBrailleChart(border_color=2, color=2, title="F6"),
                HBrailleChart(border_color=2, color=3, title="C4"),
                HBrailleChart(border_color=2, color=4, title="CP4"),
                HBrailleChart(border_color=2, color=5, title="CP3"),
                HBrailleChart(border_color=2, color=6, title="F5"),
                HBrailleChart(border_color=2, color=7, title="C3"),
                HBrailleChart(border_color=2, color=7, title="CP5"),
            ),
        )

    def callback_brainwaves_power_by_band(self, data):
        """Handle brainwaves power by band data callback."""
        for band, values in data['data'].items():
            average_power = round(sum(values) / len(values))
            path = FIELD_PATHS[band]
            self.ui.items[path[0]].items[path[1]].items[path[2]].value = average_power

    def callback_brainwaves_raw(self, data):
        """Handle raw brainwaves data callback."""
        for channel_index, channel in enumerate(data['data']):
            self.ui.items[1].items[channel_index].append(round(sum(channel) / len(channel)))

    def callback(self, data):
        prediction_calm = int(data["probability"] * 100)
        self.ui.items[0].items[0].items[1].value = prediction_calm
        if not self.text_generation_lock.locked():
            threading.Thread(target=self.generate_text, args=(prediction_calm,)).start()

    def generate_text(self, prediction_calm):
        if self.text_generation_lock.acquire(blocking=False):
            try:
                text = self.text_generator.generate_dynamic_text(prediction_calm)
                self.split_and_append(text)
                self.text_generator.play_dynamic_text(text)
            finally:
                self.text_generation_lock.release()

    def read_brainwaves(self):
        self.neurosity.calm(self.callback)
        self.neurosity.brainwaves_power_by_band(self.callback_brainwaves_power_by_band)
        self.neurosity.brainwaves_raw(self.callback_brainwaves_raw)

        try:
            while self.running:
                time.sleep(1)  
                self.ui.display()
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down.")
        finally:
            print("Cleaning up resources.")
    
    def start(self):
        self.thread = threading.Thread(target=self.read_brainwaves)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()