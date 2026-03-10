import streamlit as st
import random
import os

from engine.engine import GameEngine
from engine.states import Role

ROLE_IMAGES = {
    "TENANT": "assets/images/tenant.png",
    "LANDLORD_PRIVATE": "assets/images/private_landlord.png",
    "LANDLORD_SOCIAL": "assets/images/social_landlord.png",
    "LETTING_AGENT": "assets/images/letting_agent.png"
}

# Initialise session variables
if "role" not in st.session_state:
    st.session_state.role = None

engine = st.session_state.get("engine", None)

SOUND_MAP = {
    "Sunny": "assets/sounds/sunny.mp3",
    "Windy": "assets/sounds/windy.mp3",
    "Stormy": "assets/sounds/stormy.mp3",
}

def play_weather_sound(weather):

    last_weather = st.session_state.get("last_weather")

    # Only play when weather changes
    if weather != last_weather:

        sound_file = SOUND_MAP.get(weather)

        if sound_file and os.path.exists(sound_file):

            with open(sound_file, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3", autoplay=True)

        st.session_state["last_weather"] = weather
        
def set_background(weather):

    if weather == "Pending":
        color = "#F4F6FB"   # neutral start

    elif weather == "Sunny":
        color = "#FFF3B0"   # warm happy yellow

    elif weather == "Windy":
        color = "#E9EEF7"   # cool grey-blue

    else:  # Stormy
        color = "#DCE4F5"   # darker tension blue

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            transition: background-color 0.6s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Tenancy Training Simulator", page_icon="☀️", layout="wide")

def banner(weather: str):

    if weather == "Pending":
        return "⏳", "#F4F6FB"

    if weather == "Sunny":
        return "☀️", "#FFE98A"   # bright happy yellow

    if weather == "Windy":
        return "🌤️", "#E3E8F5"   # cool neutral blue-grey

    if weather == "Stormy":
        return "⛈️", "#D4DDF5"   # darker tension blue

    return "🌤️", "#E3E8F5"

def init_game(role: str):

    role_map = {
        "TENANT": Role.TENANT,
        "LANDLORD_PRIVATE": Role.LANDLORD,
        "LANDLORD_SOCIAL": Role.LANDLORD,
        "LETTING_AGENT": Role.LANDLORD,
    }

    st.session_state.engine = GameEngine(role=role_map[role])
    st.session_state.role = role

# Only create engine if role already selected
if "engine" not in st.session_state:
    st.session_state.engine = None

engine = st.session_state.get("engine")

# Sidebar
with st.sidebar:
    st.header("🎭 Choose your character")
    st.caption("Select who you want to play in the tenancy scenario.")

    roles = {
        "TENANT": {
            "image": ROLE_IMAGES["TENANT"],
            "title": "Tenant",
            "description": "You are renting a property and must ensure the deposit is protected."
        },
        "LANDLORD_PRIVATE": {
            "image": ROLE_IMAGES["LANDLORD_PRIVATE"],
            "title": "Private Landlord",
            "description": "You own a rental property and must follow deposit protection rules."
        },
        "LETTING_AGENT": {
            "image": ROLE_IMAGES["LETTING_AGENT"],
            "title": "Letting Agent",
            "description": "You manage tenancies on behalf of landlords and must handle deposits correctly."
        },
        "LANDLORD_SOCIAL": {
            "image": ROLE_IMAGES["LANDLORD_SOCIAL"],
            "title": "Social Landlord",
            "description": "You manage social housing and must comply with deposit scheme regulations."
        }
    }

    for role_name, data in roles.items():
        st.image(data["image"], use_container_width=True)
        st.write(f"**{data['title']}**")
        st.caption(data["description"])

        if st.button(f"Play as {data['title']}", key=f"play_{role_name}"):
            init_game(role_name)
            st.rerun()

    st.divider()


# ---- AFTER SIDEBAR ----
engine = st.session_state.get("engine")

# Stop the app until a character is selected
if engine is None:
    
    import random

    weather_icons = ["☀️", "🌤️", "🌧️", "⛈️"]
    icon = random.choice(weather_icons)
    
    st.markdown(
        f"""
        <div style="text-align:center;font-size:60px;margin-bottom:10px;">
            {icon}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
    """
    <div style="
        text-align:center;
        padding:25px;
        border-radius:14px;
        background:linear-gradient(90deg,#4F6DFF,#7C8DFF);
        color:white;
        border:1px solid #dde3ff;
        margin-bottom:20px;
    ">
        <h1 style="margin-bottom:5px;">🎮 Tenancy Training Simulator</h1>
        <p style="font-size:18px; opacity:0.85;">
        Learn how tenancy decisions affect trust, compliance and deposit outcomes.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown(    
        """
        ### Welcome to the Tenancy Deposit Game

        In this interactive game, your **decisions shape how a tenancy 
        unfolds**. Small choices can have big consequences:

        • Will the deposit be protected correctly?  
        • Will communication build trust or create conflict?  
        • Will the tenancy end smoothly — or lead to a dispute?

    ---
        ### What your decisions influence

        ✔ **Trust** between tenant and landlord  
        ✔ **Compliance** with tenancy rules  
        ✔ **Evidence** available in a dispute  
        ✔ **Legal risk**

    ---
        ### What happens at the end

        The simulator evaluates the likely outcome of an **ADR (Alternative 
        Dispute Resolution)** decision.

        👉 **Choose a character from the sidebar to begin your journey.**
        """
        )
    
    st.info("Select a character from the sidebar to begin the simulation.")
    
    st.stop()

# Main view (only runs once engine exists)
scene_text = engine.get_scene_text()
choices = engine.get_choices()

# Pending weather before any decisions
weather = engine.get_weather_state()

play_weather_sound(weather)
set_background(weather)
emoji, bg = banner(weather)

# Display current role and game controls
current_role = st.session_state.get("role")

role_titles = {
    "TENANT": "Tenant",
    "LANDLORD_PRIVATE": "Private Landlord",
    "LANDLORD_SOCIAL": "Social Landlord",
    "LETTING_AGENT": "Letting Agent"
}

col_role_img, col_role_text, col_buttons = st.columns([1,4,2])

if current_role:

    with col_role_img:
        st.image(ROLE_IMAGES[current_role], width=110)

    with col_role_text:
        st.markdown(f"### 🎮 You are playing as: {role_titles[current_role]}")

    with col_buttons:

        if st.button("🔄 Restart Game"):

            role = st.session_state.get("role")

            st.session_state.pop("engine", None)
            st.session_state.pop("last_weather", None)
            st.session_state.pop("feedback", None)
            st.session_state.pop("await_continue", None)

            init_game(role)

            st.rerun()

        if st.button("🔁 Change Character"):
            st.session_state.clear()
            st.rerun()

else:

    with col_role_text:
        st.markdown("### 🎮 Choose a character from the sidebar to start the simulation")

st.divider()

if weather == "Sunny":
    message = "The tenancy is running smoothly."

elif weather == "Windy":
    message = "Some issues are emerging in the tenancy."

elif weather == "Stormy":
    message = "Serious problems are affecting the tenancy."

else:
    message = "The tenancy has just started."

if weather == "Pending":
    message = "Pending means the tenancy has just started."

st.markdown(
    f"""
    <div style="padding:16px;border-radius:14px;background:{bg};border:1px solid #ddd;
                box-shadow:0px 4px 12px rgba(0,0,0,0.08);
                transition: all 0.4s ease;">
      <div style="font-size:28px;font-weight:700;">{emoji} Tenancy Weather: {weather}</div>
      <div style="opacity:0.85;margin-top:6px;">{message}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown("### Tenancy Lifecycle")

progress = min((engine.timeline.month - 1) / 24, 1.0)

st.progress(progress)

phase = engine.timeline.month

if phase <= 2:
    stage = "🏁 Start of Tenancy"
elif phase <= 6:
    stage = "📄 Agreement & Deposit Protection"
elif phase <= 18:
    stage = "🏡 Mid Tenancy"
elif phase <= 23:
    stage = "🔍 Checkout Preparation"
else:
    stage = "⚖️ ADR / Deposit Resolution"

st.caption(stage)

left, right = st.columns([2, 1], gap="large")

with left:

    # Scenario progress indicator
    current_step = max(engine.timeline.month - 1, 0)

    # Automatically detect number of steps
    total_steps = len(engine.get_choices()) + current_step if engine else 6

    st.caption(f"Scenario {current_step} of {total_steps}")
    st.progress(min(current_step / total_steps, 1.0))

    st.subheader("Tenancy Scenario")

    if "feedback" in st.session_state:

        feedback = st.session_state["feedback"]

        if "Good choice" in feedback or "Excellent" in feedback:
            st.success(feedback)
        elif "Risky" in feedback or "Dangerous" in feedback:
            st.warning(feedback)
        else:
            st.info(feedback)

        if st.session_state.get("await_continue"):

            if st.button("Continue ▶"):

                del st.session_state["feedback"]
                del st.session_state["await_continue"]

                st.rerun()

    if engine and not st.session_state.get("await_continue"):

        st.write(scene_text)
    
        if engine.last_event_message:
            st.warning(engine.last_event_message)

        if engine.last_explanation:
            st.info(engine.last_explanation)

        st.write("### Choices")
    
    st.divider()
    if not choices:

        st.success("Tenancy Simulation Complete")

        st.write("## 🧾 Tenancy Outcome Report")

        compliance = engine.stats.compliance
        trust = engine.stats.trust
        evidence = engine.stats.evidence
        legal_risk = engine.stats.legal_risk
    
        property_health = engine.property.overall_health()

        # Behaviour Summary
        st.write("### Behaviour Summary")
        st.write(f"Compliance score: {compliance}")
        st.write(f"Trust score: {trust}")
        st.write(f"Evidence collected: {evidence}")
        st.write(f"Legal risk: {legal_risk}")    
    
        # Behaviour interpretation
        if compliance >= 3:
            behaviour = "Strong regulatory compliance."
        elif compliance >= 1:
            behaviour = "Moderate compliance with some risks."
        else:
            behaviour = "Poor compliance behaviour."

        # Evidence interpretation
        if evidence >= 3:
            evidence_quality = "Strong documentation and records."
        elif evidence >= 1:
            evidence_quality = "Limited documentation available."
        else:
            evidence_quality = "Little or no evidence was collected."
    
        # Display assessment
        st.write("### Behaviour Assessment")
        st.info(behaviour)
        st.write("### Evidence Assessment")
        st.info(evidence_quality)
        st.write("### ADR Outcome")
        st.success(engine.outcome)
        st.write("### Property Condition")
        st.write(f"Overall property health: {property_health:.0f}%")

        st.divider()

        st.caption("Start a new tenancy simulation to explore different decisions.")

        col1, col2 = st.columns(2)

        with col1:
             if st.button("🔄 Play Again"):

              role = st.session_state.get("role")

              for key in ["engine", "last_weather", "feedback", "await_continue"]:
                if key in st.session_state:
                    del st.session_state[key]

              init_game(role)
              st.rerun()

        with col2:
            if st.button("🏠 Exit the game"):

             st.session_state.clear()
             st.rerun()

    elif not st.session_state.get("await_continue"):

        cols = st.columns(len(choices))

        for i, ch in enumerate(choices):

            with cols[i]:

                if st.button(
                    f"Option {i+1}\n\n{ch.text}",
                    key=f"{engine.state}_{i}",
                    use_container_width=True
                ):
                    feedback = engine.apply_choice(i)
                    st.session_state["feedback"] = feedback
                    st.session_state["await_continue"] = True
                    st.rerun()
   
# Dashboard: shows tenancy progress, behaviour metrics and property condition
with right:
    st.subheader("Dashboard")

    if engine:

        st.write(f"📅 **{engine.timeline.label()}**")

        total_months = 24
        current_month = (engine.timeline.year - 1) * 12 + engine.timeline.month
        progress = min(current_month / total_months, 1.0)
    else:

        st.write("📅 **Tenancy not started**")
        progress = 0
    
    st.write("### Tenancy Progress")
    st.progress(progress)

    current_month = (engine.timeline.year - 1) * 12 + engine.timeline.month if engine else 0

    if current_month <= 2:
        st.caption("Phase: Start of Tenancy")
    elif current_month <= 12:
        st.caption("Phase: Mid Tenancy")
    elif current_month <= 24:
        st.caption("Phase: End of Tenancy")
    else:
        st.caption("Phase: Deposit Resolution / ADR")

    # Timeline event indicator
    if engine and engine.last_event_message:
        st.info(engine.last_event_message)
    
    if engine:

        behaviour_score = (
            engine.stats.compliance
            + engine.stats.evidence
            + engine.stats.trust
            - engine.stats.legal_risk
        )

        max_score = 8
        good_practice_progress = max(0, min(behaviour_score / max_score, 1))

    else:
        good_practice_progress = 0

    st.write("### ✅ Good Practice Meter")
    st.progress(good_practice_progress)
   
    if good_practice_progress < 0.33:
        st.caption("⚠️ Risky tenancy behaviour")
    elif good_practice_progress < 0.66:
        st.caption("🙂 Some good practice")
    else:
        st.caption("🏆 Strong tenancy practice")

    if engine:
        st.metric("Compliance", engine.stats.compliance)
        st.metric("Evidence", engine.stats.evidence)
        st.metric("Trust", engine.stats.trust)
        st.metric("Legal risk", engine.stats.legal_risk)
    else:
        st.metric("Compliance", 0)
        st.metric("Evidence", 0)
        st.metric("Trust", 0)
        st.metric("Legal risk", 0)

   