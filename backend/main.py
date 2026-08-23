from fastapi import FastAPI

app = FastAPI(title="MatchCrewAI API")

@app.get("/")
def read_root():
    return {"message": "MatchCrewAI backend is running"}