import openai
from config import OPENAI_API_KEY

class DynamicTextGenerator:
    def __init__(self):
        # Set API key for OpenAI
        self.client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def generate_dynamic_text(self, actions, context_embedding):
        # Constructing a context-rich prompt
        context = f"{context_embedding}, si tu fueras una persona y tuvieras que decir que quieres hacer esa acción como lo harias: {', '.join(actions)}?"
        try:
            # Direct API call to generate text with contextual setup
            response = self.client.chat.completions.create(
                model="gpt-4",  
                messages=[
                    {
                        "role": "user",
                        "content": context,
                    }
                ],
                max_tokens=150,
                temperature=0.5,
                stop=None,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Failed to generate text: {e}")
            return None