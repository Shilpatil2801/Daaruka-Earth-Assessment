import re


def understand_query(query):

    query_lower = query.lower()

    metrics = []

    # Soil
    if any(word in query_lower for word in [
        "soil",
        "soil health",
        "organic carbon",
        "carbon",
        "fertility"
    ]):
        metrics.append("soil")

    # Water
    if any(word in query_lower for word in [
        "water",
        "moisture",
        "rainfall",
        "drought",
        "irrigation"
    ]):
        metrics.append("water")

    # Biodiversity
    if any(word in query_lower for word in [
        "biodiversity",
        "species",
        "habitat",
        "wildlife",
        "ecosystem"
    ]):
        metrics.append("biodiversity")

    # Land use
    if any(word in query_lower for word in [
        "land use",
        "monoculture",
        "cropping",
        "agriculture",
        "agroforestry",
        "intercropping"
    ]):
        metrics.append("land_use")

    # Pollution
    if any(word in query_lower for word in [
        "pollution",
        "pollutant",
        "pesticide",
        "chemical",
        "waste"
    ]):
        metrics.append("pollution")

    # Climate
    if any(word in query_lower for word in [
        "climate",
        "temperature",
        "warming",
        "heat"
    ]):
        metrics.append("climate")

    metrics = list(dict.fromkeys(metrics))

    # If the query is broad, analyze biodiversity/environment
    if not metrics:
        metrics = [
            "soil",
            "water",
            "biodiversity",
            "land_use"
        ]

    return {
        "original_query": query,
        "detected_metrics": metrics
    }


if __name__ == "__main__":

    test_queries = [
        "How can I improve biodiversity?",
        "How can I improve soil moisture?",
        "What can I do about soil organic carbon?",
        "How does land use affect wildlife?"
    ]

    for query in test_queries:

        print("\nQUERY:")
        print(query)

        print("UNDERSTANDING:")
        print(understand_query(query))