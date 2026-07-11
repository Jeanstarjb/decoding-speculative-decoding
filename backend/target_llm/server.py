from fastapi import FastAPI

app = FastAPI()

@app.get("/verify")
def verify_token():
    return {"message": "Target LLM verification endpoint"}