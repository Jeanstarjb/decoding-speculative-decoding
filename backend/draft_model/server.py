from fastapi import FastAPI

app = FastAPI()

@app.get("/draft")
def generate_draft():
    return {"message": "Draft model inference endpoint"}