from App.environment import get_region_data
from App.retrieval import retrieve_documents


# ============================================================
# ENVIRONMENTAL REASONING ENGINE
# ============================================================

def analyze_environment(region):

    environment = get_region_data(region)

    if environment is None:
        return {
            "error": f"No environmental data found for {region}"
        }

    factors = []
    relationships = []
    candidate_actions = []

    # --------------------------------------------------------
    # 1. SOIL HEALTH
    # --------------------------------------------------------

    organic_carbon = environment["organic_carbon"]

    if organic_carbon < 0.5:

        factors.append({
            "variable": "soil_organic_carbon",
            "value": organic_carbon,
            "status": "low"
        })

        relationships.append(
            "Low soil organic carbon may indicate "
            "pressure on soil health and biological activity."
        )

        candidate_actions.extend([
            "legume-based cover crops",
            "crop diversification",
            "organic matter management"
        ])


    # --------------------------------------------------------
    # 2. WATER AVAILABILITY
    # --------------------------------------------------------

    rainfall = environment["rainfall"]
    soil_moisture = environment["soil_moisture"]

    if rainfall == "low" or soil_moisture < 20:

        factors.append({
            "variable": "water_availability",
            "value": {
                "rainfall": rainfall,
                "soil_moisture": soil_moisture
            },
            "status": "constrained"
        })

        relationships.append(
            "Low rainfall and low soil moisture can "
            "increase water stress for vegetation and "
            "ecosystem organisms."
        )

        candidate_actions.extend([
            "water-conserving land management",
            "drought-tolerant crop diversification",
            "mulching"
        ])


    # --------------------------------------------------------
    # 3. LAND USE
    # --------------------------------------------------------

    land_use = environment["land_use"]

    if "monoculture" in land_use.lower():

        factors.append({
            "variable": "land_use",
            "value": land_use,
            "status": "low_diversity"
        })

        relationships.append(
            "Monoculture can provide less habitat "
            "diversity than diversified land-use systems."
        )

        candidate_actions.extend([
            "intercropping",
            "agroforestry",
            "habitat strips"
        ])


    # --------------------------------------------------------
    # 4. BIODIVERSITY
    # --------------------------------------------------------

    species_richness = environment[
        "species_richness"
    ]

    habitat_diversity = environment[
        "habitat_diversity"
    ]

    if (
        species_richness < 15
        or habitat_diversity == "low"
    ):

        factors.append({
            "variable": "biodiversity",
            "value": {
                "species_richness": species_richness,
                "habitat_diversity": habitat_diversity
            },
            "status": "constrained"
        })

        relationships.append(
            "Low habitat diversity can limit the "
            "range of ecological niches available "
            "to different species."
        )


    # --------------------------------------------------------
    # 5. POLLUTION
    # --------------------------------------------------------

    pollution = environment["pollution"]

    if pollution == "medium":

        factors.append({
            "variable": "pollution",
            "value": pollution,
            "status": "moderate"
        })

        relationships.append(
            "Pollution can add additional environmental "
            "pressure on ecosystems."
        )


    # --------------------------------------------------------
    # REMOVE DUPLICATE ACTIONS
    # --------------------------------------------------------

    candidate_actions = list(
        dict.fromkeys(candidate_actions)
    )


    # --------------------------------------------------------
    # MULTI-METRIC INTERACTION
    # --------------------------------------------------------

    interaction = None

    if (
        organic_carbon < 0.5
        and rainfall == "low"
        and "monoculture" in land_use.lower()
    ):

        interaction = (
            "The combination of low soil organic carbon, "
            "limited water availability and monoculture "
            "indicates multiple simultaneous pressures "
            "on soil function, vegetation resilience "
            "and habitat diversity."
        )


    return {
        "region": region,
        "environment": environment,
        "factors": factors,
        "relationships": relationships,
        "candidate_actions": candidate_actions,
        "multi_metric_interaction": interaction
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = analyze_environment("Pune")

    print()
    print("=" * 70)
    print("DARUKAA.EARTH — MULTI-METRIC ANALYSIS")
    print("=" * 70)

    print("\nREGION:")
    print(result["region"])

    print("\nENVIRONMENT:")
    print(result["environment"])

    print("\nIDENTIFIED FACTORS:")

    for factor in result["factors"]:
        print(
            f"- {factor['variable']}: "
            f"{factor['status']}"
        )

    print("\nRELATIONSHIPS:")

    for relationship in result["relationships"]:
        print(f"- {relationship}")

    print("\nCANDIDATE ACTIONS:")

    for action in result["candidate_actions"]:
        print(f"- {action}")

    print("\nMULTI-METRIC INTERACTION:")

    print(
        result["multi_metric_interaction"]
    )