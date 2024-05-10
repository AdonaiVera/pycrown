import os
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY
import pygame


class ElevenLabsTextToSpeech:
    def __init__(self):
        # Initialize the ElevenLabs client
        self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    def text_to_speech_stream(self, text: str) -> BytesIO:
        # Perform the text-to-speech conversion with specified voice and settings
        response = self.client.text_to_speech.convert(
            voice_id="TfizKtwJkGYwVpygTaPJ", 
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # Create a BytesIO object to hold the audio data in memory
        audio_stream = BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)

        self.play_audio_stream(audio_stream)

        # Return the stream for further use
        return audio_stream
    
    def play_audio_stream(self, audio_stream: BytesIO):
        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Load the audio from the BytesIO stream
        audio_stream.seek(0)  # Ensure the stream position is at the beginning
        pygame.mixer.music.load(audio_stream)

        # Play the audio
        pygame.mixer.music.play()

        # Wait until the audio playback is complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)