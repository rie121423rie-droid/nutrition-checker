from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import openai
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("backend/foods_data.json", "r", encoding="utf-8") as f:
    FOODS_DATA = json.load(f)

class InputData(BaseModel):
    age: int
    gender: str
    activity_level: str
    intake: dict

ENERGY_TABLE = {
    "male": {"low": "2300kcal_50g", "medium": "2700kcal_57.5g", "high": "3100kcal_65g"},
    "female": {"low": "2000kcal_45g", "medium": "2300kcal_50g", "high": "2600kcal_55g"},
}

@app.post("/api/calc")
def calculate_balance(data: InputData):
    key = ENERGY_TABLE[data.gender][data.activity_level]
    target = FOODS_DATA[key]
    result = {}
    for food, goal in target.items():
        eaten = data.intake.get(food, 0)
        percent = round(eaten / goal * 100, 1) if goal else 0
        result[food] = {"摂取量": eaten, "目標量": goal, "達成率": percent}
    return {"target": key, "result": result}

@app.post("/api/comment")
def comment(data: dict):
    try:
        prompt = f"以下の食品群の達成率に基づいて、1日の栄養バランスコメントを80文字以内で日本語で書いてください。\n{data}"
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"comment": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
