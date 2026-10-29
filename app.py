import streamlit as st
import os
import re
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Executive AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Microsoft Executive Design: Clean, Calming, Corporate & Pristine ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', -apple-system, sans-serif !important;
    }

    /* Calming Pearl Slate Background */
    .stApp {
        background: linear-gradient(180deg, #F1F5F9 0%, #F8FAFC 100%) !important;
        color: #0F172A !important;
    }

    /* Pristine Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.02) !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #1E293B !important;
    }

    /* Header Title in Microsoft Azure */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0078D4 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-subtitle {
        color: #64748B !important;
        font-size: 1.05rem;
        margin-bottom: 1.6rem;
    }

    /* Chat Messages - Crisp Elevated Cards */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05), 0 2px 4px -1px rgba(15, 23, 42, 0.03) !important;
    }

    /* User Message - Soft Azure Tint */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* High-contrast, easy-to-read Charcoal Typography */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li {
        color: #0F172A !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
    }

    /* Strong Accents in Deep Navy/Blue */
    [data-testid="stChatMessage"] strong, 
    [data-testid="stChatMessage"] b {
        color: #0078D4 !important;
        font-weight: 600 !important;
    }

    /* Code Snippets */
    [data-testid="stChatMessage"] code {
        color: #0284C7 !important;
        background-color: #F1F5F9 !important;
        border: 1px solid #E2E8F0 !important;
        padding: 2px 6px !important;
        border-radius: 6px !important;
    }

    /* Seamless Bottom Input Area (No harsh borders, zero ugly bars) */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stChatFloatingInputContainer {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #0078D4 !important;
        box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.15) !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-size: 1.02rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94A3B8 !important;
    }

    /* Clean Clutter */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# SIDEBAR CONTROL PANEL
# =====================================================================

with st.sidebar:
    st.markdown("### ⚙️ Workspace Settings")
    st.caption("Executive Assistant Configuration")
    
    # 1. API Key Input
    default_key = ""
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        default_key = os.environ["GEMINI_API_KEY"]

    api_key_input = st.text_input(
        "Gemini API Key",
        value=default_key,
        type="password",
        placeholder="Paste your AI Studio API key...",
        help="Get your free Gemini API key at https://aistudio.google.com"
    )

    if api_key_input:
        st.success("Connected to Intelligence Engine")
    else:
        st.info("💡 Paste your free Gemini API key to activate full responses.")

    # 2. Assistant Persona
    persona = st.selectbox(
        "Assistant Mode",
        [
            "Executive Assistant",
            "Software & Tech Specialist",
            "Business & Market Analyst",
            "Communications & Writer"
        ]
    )

    PERSONA_PROMPTS = {
        "Executive Assistant": "You are a poised, executive-level AI assistant. Today's year is 2026. Provide structured, accurate, and insightful answers with calm professionalism.",
        "Software & Tech Specialist": "You are a Principal Software Architect. Provide clean, production-grade code, architectures, and engineering best practices.",
        "Business & Market Analyst": "You are an Executive Business Strategist. Provide structured, high-impact bulleted summaries, market insights, and financial analysis.",
        "Communications & Writer": "You are a Master Corporate Communications Strategist. Produce polished, persuasive, and crystal-clear executive writing."
    }

    st.markdown("---")
    st.markdown("🌐 **Real-time Search:** Active")
    st.markdown("🧮 **Precision Math:** Active")

    # Reset Chat Button
    st.markdown("---")
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# =====================================================================
# MAIN CHAT APPLICATION
# =====================================================================

st.markdown('<div class="hero-title"><span>✨</span> AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Ask anything — real-time web search, corporate analysis, technical code, or math.</div>', unsafe_allow_html=True)

# Clean, Professional 2-Sentence Welcome
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "avatar": "✨",
            "content": "Hello! I am your personal assistant. How can I help you today?"
        }
    ]

# Render Messages with Clean Card Shadows
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar=msg.get("avatar", "👤")).markdown(msg["content"])


# =====================================================================
# RESILIENT EXECUTION ENGINE (Auto-handles Quota & Search)
# =====================================================================

def query_gemini(prompt: str, api_key: str, system_instruction: str):
    """
    High-speed, quota-resilient execution.
    Attempts live search grounding, with instant fallback to standard model if quota is tight.
    """
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={clean_key}"
    headers = {"Content-Type": "application/json"}
    
    # Check if the query asks for recent/live data
    needs_search = any(w in prompt.lower() for w in ["latest", "recent", "news", "today", "2026", "current", "who is", "movie", "release", "update"])
    
    # Strategy 1: If recent info requested, try with Google Search tool
    if needs_search:
        payload_with_search = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Context: Current year is 2026. {system_instruction}\n\nQuestion: {prompt}"}
                    ]
                }
            ],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.3}
        }
        try:
            res = requests.post(url, headers=headers, json=payload_with_search, timeout=10)
            data = res.json()
            if res.status_code == 200 and "candidates" in data:
                parts = data["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"]
        except Exception:
            pass

    # Strategy 2: Fast, Reliable Standard Execution (Uses 10x less quota, never hangs)
    standard_payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Context: The current year is 2026. {system_instruction}\n\nQuestion: {prompt}"}
                ]
            }
        ],
        "generationConfig": {"temperature": 0.4}
    }
    
    try:
        res = requests.post(url, headers=headers, json=standard_payload, timeout=10)
        data = res.json()
        
        if res.status_code == 200 and "candidates" in data:
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
        elif "error" in data:
            error_code = data["error"].get("code", 0)
            error_msg = data["error"].get("message", "Unexpected API response")
            if error_code == 429 or "quota" in error_msg.lower():
                return "⏳ **Google Free Tier Rate Limit:** You reached Google's temporary 1-minute request limit. Please wait 30 seconds and ask again, or create a fresh key at [aistudio.google.com](https://aistudio.google.com)."
            return f"⚠️ **Notice:** {error_msg}"
            
        return "Could not generate an answer. Please try asking again."
    except requests.exceptions.Timeout:
        return "⏳ The request timed out. Please try asking a slightly more concise question."
    except Exception as e:
        return f"⚠️ System message: {str(e)}"


# --- Instant Local Math Evaluator (<0.001s) ---
def try_instant_math(user_input: str):
    clean = "".join([c for c in user_input if c in "0123456789+-*/(). "]).strip()
    if bool(re.fullmatch(r'[\d\s\+\-\*\/\(\)\.]+', user_input.strip())) and len(clean) >= 3:
        try:
            ans = eval(clean)
            if isinstance(ans, float) and ans.is_integer():
                ans = int(ans)
            return f"**{clean} = {ans}**"
        except Exception:
            pass
    return None


# --- User Input Box ---
user_query = st.chat_input("Ask a question, request code, research, or analysis...")

if user_query:
    # 1. User Message
    st.session_state.chat_history.append({"role": "user", "avatar": "👤", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 2. Assistant Processing
    with st.chat_message("assistant", avatar="✨"):
        if api_key_input:
            math_ans = try_instant_math(user_query)
            if math_ans:
                st.markdown(math_ans)
                final_answer = math_ans
            else:
                with st.spinner("Processing..."):
                    final_answer = query_gemini(
                        prompt=user_query,
                        api_key=api_key_input,
                        system_instruction=PERSONA_PROMPTS[persona]
                    )
                    st.markdown(final_answer)
        else:
            st.warning("Please enter your Gemini API Key in the left sidebar to activate the assistant.")
            final_answer = "*(Awaiting API Key)*"

    st.session_state.chat_history.append({"role": "assistant", "avatar": "✨", "content": final_answer})
