import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        # Initialize the recognizer object from the speech_recognition library.
        self.recognizer = sr.Recognizer()

    def listen(self):
        # This method uses the microphone to capture speech.
        with sr.Microphone() as source:
            # Adjusts the recognizer sensitivity to ambient noise for 1 second.
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("No speech detected within the allowed time.")
                return None

        return self.recognize(audio)

    def recognize(self, audio):
        # Attempts to recognize speech using Google's Web Speech API and converts it into text.
        try:
            text = self.recognizer.recognize_google(audio, language='es-ES')
            return text
        except sr.UnknownValueError:
            # This exception is raised when the speech is unintelligible.
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            # This exception is raised when there are issues with the Google API, such as connectivity problems,
            # or reaching API limits.
            print(f"API request failed; {e}")
            return None