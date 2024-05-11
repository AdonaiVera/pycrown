# Import necessary libraries and modules
import threading
import time
import os
from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
from modules.text_generation import DynamicTextGenerator

# Check if the dashing library is installed and handle the ImportError
try:
    from dashing import HSplit, VSplit, HGauge, VGauge, HBrailleChart, Log
except ImportError:
    print("The dashing module is not installed. Please install it using:")
    print("pip install dashing")
    exit(1)

# UI field paths for displaying brainwave band powers
FIELD_PATHS = {
    "alpha": (0, 1, 0),
    "beta": (0, 1, 1),
    "delta": (0, 1, 2),
    "gamma": (0, 1, 3),
    "theta": (0, 1, 4)
}

# Class definition for NeurosityReader to handle Neurosity SDK interactions
class NeurosityReader:
    def __init__(self):
        # Initialize Neurosity SDK with configuration details
        self.neurosity = NeurositySDK({"device_id": NEUROSITY_DEVICE_ID})
        self.neurosity.login({"email": NEUROSITY_EMAIL, "password": NEUROSITY_PASSWORD})
        self.running = True

        # Initialize text generator and threading lock for text generation
        self.text_generator = DynamicTextGenerator()
        self.text_generation_lock = threading.Lock()
        self.threshold = 0.8  # Threshold value for calm detection

        # UI setup and initial greeting
        self.setup_ui()
        self.split_and_append("Hola, soy ALE, tu guía espiritual en este viaje de meditación. ¿Cómo te sientes hoy y qué tipo de meditación te gustaría hacer?")

    def split_and_append(self, text):
        # Split text into chunks and append to the log UI
        words = text.split()
        for i in range(0, len(words), 12):  # Break text into chunks of 12 words
            chunk = ' '.join(words[i:i+12])
            self.ui.items[0].items[0].items[0].append(chunk)
        self.ui.items[0].items[0].items[0].append("")

    def setup_ui(self):
        """Set up the user interface using dashing widgets."""
        self.ui = HSplit(
            VSplit(
                HSplit(
                    Log(title='ALE', border_color=2, color=4),
                    VGauge(val=5, title="Meditation", border_color=2, color=3),
                ),
                HSplit(
                    VGauge(val=0, title="Alpha", border_color=2, color=1),
                    VGauge(val=0, title="Beta", border_color=2, color=2),
                    VGauge(val=0, title="Delta", border_color=2, color=3),
                    VGauge(val=0, title="Gamma", border_color=2, color=4),
                    VGauge(val=0, title="Theta", border_color=2, color=5),
                )
            )
        )

    def callback_brainwaves_power_by_band(self, data):
        """Update UI gauges based on brainwave band powers."""
        for band, values in data['data'].items():
            average_power = round(sum(values) / len(values), 2)
            path = FIELD_PATHS[band]
            self.ui.items[path[0]].items[path[1]].items[path[2]].value = average_power

    def callback_brainwaves_raw(self, data):
        """Handle raw brainwaves data callback."""
        for channel_index, channel in enumerate(data['data']):
            self.ui.items[1].items[channel_index].append(round(sum(channel) / len(channel), 2))

    def callback(self, data):
        """Handle callback from calm detection and generate text accordingly."""
        prediction_calm = int(data["probability"] * 100)
        self.ui.items[0].items[0].items[1].value = prediction_calm
        if not self.text_generation_lock.locked():
            threading.Thread(target=self.generate_text, args=(prediction_calm,)).start()

    def generate_text(self, prediction_calm):
        """Generate dynamic text based on the calm level and update the UI."""
        if self.text_generation_lock.acquire(blocking=False):
            try:
                text = self.text_generator.generate_dynamic_text(prediction_calm)
                self.split_and_append(text)
                self.text_generator.play_dynamic_text(text)
            finally:
                self.text_generation_lock.release()

    def read_brainwaves(self):
        """Read brainwaves and display them on the UI."""
        self.neurosity.calm(self.callback)
        self.neurosity.brainwaves_power_by_band(self.callback_brainwaves_power_by_band)
        try:
            while self.running:
                time.sleep(1)  # Sleep to reduce CPU usage
                self.ui.display()
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down.")
        finally:
            print("Cleaning up resources.")

    def start(self):
        """Start the brainwave reading thread."""
        self.thread = threading.Thread(target=self.read_brainwaves)
        self.thread.start()

    def stop(self):
        """Stop the brainwave reading thread and clean up resources."""
        self.running = False
        self.thread.join()

