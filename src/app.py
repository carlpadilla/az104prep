import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Mount the static directory (located at src/static)
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Set up the templates directory (located at src/templates)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Load quiz questions from questions.json located in the project root.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
questions_file = os.path.join(base_dir, "questions.json")
with open(questions_file, "r") as f:
    questions = json.load(f)

class AnswerRequest(BaseModel):
    question_index: int
    answer: str

@app.get("/", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/question/{question_index}")
async def get_question(question_index: int):
    if 0 <= question_index < len(questions):
        return {"question": questions[question_index]["question"]}
    raise HTTPException(status_code=404, detail="No more questions")

@app.post("/check_answer")
async def check_answer(request_data: AnswerRequest):
    if 0 <= request_data.question_index < len(questions):
        correct_answer = questions[request_data.question_index]["answer"].strip().lower()
        is_correct = request_data.answer.strip().lower() == correct_answer
        return {"correct": is_correct}
    raise HTTPException(status_code=400, detail="Invalid question index")
