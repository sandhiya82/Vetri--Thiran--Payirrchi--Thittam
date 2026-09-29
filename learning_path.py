import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for the topic below.

Topic:
{topic}

Requirements:
1. Start from beginner level.
2. Continue to intermediate level.
3. Finish with advanced level.
4. Give topics in step-by-step order.
5. Suggest useful learning resources such as videos,
   articles, or books.
6. Use simple language.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"