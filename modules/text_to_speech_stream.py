import os
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY
import pygame

class ElevenLabsTextToSpeech:
    def __init__(self):
        """Initialize the ElevenLabs client with the provided API key."""
        self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    def text_to_speech_stream(self, text: str) -> BytesIO:
        """
        Converts text to speech using ElevenLabs' API and returns the audio data as a BytesIO stream.
        """
        # Convert text to speech with specific voice and settings
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

        # Initialize a BytesIO object to store the streamed audio data
        audio_stream = BytesIO()
        
        # Write audio data to the stream from the API response
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)
        
        # Rewind the stream to the beginning for playback
        audio_stream.seek(0)

        # Play the audio stream
        self.play_audio_stream(audio_stream)

        # Return the BytesIO stream containing the audio for potential further use
        return audio_stream
    
    def play_audio_stream(self, audio_stream: BytesIO):
        """
        Plays audio from a BytesIO stream using Pygame's mixer.
        """
        # Initialize Pygame's mixer
        pygame.mixer.init()

        # Load the audio data from the BytesIO stream into Pygame mixer
        audio_stream.seek(0)  # Ensure the stream starts at the beginning
        pygame.mixer.music.load(audio_stream)

        # Play the audio and wait for completion
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Wait for the audio to finish playing