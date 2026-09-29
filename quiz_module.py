import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_quiz(text: str):
    prompt = f"""
Create 3 multiple-choice questions from the following text.

Rules:
- Each question must have 4 options.
- Give the correct answer.
- Return ONLY valid JSON.
- Use this format:

[
  {{
    "question": "Question 1",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Text:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text.strip()

        # Remove markdown code block if Gemini adds it
        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        return json.loads(result)

    except Exception as e:
        return {"error": str(e)}