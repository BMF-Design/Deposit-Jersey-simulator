# Copilot instructions for the Tenancy Deposit Game

Short, actionable guidance for AI coding agents working on this repository.

1) Big picture
- Purpose: a small interactive prototype that models tenancy deposit workflows for Tenant and Landlord roles.
- Two UI modes: a Streamlit web UI (`app.py`) and a terminal CLI (`game.py`). Both drive the same core `GameEngine`.
- Core engine: `engine/engine.py` (state machine + `PlayerStats`). Scenes and choices are defined declaratively in `engine/choices.py` and the enums/dataclasses live in `engine/states.py`.

2) Key files and responsibilities
- `app.py`: Streamlit front-end. Initializes a `GameEngine(role)` in `st.session_state.engine` and renders the current scene, choices, and stats. Uses `st.rerun()` after choices.
- `game.py`: Simple CLI runner. Calls `GameEngine` and loops over `get_scene_text()`, `get_choices()`, and `apply_choice()`.
- `engine/engine.py`: `GameEngine` class. Public methods used by UIs: `get_scene_text()`, `get_choices()`, `apply_choice(index)`, `is_game_over()`.
- `engine/choices.py`: `Choice` dataclass, `SCENES` (mapping (Role, GameState) -> str), and `CHOICES` (mapping (Role, GameState) -> list[Choice]). Add or modify gameplay by editing these mappings.
- `engine/states.py`: `Role`, `GameState`, and `PlayerStats` dataclass.

3) How to run locally (dev flows)
- Run web UI (Streamlit):
  - `pip install -r requirements.txt` (if present) or `pip install streamlit`
  - `streamlit run app.py`
- Run CLI: `python game.py`

4) Project-specific conventions and patterns
- Declarative game content: content lives in `engine/choices.py` as `Choice` instances. Prefer adding new entries there rather than hard-coding logic elsewhere.
- Keys: SCENES and CHOICES are keyed by `(Role, GameState)`. Keep keys consistent with `engine/states.py` enums.
- Choice IDs: use concise uppercase IDs (e.g. `T1_READ`, `L3_PROTECT`) and ensure uniqueness across the file.
- Stats changes: a `Choice` modifies `PlayerStats` via `*_delta` fields. Keep these integer deltas small and document intent in `explanation` and `law_reference`.
- UI contract: `get_choices()` returns a list of `Choice` objects; UIs expect `Choice.text`, `.id`, `.explanation`, and `.law_reference` fields.

5) Safe edit rules for AI agents
- Do not change `GameEngine` method signatures without updating both `app.py` and `game.py`.
- When adding states: update `GameState` in `engine/states.py`, then add scene text in `SCENES` and choices in `CHOICES` for both roles if intended.
- Preserve existing `Choice.id` values when editing to avoid breaking any analytics or saved state assumptions.

6) Extension examples (copy/paste patterns)
- Add a scene:
  - In `engine/choices.py`:
    SCENES[(Role.TENANT, GameState.NEW_STATE)] = "Short scene text here."
- Add a choice for a tenant state:
    CHOICES[(Role.TENANT, GameState.NEW_STATE)] = [
        Choice(id="T_NEW", text="Do X", next_state=GameState.MID_TENANCY, compliance_delta=1, explanation="Why this matters."),
    ]

7) Dependencies & integration points
- `streamlit` is required for `app.py`. There are no other external services in the prototype.
- The engine is synchronous and in-memory; there is no DB or network integration.

8) What to look for when modifying gameplay
- Keep scene text short and focused — `app.py` renders it directly.
- Update `law_reference` strings on `Choice` when adding legal guidance; `app.py` shows these in an expander.
- If you change stats or add new stats fields, adjust `app.py`'s dashboard metrics accordingly.

9) Tests & debugging
- There are no tests in the project currently. To validate changes quickly:
  - Run `python game.py` for CLI smoke tests.
  - Run `streamlit run app.py` to exercise the web UI (click through choices).

10) When to ask the repo owner
- If you need a canonical list of law references or mappings to real schemes, ask before introducing external data.

If any section is unclear or you'd like more examples (e.g., how to add a final-state/ADR flow), tell me which part to expand.
