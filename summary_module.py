import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text.

Requirements:
- Keep the important points.
- Use simple language.
- Make it short and easy to revise.

Text:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"