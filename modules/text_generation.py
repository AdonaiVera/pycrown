import openai
from config import OPENAI_API_KEY
from modules.speech_to_text_stream import SpeechToText
from modules.text_to_speech_stream import ElevenLabsTextToSpeech

class DynamicTextGenerator:
    def __init__(self):
        """Initialize components and set the OpenAI API key."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.is_first_interaction = True
        self.session_history = []
        self.speech_text = SpeechToText()
        self.previous_relaxation = 0
        self.text_speech = ElevenLabsTextToSpeech()

    def construct_prompt(self, context):
        """Constructs a prompt for the GPT model by appending recent interactions."""
        # Combine the last 5 interactions to maintain conversational context without overload.
        history_snippet = " ".join(self.session_history[-5:])
        return f"{history_snippet} {context} Por favor, continúa con algo nuevo y relevante."
    
    def initial_interaction(self):
        """Handles the initial user interaction, speaking a greeting and listening for a response."""
        self.text_speech.text_to_speech_stream("Hola, soy ALE, tu guía espiritual en este viaje de meditación. ¿Cómo te sientes hoy y qué tipo de meditación te gustaría hacer?")
        user_response = self.speech_text.listen()  
        self.is_first_interaction = False
        return user_response

    def get_feedback(self, current_relaxation):
        """Generates feedback based on the change in relaxation level."""
        if current_relaxation < self.previous_relaxation:
            return "Parece que estás menos relajado que antes. Vamos a encontrar maneras de mejorar eso."
        elif current_relaxation > self.previous_relaxation:
            return "Tu relajación ha mejorado desde la última vez. Eso es excelente."
        else:
            return "Tu nivel de relajación se mantiene estable, lo cual es bueno."

    def get_suggestion(self, relaxation_level):
        """Provides suggestions based on the current relaxation level."""
        suggestions = [
            (20, "Sugiero que hagamos algunas respiraciones profundas para ayudarte a relajarte."),
            (40, "Sería bueno realizar algunos estiramientos suaves ahora."),
            (60, "Intenta cerrar los ojos y visualizar un lugar tranquilo."),
            (80, "Mantén tu respiración regular y enfócate en la suavidad del aire."),
            (100, "Continúa disfrutando de este estado de profunda relajación.")
        ]
        for threshold, suggestion in suggestions:
            if relaxation_level < threshold:
                return suggestion

    def generate_dynamic_text(self, prediction_calm):
        """Generate and return dynamic text based on the user's relaxation level."""
        if self.is_first_interaction:
            introduction = f"Hola, soy ALE, tu guía espiritual. Me has dicho esto: {self.initial_interaction()}. Vamos a preparar una meditación personalizada para ti."
        else:
            introduction = "Gracias por continuar esta sesión de meditación. Vamos a ajustar la práctica según cómo te sientes ahora."

        feedback = self.get_feedback(prediction_calm)
        suggestion = self.get_suggestion(prediction_calm)
        self.previous_relaxation = prediction_calm
        context = f"{introduction} {feedback} {suggestion}"
        prompt = self.construct_prompt(context)

        # Invoke the model to continue the conversation
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5
            )
            self.session_history.append(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed to generate text: {e}")
            return ""

    def play_dynamic_text(self, text):
        """Play the generated text using text-to-speech."""
        self.text_speech.text_to_speech_stream(text)
