import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_topic(topic):
    prompt = f"""
    Explain the following topic in very simple language.
    Give a short definition, important points and one simple example.

    Topic: {topic}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text