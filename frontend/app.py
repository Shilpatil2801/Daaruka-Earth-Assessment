import streamlit as st
import requests


# ============================================================
# Configuration
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Daaruka.Earth",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {
        "region": None,
        "last_query": None,
        "last_detected_metrics": []
    }


if "region" not in st.session_state:
    st.session_state.region = "Pune"


# ============================================================
# Header
# ============================================================

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


# ============================================================
# Sidebar
# ============================================================

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

    # Detect region change
    if region != st.session_state.region:

        st.session_state.region = region

        # Reset conversational context when region changes
        st.session_state.conversation_context = {
            "region": region,
            "last_query": None,
            "last_detected_metrics": []
        }

        # Optional: clear previous messages because they
        # belong to the previous environmental context
        st.session_state.messages = []

        st.rerun()

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

        st.session_state.conversation_context = {
            "region": st.session_state.region,
            "last_query": None,
            "last_detected_metrics": []
        }

        st.rerun()


# ============================================================
# Helper Function
# ============================================================

def display_analysis(data):

    # ========================================================
    # Environmental Snapshot
    # ========================================================

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

    # ========================================================
    # Detected Environmental Factors
    # ========================================================

    metrics = data.get("detected_metrics", [])

    if metrics:

        st.markdown("### 🔎 Detected Environmental Factors")

        cols = st.columns(len(metrics))

        for col, metric in zip(cols, metrics):

            with col:

                st.info(
                    metric.replace("_", " ").title()
                )

    # ========================================================
    # Environmental Reasoning
    # ========================================================

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

    # ========================================================
    # Recommendations
    # ========================================================

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

                # ====================================================
                # Scientific Evidence
                # ====================================================

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


# ============================================================
# Display Previous Conversation
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        # Previous assistant analyses are collapsed
        if (
            message["role"] == "assistant"
            and "data" in message
        ):

            with st.expander(
                "🔎 View detailed environmental analysis"
            ):

                display_analysis(
                    message["data"]
                )


# ============================================================
# Chat Input
# ============================================================

query = st.chat_input(
    "Ask an environmental question..."
)


# ============================================================
# Process New Query
# ============================================================

if query:

    # ========================================================
    # User Message
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # ========================================================
    # Backend Request
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing environmental conditions..."
        ):

            try:

                # ------------------------------------------------
                # Retrieve conversation context
                # ------------------------------------------------

                context = (
                    st.session_state.conversation_context
                )

                previous_query = context.get(
                    "last_query"
                )

                previous_metrics = context.get(
                    "last_detected_metrics",
                    []
                )

                # ------------------------------------------------
                # Default query
                # ------------------------------------------------

                enhanced_query = query

                # ------------------------------------------------
                # Detect follow-up questions
                # ------------------------------------------------

                follow_up_phrases = [
                    "what about",
                    "how about",
                    "what else",
                    "and what about",
                    "how does that",
                    "what about that"
                ]

                is_follow_up = (
                    previous_query is not None
                    and any(
                        phrase in query.lower()
                        for phrase in follow_up_phrases
                    )
                )

                # ------------------------------------------------
                # Add previous context internally
                # ------------------------------------------------

                if is_follow_up:

                    enhanced_query = (
                        f"Previous user query: "
                        f"{previous_query}. "

                        f"Previous environmental factors: "
                        f"{', '.join(previous_metrics)}. "

                        f"Current follow-up query: "
                        f"{query}"
                    )

                # ------------------------------------------------
                # Send request to FastAPI
                # ------------------------------------------------

                response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "region": region,
                        "query": enhanced_query
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                # ------------------------------------------------
                # Save conversational context
                # ------------------------------------------------

                st.session_state.conversation_context = {
                    "region": region,
                    "last_query": query,
                    "last_detected_metrics": data.get(
                        "detected_metrics",
                        []
                    )
                }

                # ------------------------------------------------
                # Display CURRENT analysis
                # ------------------------------------------------

                display_analysis(data)

                # ------------------------------------------------
                # Save assistant response
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Here's the environmental "
                            "analysis for your question."
                        ),
                        "data": data
                    }
                )

            # ====================================================
            # Error Handling
            # ====================================================

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

            except requests.exceptions.HTTPError as e:

                st.error(
                    f"Backend error: {e}"
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )