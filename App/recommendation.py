from App.reasoning import analyze_environment
from App.evidence import get_evidence


def generate_recommendations(region):

    analysis = analyze_environment(region)

    if "error" in analysis:
        return analysis

    environment = analysis["environment"]
    recommendations = []

    # ---------------------------------------------------------
    # 1. SOIL ORGANIC CARBON
    # ---------------------------------------------------------
    if environment["organic_carbon"] < 0.5:

        recommendation = {
            "action": (
                "Introduce legume-based cover crops and increase "
                "organic matter inputs."
            ),
            "why": (
                "Low soil organic carbon can indicate pressure on soil "
                "health and biological activity. Increasing organic inputs "
                "can support soil biological activity and soil functions."
            ),
            "impacted_metrics": [
                "soil organic carbon",
                "soil health",
                "soil biological activity"
            ],
            "categories": ["soil"],
            "time_horizon": "6–24 months",
            "confidence": "High"
        }

        recommendation["evidence"] = get_evidence(
            recommendation,
            top_k=2
        )

        recommendations.append(recommendation)

    # ---------------------------------------------------------
    # 2. WATER AVAILABILITY
    # ---------------------------------------------------------
    if (
        environment["rainfall"] == "low"
        or environment["soil_moisture"] < 20
    ):

        recommendation = {
            "action": (
                "Use mulching and water-conserving land "
                "management practices."
            ),
            "why": (
                "Low rainfall and soil moisture increase water stress. "
                "Maintaining soil cover can help retain soil moisture "
                "and reduce pressure on vegetation."
            ),
            "impacted_metrics": [
                "soil moisture",
                "water availability",
                "vegetation resilience"
            ],
            "categories": ["water"],

            "time_horizon": "1–12 months",
            "confidence": "High"
        }

        recommendation["evidence"] = get_evidence(
            recommendation,
            top_k=2
        )

        recommendations.append(recommendation)

    # ---------------------------------------------------------
    # 3. MONOCULTURE / LAND USE
    # ---------------------------------------------------------
    if "monoculture" in environment["land_use"].lower():

        recommendation = {
            "action": (
                "Replace part of the monoculture area with "
                "intercropping, agroforestry or habitat strips."
            ),
            "why": (
                "Monoculture can provide relatively limited habitat "
                "structure. Diversifying land use can increase habitat "
                "variety and ecological niches."
            ),
            "impacted_metrics": [
                "habitat diversity",
                "species richness",
                "land-use diversity"
            ],
            "categories": ["biodiversity", "land_use"],
            "time_horizon": "1–3 years",
            "confidence": "High"
        }

        recommendation["evidence"] = get_evidence(
            recommendation,
            top_k=2
        )

        recommendations.append(recommendation)

    # ---------------------------------------------------------
    # 4. BIODIVERSITY
    # ---------------------------------------------------------
    if (
        environment["species_richness"] < 15
        or environment["habitat_diversity"] == "low"
    ):

        recommendation = {
            "action": (
                "Create or restore small habitat patches "
                "and vegetation corridors."
            ),
            "why": (
                "Low habitat diversity can restrict the number of "
                "ecological niches available to species. Increasing "
                "habitat variety can support a wider range of organisms."
            ),
            "impacted_metrics": [
                "species richness",
                "habitat diversity",
                "ecosystem resilience"
            ],
            "categories": ["biodiversity"],
            "time_horizon": "1–5 years",
            "confidence": "Medium"
        }

        recommendation["evidence"] = get_evidence(
            recommendation,
            top_k=2
        )

        recommendations.append(recommendation)

    # ---------------------------------------------------------
    # 5. MULTI-METRIC RECOMMENDATION
    # ---------------------------------------------------------
    if (
        environment["organic_carbon"] < 0.5
        and environment["rainfall"] == "low"
        and "monoculture" in environment["land_use"].lower()
    ):

        recommendation = {
            "action": (
                "Transition from monoculture toward diversified "
                "cropping with cover crops, mulching and habitat strips."
            ),
            "why": (
                "Multiple environmental pressures are occurring together: "
                "low soil organic carbon, limited water availability and "
                "low land-use diversity. A combined intervention can "
                "address soil health, moisture retention and habitat "
                "diversity simultaneously."
            ),
            "impacted_metrics": [
                "soil organic carbon",
                "soil moisture",
                "water availability",
                "habitat diversity",
                "species richness",
                "land-use diversity"
            ],
            "categories": ["soil", "water", "biodiversity", "land_use"],
            "time_horizon": "1–3 years",
            "confidence": "High"
        }

        recommendation["evidence"] = get_evidence(
            recommendation,
            top_k=3
        )

        recommendations.append(recommendation)

    return {
        "region": region,
        "recommendations": recommendations
    }


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    result = generate_recommendations("Pune")

    print()
    print("=" * 75)
    print("DARUKAA.EARTH — EVIDENCE-BACKED RECOMMENDATIONS")
    print("=" * 75)

    print(f"\nREGION: {result['region']}")

    for i, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):

        print(f"\n{'=' * 75}")
        print(f"RECOMMENDATION {i}")
        print(f"{'=' * 75}")

        print("\nACTION:")
        print(recommendation["action"])

        print("\nWHY:")
        print(recommendation["why"])

        print("\nIMPACTED METRICS:")

        for metric in recommendation["impacted_metrics"]:
            print(f"  - {metric}")

        print(f"\nTIME HORIZON: {recommendation['time_horizon']}")
        print(f"CONFIDENCE: {recommendation['confidence']}")

        print("\nSCIENTIFIC EVIDENCE:")

        for j, evidence in enumerate(
            recommendation["evidence"],
            start=1
        ):

            print(f"\n  Evidence {j}")
            print(f"  Source: {evidence['source']}")
            print(f"  Page: {evidence['page']}")
            print(f"  Distance: {evidence['relevance_distance']}")
            print(f"  {evidence['text'][:500]}...")

def filter_recommendations(recommendations, detected_metrics):

    # No detected topic → broad environmental response
    if not detected_metrics:
        return recommendations

    filtered = []

    for rec in recommendations:

        categories = set(
            rec.get("categories", [])
        )

        if categories.intersection(
            set(detected_metrics)
        ):
            filtered.append(rec)

    # If filtering somehow produces nothing,
    # retain the original recommendations.
    return filtered if filtered else recommendations