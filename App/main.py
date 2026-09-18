from fastapi import FastAPI
from pydantic import BaseModel

from App.recommendation import generate_recommendations


app = FastAPI(
    title="Daaruka.Earth Biodiversity Intelligence API",
    description="AI-powered environmental reasoning and evidence retrieval system",
    version="1.0.0"
)


class AnalysisRequest(BaseModel):
    region: str
    query: str


@app.get("/")
def root():
    return {
        "message": "Daaruka.Earth Biodiversity Intelligence API",
        "status": "running"
    }


@app.post("/analyze")
def analyze(request: AnalysisRequest):

    result = generate_recommendations(request.region)

    if "error" in result:
        return result

    return {
        "region": request.region,
        "query": request.query,
        "recommendations": result["recommendations"]
    }