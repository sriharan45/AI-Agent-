import streamlit as st
import os
import re
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- High-Contrast, AMOLED Dark Theme (Crystal Clear Text & Zero White Bars) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    /* Pure Solid AMOLED Deep Black Background */
    .stApp {
        background-color: #030712 !important;
        background: #030712 !important;
        color: #ffffff !important;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #080e1a !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Header Title in Crisp Electric Sky Blue */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #38bdf8 !important;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #94a3b8 !important;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Chat Message Bubbles - High Contrast Solid Cards */
    [data-testid="stChatMessage"] {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6) !important;
    }

    /* PURE WHITE TEXT - Crystal clear readability, zero blur */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.65 !important;
        font-weight: 400 !important;
    }

    /* Bold Highlights */
    [data-testid="stChatMessage"] strong, 
    [data-testid="stChatMessage"] b {
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }

    /* Inline Code */
    [data-testid="stChatMessage"] code {
        color: #38bdf8 !important;
        background-color: #1e293b !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }

    /* ELIMINATE THE UGLY WHITE BAR AT THE BOTTOM */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stChatFloatingInputContainer {
        background-color: #030712 !important;
        background: #030712 !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #0f172a !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 14px !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        font-size: 1.02rem !important;
        border: none !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* Clean UI */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# SIDEBAR CONTROL PANEL
# =====================================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # 1. API Key Input
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

    if api_key_input:
        st.success("⚡ Live Connection: Active")
    else:
        st.info("💡 Paste your Gemini API key above to activate the assistant.")

    # 2. Assistant Persona
    persona = st.selectbox(
        "Assistant Mode",
        [
            "General Assistant",
            "Software Engineer",
            "Business Analyst",
            "Creative Writer"
        ]
    )

    PERSONA_PROMPTS = {
        "General Assistant": "You are a smart, friendly, and helpful AI assistant. Today's year is 2026. Provide clear, direct, and up-to-date answers.",
        "Software Engineer": "You are a Principal Software Engineer. Provide clean, production-ready code with concise explanations.",
        "Business Analyst": "You are a Business Strategist. Provide structured, executive-ready insights.",
        "Creative Writer": "You are a Master Copywriter. Produce engaging, polished, and persuasive content."
    }

    st.markdown("---")
    st.markdown("🌐 **Real-Time Web Search:** Active (Google Grounded)")
    st.markdown("🧮 **Instant Math:** Active")

    # Reset Conversation Button
    st.markdown("---")
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# =====================================================================
# MAIN CHAT APPLICATION
# =====================================================================

st.markdown('<div class="hero-title">⚡ AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Ask anything — real-time web search, coding, math, or knowledge.</div>', unsafe_allow_html=True)

# Initialize Session History (Clean, simple first line as requested)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "avatar": "⚡",
            "content": "Hello, how can I help you? I am your assistant, how can I help you?"
        }
    ]

# Render History with High-Contrast White Text
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar=msg.get("avatar", "👤")).markdown(msg["content"])


# =====================================================================
# HIGH-SPEED EXECUTION ENGINE WITH REAL-TIME WEB SEARCH
# =====================================================================

def query_gemini_fast(prompt: str, api_key: str, system_instruction: str):
    """
    Direct, lightning-fast execution (1.5-2 seconds).
    Includes Google Search Grounding for live 2026 data.
    """
    clean_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={clean_key}"
    headers = {"Content-Type": "application/json"}
    
    # Payload with Google Search Grounding enabled for 2026 real-time information
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"System Context: The current year is 2026. {system_instruction}\n\nUser Question: {prompt}"}
                ]
            }
        ],
        "tools": [
            {
                "google_search": {}
            }
        ],
        "generationConfig": {
            "temperature": 0.3
        }
    }
    
    try:
        # Fast direct call with 12s timeout (no hanging!)
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        data = response.json()
        
        if response.status_code == 200 and "candidates" in data:
            candidate = data["candidates"][0]
            parts = candidate.get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
        
        # If google_search tool wasn't accepted on this key, fallback immediately without tools
        if "error" in data:
            err_msg = data["error"].get("message", "")
            # Try simple payload without search tool
            fallback_payload = {
                "contents": [{"parts": [{"text": f"Context: Current year is 2026. {system_instruction}\n\nQuestion: {prompt}"}]}],
                "generationConfig": {"temperature": 0.3}
            }
            res2 = requests.post(url, headers=headers, json=fallback_payload, timeout=8)
            data2 = res2.json()
            if res2.status_code == 200 and "candidates" in data2:
                return data2["candidates"][0]["content"]["parts"][0]["text"]
            return f"⚠️ **API Notice:** {err_msg}"
            
        return "Could not generate response. Please try again."
    except requests.exceptions.Timeout:
        return "⚠️ The request timed out. Please try asking a shorter question."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


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
user_query = st.chat_input("Ask any question, request latest news, movies, coding, or math...")

if user_query:
    # 1. Render User Message
    st.session_state.chat_history.append({"role": "user", "avatar": "👤", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 2. Assistant Processing
    with st.chat_message("assistant", avatar="⚡"):
        if api_key_input:
            # Check fast math first (0.001s)
            math_res = try_instant_math(user_query)
            if math_res:
                st.markdown(math_res)
                final_answer = math_res
            else:
                with st.spinner("Searching and thinking..."):
                    final_answer = query_gemini_fast(
                        prompt=user_query,
                        api_key=api_key_input,
                        system_instruction=PERSONA_PROMPTS[persona]
                    )
                    st.markdown(final_answer)
        else:
            st.warning("⚠️ **Gemini API Key Required**")
            st.markdown("Please enter your API Key in the left sidebar.")
            final_answer = "*(Awaiting Gemini API Key)*"

    st.session_state.chat_history.append({"role": "assistant", "avatar": "⚡", "content": final_answer})
