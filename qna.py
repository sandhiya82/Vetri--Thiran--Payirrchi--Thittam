from dotenv import load_dotenv
load_dotenv()
import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, an educational learning assistant.

Answer the student's question clearly and simply.
Use easy language and give a useful explanation.

Student question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"