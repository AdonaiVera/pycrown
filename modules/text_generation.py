import openai
from config import OPENAI_API_KEY
from modules.speech_to_text_stream import SpeechToText
from modules.text_to_speech_stream import ElevenLabsTextToSpeech

class DynamicTextGenerator:
    def __init__(self):
        # Set API key for OpenAI
        self.client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.is_first_interaction = True
        self.session_history = []
        self.speech_text = SpeechToText()
        self.previous_relaxation = 0
        self.text_speech = ElevenLabsTextToSpeech()

    def construct_prompt(self, context):
        # Include recent interactions to maintain context and avoid repetition.
        history_snippet = " ".join(self.session_history[-5:])  # Last 5 interactions to maintain relevance without overload.
        return f"{history_snippet} {context} Por favor, continúa con algo nuevo y relevante."
    
    def initial_interaction(self):
        self.text_speech.text_to_speech_stream("Hola, soy ALE, tu guía espiritual en este viaje de meditación. ¿Cómo te sientes hoy y qué tipo de meditación te gustaría hacer?")
        user_response = self.speech_text.listen()  
        self.is_first_interaction = False
        return user_response

    def get_feedback(self, current_relaxation):
        if current_relaxation < self.previous_relaxation:
            return "Parece que estás menos relajado que antes. Vamos a encontrar maneras de mejorar eso."
        elif current_relaxation > self.previous_relaxation:
            return "Tu relajación ha mejorado desde la última vez. Eso es excelente."
        else:
            return "Tu nivel de relajación se mantiene estable, lo cual es bueno."

    def get_suggestion(self, relaxation_level):
        # Dynamic suggestions based on the relaxation level
        if relaxation_level < 20:
            return "Sugiero que hagamos algunas respiraciones profundas para ayudarte a relajarte."
        elif relaxation_level < 40:
            return "Sería bueno realizar algunos estiramientos suaves ahora."
        elif relaxation_level < 60:
            return "Intenta cerrar los ojos y visualizar un lugar tranquilo."
        elif relaxation_level < 80:
            return "Mantén tu respiración regular y enfócate en la suavidad del aire."
        else:
            return "Continúa disfrutando de este estado de profunda relajación."

    def generate_dynamic_text(self, prediction_calm):
        if self.is_first_interaction:

            introduction = f"Hola, soy ALE, tu guía espiritual. Me has dicho esto: {self.initial_interaction()}. Vamos a preparar una meditación personalizada para ti."
        else:
            # Generar el texto de acuerdo al estado de ánimo y nivel de relajación
             introduction = "Gracias por continuar esta sesión de meditación. Vamos a ajustar la práctica según cómo te sientes ahora."

        # Analyze relaxation change and generate feedback and suggestions
        feedback = self.get_feedback(prediction_calm)
        suggestion = self.get_suggestion(prediction_calm)
        self.previous_relaxation = prediction_calm

        context = f"{introduction} {feedback} {suggestion}"

        # Inform GPT-4 of the session history to maintain context awareness and prevent repetition.
        prompt = self.construct_prompt(context)

        # Invocar el modelo para continuar la conversación, simulando diálogo
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=100,
                temperature=0.5,
                stop=None,
            )

            self.session_history.append(response.choices[0].message.content)

            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed to generate text: {e}")
            return ""

    def play_dynamic_text(self, text):
        self.text_speech.text_to_speech_stream(text)
