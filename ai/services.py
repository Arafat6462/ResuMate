import os
from google import genai
from openai import OpenAI
from .models import AIModel

def generate_resume_content(model_instance: AIModel, user_input: str) -> str:
    """
    Selects the correct AI provider and generates resume content.
    """
    api_key = os.environ.get(model_instance.api_key_name)
    if not api_key or api_key.startswith('placeholder'):
        raise ValueError(f"API key '{model_instance.api_key_name}' is not configured in the environment.")

    prompt = f"Based on the following text, create a professional resume in Markdown format:\n\n---\n\n{user_input}"

    try:
        if model_instance.api_provider == 'google_gemini':
            # Direct implementation based on user's working code
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_instance.model_name, contents=prompt
                )
            return response.text

        elif model_instance.api_provider == 'open_router':
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            completion = client.chat.completions.create(
                model=model_instance.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return completion.choices[0].message.content
        
        else:
            raise NotImplementedError(f"The API provider '{model_instance.api_provider}' is not supported.")

    except Exception as e:
        # Log the specific error for debugging
        print(f"AI_SERVICE_ERROR: Failed to call {model_instance.display_name}. Error: {e}")
        # Raise a generic error to the view
        raise Exception("An error occurred while communicating with the AI service.")
