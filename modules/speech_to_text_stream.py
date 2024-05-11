import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        """Initializes the recognizer object from the speech_recognition library."""
        self.recognizer = sr.Recognizer()

    def listen(self):
        """Captures speech from the microphone and returns its text representation."""
        with sr.Microphone() as source:
            # Adjust the recognizer sensitivity to ambient noise to improve accuracy.
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                print("Listening...")
                # Listen to the source with a timeout and a phrase time limit
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                # Handle cases where no speech is detected within the timeout limit.
                print("Listening timed out while waiting for phrase to start")
                return ""

        # After capturing the audio, attempt to recognize it
        return self.recognize(audio)

    def recognize(self, audio):
        """Attempts to recognize speech using Google's Web Speech API and returns the text."""
        try:
            # Call Google's Web Speech API to convert speech to text in Spanish
            text = self.recognizer.recognize_google(audio, language='es-ES')
            return text
        except sr.UnknownValueError:
            # Handle the exception for unintelligible speech
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            # Handle exceptions related to API requests like network errors, or API limits
            print(f"API request failed; {e}")
            return None
