from App.retrieval import retrieve_documents


def get_evidence(recommendation, top_k=3):

    query = (
        recommendation["action"]
        + ". "
        + recommendation["why"]
        + " "
        + " ".join(recommendation["impacted_metrics"])
    )

    documents = retrieve_documents(query, top_k=top_k)

    evidence = []

    for doc in documents:

        evidence.append({
            "source": doc["source"],
            "page": doc["page"],
            "relevance_distance": round(doc["distance"], 4),
            "text": doc["text"]
        })

    return evidence


if __name__ == "__main__":

    recommendation = {
        "action": (
            "Transition from monoculture toward diversified cropping "
            "with cover crops, mulching and habitat strips."
        ),
        "why": (
            "Multiple environmental pressures are occurring together: "
            "low soil organic carbon, limited water availability and "
            "low land-use diversity."
        ),
        "impacted_metrics": [
            "soil organic carbon",
            "soil moisture",
            "water availability",
            "habitat diversity",
            "species richness",
            "land-use diversity"
        ]
    }

    results = get_evidence(recommendation)

    print()
    print("=" * 75)
    print("DARUKAA.EARTH — SCIENTIFIC EVIDENCE")
    print("=" * 75)

    for i, item in enumerate(results, start=1):

        print(f"\nEVIDENCE {i}")
        print("-" * 75)

        print(f"Source: {item['source']}")
        print(f"Page: {item['page']}")
        print(f"Distance: {item['relevance_distance']}")

        print("\nEvidence:")
        print(item["text"][:1000])