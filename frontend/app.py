import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/analyze"


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Daaruka.Earth",
    page_icon="🌍",
    layout="wide"
)


# -----------------------------
# Session state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "region" not in st.session_state:
    st.session_state.region = "Pune"


# -----------------------------
# Header
# -----------------------------

st.title("🌍 Daaruka.Earth")
st.subheader("AI Biodiversity Intelligence Assistant")

st.markdown(
    f"""
    Currently analyzing **{st.session_state.region}**.

    Ask questions about **soil health, water availability, biodiversity,
    land use, climate and environmental sustainability**.

    The system combines structured environmental data with
    scientifically grounded knowledge retrieval.
    """
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("🌱 Environment")

    regions = [
        "Pune",
        "Nagpur",
        "Nashik",
        "Ahmednagar",
        "Kolhapur"
    ]

    region = st.selectbox(
        "Select region",
        regions,
        index=regions.index(st.session_state.region)
    )

    st.session_state.region = region

    st.divider()

    st.markdown("### Environmental Metrics")

    st.markdown(
        """
        - 🧪 Soil health
        - 💧 Water availability
        - 🌿 Biodiversity
        - 🌾 Land use
        - 🏭 Pollution
        - 🌡️ Climate
        """
    )

    st.divider()

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# Helper function
# -----------------------------

def display_analysis(data):

    # -------------------------
    # Environmental Snapshot
    # -------------------------

    environment = data.get("environment")

    if environment:

        st.markdown("### 🌱 Environmental Snapshot")

        cols = st.columns(4)

        with cols[0]:
            st.metric(
                "Soil pH",
                environment.get("soil_ph", "N/A")
            )

        with cols[1]:
            st.metric(
                "Organic Carbon",
                environment.get("organic_carbon", "N/A")
            )

        with cols[2]:
            st.metric(
                "Soil Moisture",
                environment.get("soil_moisture", "N/A")
            )

        with cols[3]:
            st.metric(
                "Temperature",
                f"{environment.get('temperature', 'N/A')}°C"
            )

        cols = st.columns(4)

        with cols[0]:
            st.metric(
                "Rainfall",
                environment.get("rainfall", "N/A")
            )

        with cols[1]:
            st.metric(
                "Species Richness",
                environment.get("species_richness", "N/A")
            )

        with cols[2]:
            st.metric(
                "Habitat Diversity",
                environment.get("habitat_diversity", "N/A")
            )

        with cols[3]:
            st.metric(
                "Pollution",
                environment.get("pollution", "N/A")
            )

        st.markdown(
            f"**Current land use:** "
            f"{environment.get('land_use', 'N/A')}"
        )

    # -------------------------
    # Detected Metrics
    # -------------------------

    metrics = data.get("detected_metrics", [])

    if metrics:

        st.markdown("### 🔎 Detected Environmental Factors")

        cols = st.columns(len(metrics))

        for col, metric in zip(cols, metrics):

            with col:
                st.info(
                    metric.replace("_", " ").title()
                )

    # -------------------------
    # Environmental Reasoning
    # -------------------------

    reasoning = data.get("reasoning")

    if reasoning:

        st.markdown("### 🧠 Environmental Reasoning")

        relationships = reasoning.get(
            "relationships",
            []
        )

        if relationships:

            for relationship in relationships:

                st.info(
                    f"🔗 {relationship}"
                )

        interaction = reasoning.get(
            "multi_metric_interaction"
        )

        if interaction:

            st.markdown(
                "#### Multi-Metric Interaction"
            )

            st.warning(interaction)

    # -------------------------
    # Recommendations
    # -------------------------

    recommendations = data.get(
        "recommendations",
        []
    )

    if recommendations:

        st.markdown("### 💡 Recommendations")

        for i, rec in enumerate(
            recommendations,
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"#### {i}. "
                    f"{rec.get('action', 'Recommendation')}"
                )

                if rec.get("why"):

                    st.markdown(
                        f"**Why:** {rec['why']}"
                    )

                if rec.get("metrics"):

                    st.markdown(
                        "**Impacted metrics:** "
                        + ", ".join(
                            rec["metrics"]
                        )
                    )

                if rec.get("time_horizon"):

                    st.markdown(
                        "**Time horizon:** "
                        + rec["time_horizon"]
                    )

                if rec.get("confidence"):

                    st.markdown(
                        "**Confidence:** "
                        + rec["confidence"]
                    )

                # -----------------
                # Evidence
                # -----------------

                evidence = rec.get(
                    "evidence",
                    []
                )

                if evidence:

                    st.markdown(
                        "**📚 Scientific Evidence**"
                    )

                    for item in evidence:

                        source = item.get(
                            "source",
                            "Unknown"
                        )

                        page = item.get(
                            "page",
                            "N/A"
                        )

                        text = item.get(
                            "text",
                            ""
                        )

                        st.markdown(
                            f"**{source} — Page {page}**"
                        )

                        st.caption(text)

    else:

        st.warning(
            "No recommendations were generated."
        )


# -----------------------------
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "data" in message
        ):

            display_analysis(
                message["data"]
            )


# -----------------------------
# Chat input
# -----------------------------

query = st.chat_input(
    "Ask an environmental question..."
)


if query:

    # -------------------------
    # User message
    # -------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # -------------------------
    # Backend request
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing environmental conditions..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "region": st.session_state.region,
                        "query": query
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                display_analysis(data)

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Environmental analysis "
                            "completed."
                        ),
                        "data": data
                    }
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the backend. "
                    "Make sure FastAPI is running on "
                    "http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The backend took too long to respond."
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )