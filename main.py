import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google import genai

load_dotenv()

app = FastAPI(title="EduGenie - AI Learning Assistant")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def generate_ai_response(task: str, user_input: str):

    client = get_gemini_client()

    if client is None:
        return "Gemini API key not found. Please add GEMINI_API_KEY in the .env file."

    if task == "qa":

        prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.
Use simple language and give an example when useful.

Student Question:
{user_input}
"""

    elif task == "explain":

        prompt = f"""
You are EduGenie, an educational assistant.

Explain the following topic in very simple language.

Include:
1. Simple definition
2. Important points
3. One simple example

Topic:
{user_input}
"""

    elif task == "quiz":

        prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions about the following topic.

For every question provide:
- Question
- Option A
- Option B
- Option C
- Option D
- Correct Answer

Topic:
{user_input}
"""

    elif task == "summary":

        prompt = f"""
You are EduGenie, an educational assistant.

Summarize the following text in simple language.
Keep the important information.
Use clear bullet points.

Text:
{user_input}
"""

    elif task == "learn":

        prompt = f"""
You are EduGenie, an educational learning-path assistant.

Create a structured learning path for the following topic.

Include:
1. Beginner level
2. Intermediate level
3. Advanced level
4. Important topics to learn
5. Suggested practice
6. Useful learning resources

Topic:
{user_input}
"""

    else:

        prompt = f"""
You are EduGenie, an educational assistant.

Help the student with the following request:

{user_input}
"""

    # Gemini API call with retry
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model ="gemini-3.7-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message and attempt < 2:

                time.sleep(5 * (attempt + 1))
                continue

            return f"Gemini API Error: {error_message}"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None
        }
    )


@app.post("/", response_class=HTMLResponse)
async def process_request(
    request: Request,
    task: str = Form(...),
    user_input: str = Form(...)
):

    result = generate_ai_response(task, user_input)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result
        }
    )


@app.post("/qa", response_class=HTMLResponse)
async def qa_endpoint(
    request: Request,
    question: str = Form(default=""),
    user_input: str = Form(default="")
):

    text = question.strip() or user_input.strip()

    if not text:
        result = "Please enter a question."

    else:
        result = generate_ai_response("qa", text)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result
        }
    )


@app.post("/explain")
async def explain_endpoint(topic: str = Form(...)):

    result = generate_ai_response("explain", topic)

    return {"result": result}


@app.post("/quiz")
async def quiz_endpoint(topic: str = Form(...)):

    result = generate_ai_response("quiz", topic)

    return {"result": result}


@app.post("/summarize")
async def summarize_endpoint(text: str = Form(...)):

    result = generate_ai_response("summary", text)

    return {"result": result}


@app.post("/learn/recommendations")
async def learning_endpoint(topic: str = Form(...)):

    result = generate_ai_response("learn", topic)

    return {"result": result}