from fastapi import FastAPI
from pydantic import BaseModel

from App.recommendation import (
    generate_recommendations,
    filter_recommendations
)

from App.query import understand_query
from App.reasoning import analyze_environment
from App.environment import get_region_data


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

    # 1. Understand the query
    query_analysis = understand_query(request.query)

    # 2. Generate recommendations
    result = generate_recommendations(request.region)

    if "error" in result:
        return result

    # 3. Analyze environmental conditions
    environment_analysis = analyze_environment(
        request.region
    )

    # 4. Get structured environmental data
    environment = get_region_data(
        request.region
    )

    # 5. Filter recommendations based on query
    filtered_recommendations = filter_recommendations(
        result["recommendations"],
        query_analysis["detected_metrics"]
    )

    return {
        "region": request.region,
        "query": request.query,
        "detected_metrics": query_analysis["detected_metrics"],
        "environment": environment,
        "reasoning": environment_analysis,
        "recommendations": filtered_recommendations
    }