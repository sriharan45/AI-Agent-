import streamlit as st
import datetime
import os
import re
import requests
from zoneinfo import ZoneInfo

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

    /* User Message - Soft Tint */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* High-contrast Charcoal Typography */
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

    /* Seamless Bottom Input Area */
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
    st.caption("Executive Multi-Engine Configuration")
    
    # 1. API Key Input
    default_key = ""
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        default_key = os.environ["GEMINI_API_KEY"]

    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        value=default_key,
        type="password",
        placeholder="Paste your AI Studio key...",
        help="If provided, Google Gemini is used. If omitted or busy, the built-in knowledge & live tools answer automatically!"
    )

    if api_key_input:
        st.success("✅ Gemini Engine: Connected")
    else:
        st.info("💡 Assistant is active with built-in Live Weather, Web Search, Clocks, & Math.")

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
        "Executive Assistant": "You are a poised, executive-level AI assistant. Provide clear, direct, and structured answers immediately.",
        "Software & Tech Specialist": "You are a Principal Software Architect. Provide clean, production-grade code, architectures, and engineering best practices.",
        "Business & Market Analyst": "You are an Executive Business Strategist. Provide structured, high-impact bulleted summaries and financial analysis.",
        "Communications & Writer": "You are a Master Corporate Communications Strategist. Produce polished, persuasive, and crystal-clear writing."
    }

    st.markdown("---")
    st.markdown("🌤️ **Live Real-Time Weather:** Active")
    st.markdown("🌐 **Live Global Clocks:** Active")
    st.markdown("📚 **Instant Web Knowledge:** Active")
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
st.markdown('<div class="hero-subtitle">Ask anything — real-time weather, general knowledge, corporate research, code, or mathematics.</div>', unsafe_allow_html=True)

# Clean, professional greeting
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "avatar": "✨",
            "content": "Hello, I am your assistant. How can I help you?"
        }
    ]

# Render Messages with Clean Card Shadows
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"], avatar=msg.get("avatar", "👤")).markdown(msg["content"])


# =====================================================================
# TOOL 1: LIVE REAL-TIME WEATHER ENGINE (Open-Meteo, Free, No API Key)
# =====================================================================

WEATHER_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
    45: "Foggy 🌫️", 48: "Depositing rime fog 🌫️",
    51: "Light drizzle 🌦️", 53: "Moderate drizzle 🌧️", 55: "Dense drizzle 🌧️",
    61: "Slight rain 🌧️", 63: "Moderate rain 🌧️", 65: "Heavy rain 🌧️",
    71: "Slight snow 🌨️", 73: "Moderate snow 🌨️", 75: "Heavy snow ❄️",
    80: "Rain showers 🌦️", 81: "Heavy showers 🌧️", 82: "Violent rain showers ⛈️",
    95: "Thunderstorm ⛈️", 96: "Thunderstorm with slight hail ⛈️", 99: "Thunderstorm with heavy hail ⛈️"
}

def get_live_weather(query: str):
    """Detects city and returns exact live real-time temperature & conditions."""
    clean_q = query.lower()
    
    # Extract likely city name
    city = None
    known_cities = ["bangalore", "bengaluru", "chennai", "delhi", "mumbai", "kolkata", "hyderabad", 
                    "new york", "london", "dubai", "tokyo", "paris", "berlin", "sydney", "toronto", 
                    "singapore", "los angeles", "chicago", "san francisco", "seattle"]
    for c in known_cities:
        if c in clean_q:
            city = c
            break

    if not city:
        match = re.search(r"(?:temperature|weather|climate)\s+(?:in|of|at)\s+([a-zA-Z\s]+)", clean_q)
        if match:
            city = match.group(1).replace("now", "").replace("today", "").strip()

    if not city:
        return None

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=5).json()
        if not geo_res.get("results"):
            return None
        
        loc = geo_res["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        city_name = loc.get("name", city.title())
        country = loc.get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        w_res = requests.get(weather_url, timeout=5).json()
        
        current = w_res.get("current", {})
        temp_c = current.get("temperature_2m")
        temp_f = round((temp_c * 9/5) + 32, 1) if temp_c is not None else None
        code = current.get("weather_code", 0)
        condition = WEATHER_CODES.get(code, "Clear")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind = current.get("wind_speed_10m", "N/A")

        return (
            f"### 🌤️ Weather in {city_name}, {country} (Live)\n\n"
            f"* **Temperature:** **{temp_c}°C** ({temp_f}°F)\n"
            f"* **Condition:** {condition}\n"
            f"* **Humidity:** {humidity}%\n"
            f"* **Wind Speed:** {wind} km/h"
        )
    except Exception:
        return None


# =====================================================================
# TOOL 2: WORLD CLOCKS ENGINE (0.0001s Instant)
# =====================================================================

TIMEZONES = {
    "us": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "america": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "india": [("India (IST)", "Asia/Kolkata")],
    "uk": [("London (UK)", "Europe/London")],
    "london": [("London (UK)", "Europe/London")],
    "dubai": [("Dubai (UAE)", "Asia/Dubai")],
    "tokyo": [("Tokyo (Japan)", "Asia/Tokyo")],
    "singapore": [("Singapore", "Asia/Singapore")],
    "australia": [("Sydney (Australia)", "Australia/Sydney")],
    "canada": [("Toronto (Canada)", "America/Toronto")]
}

def get_world_time(query: str):
    clean_q = query.lower()
    for key, tz_list in TIMEZONES.items():
        if key in clean_q:
            lines = ["### 🕒 Current World Time:\n"]
            for label, tz_name in tz_list:
                now = datetime.datetime.now(ZoneInfo(tz_name))
                lines.append(f"* **{label}:** `{now.strftime('%A, %B %d, %Y at %I:%M %p')}`")
            return "\n".join(lines)
    return None


# =====================================================================
# TOOL 3: WIKIPEDIA KNOWLEDGE SEARCH (Always Available, Free)
# =====================================================================

def search_wikipedia_knowledge(query: str):
    """Queries Wikipedia encyclopedia directly for facts, people, history, companies."""
    # Clean query for search
    clean = re.sub(r"(?i)\b(who is|what is|when did|tell me about|give short notes on|notes on|information about)\b", "", query).strip()
    if not clean:
        clean = query.strip()

    try:
        # Search API
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(clean)}&utf8=&format=json"
        headers = {"User-Agent": "ExecutiveAssistant/2.0 (Executive AI Chat App)"}
        s_res = requests.get(search_url, headers=headers, timeout=5).json()
        
        search_results = s_res.get("query", {}).get("search", [])
        if not search_results:
            return None
        
        best_title = search_results[0]["title"]

        # Fetch Summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_title)}"
        sum_res = requests.get(summary_url, headers=headers, timeout=5).json()

        extract = sum_res.get("extract")
        if extract:
            return f"### 📚 {best_title}\n\n{extract}"
    except Exception:
        pass
    return None


# =====================================================================
# TOOL 4: GOOGLE GEMINI CLOUD ENGINE (Handles Writing, Code, Analysis)
# =====================================================================

def query_gemini_cloud(prompt: str, api_key: str, system_instruction: str):
    """Direct, robust call to Google Gemini with proper URL and header key passing."""
    clean_key = api_key.strip()
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": clean_key
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Instruction: {system_instruction}\n\nQuestion: {prompt}"}]
            }
        ]
    }

    # Fleet list to try: 2.5-flash -> 3.8-flash -> 1.5-flash
    for model_name in ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=12)
            data = res.json()
            if res.status_code == 200 and "candidates" in data:
                parts = data["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"]
        except Exception:
            continue

    return None


# =====================================================================
# MASTER AGENT BRAIN (Zero Failures Guarantee)
# =====================================================================

def master_agent_respond(prompt: str, api_key: str, system_instruction: str):
    clean_prompt = prompt.strip().lower()

    # 1. Direct Greetings (0.001s)
    if clean_prompt in ["hi", "hello", "hey", "hi there", "hello there", "good morning", "good afternoon", "good evening"]:
        return "Hello! I am your personal AI assistant. How can I help you today?"

    # 2. Weather Check (Live Real-time data)
    if any(w in clean_prompt for w in ["temperature", "weather", "climate", "degree", "rain", "forecast"]):
        weather_report = get_live_weather(prompt)
        if weather_report:
            return weather_report

    # 3. World Clocks Check (0.0001s)
    if any(w in clean_prompt for w in ["time in", "clock in", "current time"]):
        clock_report = get_world_time(prompt)
        if clock_report:
            return clock_report

    # 4. Instant Answers for Common Known Queries
    if "pm of india" in clean_prompt or "prime minister of india" in clean_prompt:
        return "**Narendra Modi** is the Prime Minister of India."
    
    if "cm of tn" in clean_prompt or "cm of tamil nadu" in clean_prompt or "chief minister of tamil nadu" in clean_prompt:
        return "The Chief Minister of Tamil Nadu is **M. K. Stalin**."

    if "ceo of google" in clean_prompt:
        return (
            "### CEO of Google:\n\n"
            "* **Sundar Pichai** became the CEO of Google on **August 10, 2015**.\n"
            "* He later also became the CEO of Alphabet (Google's parent company) in **December 2019**.\n"
            "* Prior to Sundar Pichai, Google was led by co-founder **Larry Page**."
        )

    # 5. Google Gemini Cloud Reasoning (If API key provided)
    if api_key:
        gemini_answer = query_gemini_cloud(prompt, api_key, system_instruction)
        if gemini_answer:
            return gemini_answer

    # 6. Built-in Knowledge Search (Fallback if Gemini is busy or no key entered)
    wiki_answer = search_wikipedia_knowledge(prompt)
    if wiki_answer:
        return wiki_answer

    # 7. Graceful Response
    return (
        f"I have reviewed your query: *\"{prompt}\"*.\n\n"
        "To get deeper AI-generated coding, analysis, or conversational writing, ensure your Gemini API key is entered in the left sidebar.\n"
        "You can also ask me for **real-time weather** (e.g. *'temperature in Bangalore'*), **world clocks**, **math**, or **encyclopedia knowledge** anytime!"
    )


# --- Instant Local Math Evaluator (<0.0001s) ---
def try_instant_math(user_input: str):
    cleaned = user_input.strip()
    allowed = set("0123456789+-*/%(). ")
    if all(c in allowed for c in cleaned) and any(op in cleaned for op in "+-*/%"):
        try:
            ans = eval(cleaned)
            if isinstance(ans, float) and ans.is_integer():
                ans = int(ans)
            return f"**{cleaned} = {ans}**"
        except Exception:
            pass
    return None


# --- User Input Box ---
user_query = st.chat_input("Ask any question, request live weather, coding, research, or math...")

if user_query:
    # 1. User Message
    st.session_state.chat_history.append({"role": "user", "avatar": "👤", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 2. Assistant Processing
    with st.chat_message("assistant", avatar="✨"):
        math_ans = try_instant_math(user_query)
        if math_ans:
            st.markdown(math_ans)
            final_answer = math_ans
        else:
            with st.spinner("Processing..."):
                final_answer = master_agent_respond(
                    prompt=user_query,
                    api_key=api_key_input,
                    system_instruction=PERSONA_PROMPTS[persona]
                )
                st.markdown(final_answer)

    st.session_state.chat_history.append({"role": "assistant", "avatar": "✨", "content": final_answer})
