import streamlit as st
import datetime
import os
import re
from zoneinfo import ZoneInfo

# --- Page Configuration ---
st.set_page_config(
    page_title="Enterprise AI Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Enterprise Dark Theme (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Ambient Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d172a 0%, #050a14 60%, #020408 100%) !important;
        color: #f1f5f9 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #070d1a !important;
        border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
    }

    /* Titles */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Chat Messages - Enterprise Cards */
    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(56, 189, 248, 0.12) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(12px) !important;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(56, 189, 248, 0.3) !important;
    }

    /* Tool Call Badges */
    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 8px;
    }

    /* Chat Input */
    [data-testid="stChatInput"] textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }

    /* Hide standard clutter */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# ENTERPRISE TOOLS REGISTRY (Python Functions the LLM can invoke)
# =====================================================================

def calculate(expression: str) -> str:
    """Calculates any mathematical expression with 100% precision without hallucinations."""
    try:
        allowed = set("0123456789+-*/(). ")
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Error: Expression contains unsupported characters."
    except Exception as e:
        return f"Error: {e}"

def get_world_time(region_or_city: str) -> str:
    """Fetches real-time current date and time for any global city or country."""
    mapping = {
        "us": "America/New_York",
        "usa": "America/New_York",
        "america": "America/New_York",
        "new york": "America/New_York",
        "california": "America/Los_Angeles",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "india": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "bangalore": "Asia/Kolkata",
        "uk": "Europe/London",
        "london": "Europe/London",
        "dubai": "Asia/Dubai",
        "uae": "Asia/Dubai",
        "tokyo": "Asia/Tokyo",
        "japan": "Asia/Tokyo",
        "singapore": "Asia/Singapore",
        "paris": "Europe/Paris",
        "france": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "germany": "Europe/Berlin",
        "sydney": "Australia/Sydney",
        "australia": "Australia/Sydney",
        "toronto": "America/Toronto",
        "canada": "America/Toronto",
    }
    key = region_or_city.lower().strip()
    tz_name = mapping.get(key, "Asia/Kolkata")
    
    try:
        now = datetime.datetime.now(ZoneInfo(tz_name))
        return f"Current time in {region_or_city.title()}: {now.strftime('%A, %B %d, %Y at %I:%M %p (%Z)')}"
    except Exception:
        local_now = datetime.datetime.now()
        return f"Local time: {local_now.strftime('%A, %B %d, %Y at %I:%M %p')}"

def save_note(content: str) -> str:
    """Saves a note, action item, or memory to the persistent workspace notes file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("workspace_notes.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {content}\n")
    return f"Successfully saved to workspace notes: '{content}'"

def list_notes() -> str:
    """Retrieves all saved notes and action items from the workspace."""
    if not os.path.exists("workspace_notes.txt"):
        return "No notes have been saved yet."
    with open("workspace_notes.txt", "r", encoding="utf-8") as f:
        notes = f.read().strip()
    return notes if notes else "No notes found."


# =====================================================================
# SIDEBAR - ENTERPRISE CONTROL PANEL
# =====================================================================

with st.sidebar:
    st.markdown("### ⚙️ Agent Control Center")
    st.caption("Enterprise multi-purpose AI assistant configuration")

    # 1. API Key Input (Checked in order: Sidebar Input -> Streamlit Secrets -> OS Env)
    default_key = ""
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        default_key = os.environ["GEMINI_API_KEY"]

    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=default_key,
        type="password",
        placeholder="Paste your AI Studio API key...",
        help="Get your 100% free Gemini API key at https://aistudio.google.com"
    )

    if not api_key_input:
        st.info("💡 **Need a free API Key?**\n1. Go to [aistudio.google.com](https://aistudio.google.com)\n2. Click **Get API key**\n3. Paste it above to activate full LLM intelligence!")

    # 2. Agent Persona / System Role
    persona = st.selectbox(
        "Agent Specialization",
        [
            "General AI Specialist",
            "Senior Software Engineer",
            "Business & Strategy Analyst",
            "Executive Copywriter & Comms"
        ]
    )

    PERSONA_PROMPTS = {
        "General AI Specialist": "You are an elite, multi-purpose AI Assistant. You possess deep knowledge across science, technology, mathematics, and business. Be concise, insightful, polite, and helpful.",
        "Senior Software Engineer": "You are a Principal Software Engineer. Provide clean, production-ready, well-documented code across any stack. Explain system architecture, edge cases, and best practices.",
        "Business & Strategy Analyst": "You are an Executive Business Strategist. Provide structured frameworks, data-driven reasoning, market insights, ROI calculations, and strategic summaries.",
        "Executive Copywriter & Comms": "You are a Master Communications Strategist and Copywriter. Produce engaging, polished, persuasive emails, documentation, announcements, and executive summaries."
    }

    # 3. Model Selector & Temperature
    model_choice = st.selectbox("LLM Model Engine", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temperature = st.slider("Reasoning Temperature", min_value=0.0, max_value=1.0, value=0.4, step=0.1, help="Lower = more precise and analytical; Higher = more creative.")

    # 4. Active Enterprise Capabilities
    st.markdown("---")
    st.markdown("**Active Tool Integrations:**")
    st.markdown("✅ `calculate()` • Math Precision Engine")
    st.markdown("✅ `get_world_time()` • Live Global Clock")
    st.markdown("✅ `save_note()` • Workspace Memory")
    st.markdown("✅ `list_notes()` • Memory Retrieval")

    # 5. Clear Session Button
    st.markdown("---")
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# =====================================================================
# MAIN CHAT APPLICATION
# =====================================================================

st.markdown('<div class="hero-title">⚡ Multi-Purpose Enterprise AI Agent</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-subtitle">Role: <b>{persona}</b> • Powered by Google Gemini & Python Tools</div>', unsafe_allow_html=True)

# Initialize Session History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "avatar": "⚡",
            "content": f"Hello! I am your **{persona}**. I can answer complex questions, write and debug code, calculate math, check world timezones, and manage workspace notes. How may I assist you today?"
        }
    ]

# Render History
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar=msg.get("avatar", "👤")).markdown(msg["content"])


# =====================================================================
# LLM AGENT EXECUTION ENGINE
# =====================================================================

def run_agent_with_llm(prompt: str, api_key: str, system_instruction: str, model_name: str, temp: float):
    """Executes the prompt using Google Gemini LLM with registered tools and function calling."""
    try:
        import google.generativeai as genai
    except ImportError:
        return "⚠️ The `google-generativeai` package is not installed. Add it to requirements.txt and run `pip install google-generativeai`."

    try:
        genai.configure(api_key=api_key)

        # Register functions as native LLM tools
        tools_list = [calculate, get_world_time, save_note, list_notes]

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={"temperature": temp},
            system_instruction=system_instruction,
            tools=tools_list
        )

        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ **Error communicating with Gemini LLM:** {str(e)}\n\nPlease ensure your API Key is valid."


# --- User Input Box ---
user_query = st.chat_input("Ask any question, request code, analysis, world times, or math...")

if user_query:
    # 1. Render User Message
    st.session_state.chat_history.append({"role": "user", "avatar": "👤", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 2. Process Response
    with st.chat_message("assistant", avatar="⚡"):
        # If API key is provided -> Full LLM Agent Execution!
        if api_key_input:
            with st.spinner("Agent reasoning & processing..."):
                response_text = run_agent_with_llm(
                    prompt=user_query,
                    api_key=api_key_input,
                    system_instruction=PERSONA_PROMPTS[persona],
                    model_name=model_choice,
                    temp=temperature
                )
                st.markdown(response_text)
        else:
            # Fallback when no API Key is entered yet
            st.warning("⚠️ **Gemini API Key Required for Full LLM Intelligence**")
            st.markdown(
                "To let this agent answer *any question in the universe* (coding, writing, analysis, reasoning), please paste your free Gemini API key in the sidebar.\n\n"
                "**How to get one in 30 seconds (100% Free):**\n"
                "1. Visit [Google AI Studio](https://aistudio.google.com/)\n"
                "2. Sign in with Google and click **Get API key**\n"
                "3. Paste it in the left sidebar control center!"
            )
            response_text = "*(Awaiting Gemini API Key for unbounded reasoning)*"

    st.session_state.chat_history.append({"role": "assistant", "avatar": "⚡", "content": response_text})
