import streamlit as st

from engine.engine import GameEngine
from engine.states import Role

st.write("App is running")

st.set_page_config(page_title="Tenancy Deposit Game", page_icon="🏠", layout="wide")


def reset_game():
    st.session_state.engine = None
    st.session_state.role = None


st.title("🏠 Tenancy Deposit Game")
st.caption("Learn the full deposit journey: agreement → deposit protection → end of tenancy → return or dispute.")

# Session state init
if "engine" not in st.session_state:
    st.session_state.engine = None
if "role" not in st.session_state:
    st.session_state.role = None

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Restart"):
        reset_game()
        st.rerun()

# Role selection screen
if st.session_state.engine is None:
    st.subheader("Choose your role")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("I am a Tenant"):
            st.session_state.role = Role.TENANT
            st.session_state.engine = GameEngine(Role.TENANT)
            st.rerun()

    with col2:
        if st.button("I am a Landlord"):
            st.session_state.role = Role.LANDLORD
            st.session_state.engine = GameEngine(Role.LANDLORD)
            st.rerun()

    st.stop()

engine = st.session_state.engine

# Main layout
left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("Current situation")
    st.write(engine.get_scene_text())

    choices = engine.get_choices()
    if not choices:
        st.success("End of current prototype path.")
        st.stop()

    st.subheader("What do you do next?")
    for i, c in enumerate(choices):
        if st.button(c.text, key=f"choice_{c.id}"):
            explanation = engine.apply_choice(i)
            st.session_state.last_explanation = explanation
            st.session_state.last_law = c.law_reference
            st.rerun()

    # Feedback panel
    if "last_explanation" in st.session_state:
        st.info(st.session_state.last_explanation)

    if "last_law" in st.session_state and st.session_state.last_law:
        with st.expander("📚 Law / guidance reference"):
            st.write(st.session_state.last_law)

with right:
    st.subheader("Player dashboard")
    s = engine.stats
    st.metric("Compliance", s.compliance)
    st.metric("Trust", s.trust)
    st.metric("Evidence", s.evidence)
    st.metric("Legal Risk", s.legal_risk)

    # Optional: simple progress estimate (you can replace with real mapping)
    progress = min(max((s.compliance + s.evidence + s.trust) / 10, 0), 1)
    st.progress(progress, text="Progress (prototype estimate)")