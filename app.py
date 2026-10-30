import streamlit as st
import datetime
import os
import re
import random
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
        placeholder="Paste your AI Studio key...",
        help="Optional: Paste your key from aistudio.google.com to power custom unbounded generations."
    )

    if api_key_input:
        st.success("✅ Gemini Engine: Connected")
    else:
        st.info("💡 **Tip:** Add `GEMINI_API_KEY` into Streamlit Cloud Secrets so all visitors get full cloud AI automatically!")

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

    st.markdown("---")
    st.markdown("📏 **Constraint:** Strictly under 100 words")
    st.markdown("🌤️ **Live Weather:** Active (Filtered by population)")
    st.markdown("🕒 **Global Clocks:** Active (Delhi, Chennai, US, etc.)")
    st.markdown("🧠 **Mind-Refreshing Facts:** Active")
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
st.markdown('<div class="hero-subtitle">Ask anything — facts, weather, world times, geography, coding, or math. Answers concise and under 100 words.</div>', unsafe_allow_html=True)

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
# HELPER: ENFORCE UNDER 100 WORDS
# =====================================================================

def enforce_under_100_words(text: str) -> str:
    """Guarantees the output is strictly concise and under 100 words."""
    words = text.strip().split()
    if len(words) <= 100:
        return text.strip()
    
    shortened = " ".join(words[:90])
    last_period = max(shortened.rfind('.'), shortened.rfind('!'), shortened.rfind('?'))
    if last_period > 60:
        return shortened[:last_period + 1]
    return shortened + "..."


# =====================================================================
# MIND-REFRESHING FACTS & INSPIRING CONTENT
# =====================================================================

CURATED_FACTS = [
    "✨ **Honey never spoils:** Archaeologists excavating ancient Egyptian tombs found 3,000-year-old pots of honey that are still completely edible due to its low moisture and acidic pH.",
    "🌌 **Trees vs Stars:** Earth has an estimated 3 trillion trees, which is vastly more than the 100 to 400 billion stars in our entire Milky Way galaxy.",
    "🐙 **Three Hearts:** An octopus possesses three hearts, nine brains (one central brain and one in each arm), and copper-based blue blood.",
    "🪐 **Venusian Days:** A single day on Venus (243 Earth days to rotate once) is longer than an entire Venusian year (225 Earth days to complete an orbit around the Sun).",
    "🗼 **Growing Tower:** The Eiffel Tower expands up to 15 centimeters (6 inches) taller during hot summer days because metal expands with heat.",
    "🐬 **Dolphin Names:** Dolphins develop unique signature whistles that act just like names to address and call specific members of their pod.",
    "🌿 **Brain Power:** Although the human brain accounts for only about 2% of total body weight, it consumes over 20% of the body's daily oxygen and energy."
]

CURATED_JOKES = [
    "😄 Why do programmers prefer dark mode? Because light attracts bugs!",
    "😄 Why did the Python programmer wear glasses? Because they couldn't C#.",
    "😄 There are 10 types of people in the world: those who understand binary, and those who don't."
]


# =====================================================================
# TOOL 1: WORLD CLOCKS ENGINE
# =====================================================================

INDIAN_REGIONS = [
    "delhi", "new delhi", "chennai", "mumbai", "kolkata", "bengaluru", "bangalore", 
    "hyderabad", "ahmedabad", "pune", "jaipur", "lucknow", "kanpur", "nagpur", 
    "indore", "coimbatore", "madurai", "trichy", "salem", "kerala", "kochi", 
    "patna", "goa", "chandigarh", "bhopal", "tamil nadu", "tamilnadu", "india"
]

GLOBAL_CITIES = {
    "new york": ("New York (Eastern Time)", "America/New_York"),
    "los angeles": ("Los Angeles (Pacific Time)", "America/Los_Angeles"),
    "california": ("California (Pacific Time)", "America/Los_Angeles"),
    "chicago": ("Chicago (Central Time)", "America/Chicago"),
    "texas": ("Texas (Central Time)", "America/Chicago"),
    "london": ("London (UK)", "Europe/London"),
    "uk": ("London (UK)", "Europe/London"),
    "england": ("London (UK)", "Europe/London"),
    "dubai": ("Dubai (UAE)", "Asia/Dubai"),
    "uae": ("Dubai (UAE)", "Asia/Dubai"),
    "tokyo": ("Tokyo (Japan)", "Asia/Tokyo"),
    "japan": ("Tokyo (Japan)", "Asia/Tokyo"),
    "singapore": ("Singapore", "Asia/Singapore"),
    "sydney": ("Sydney (Australia)", "Australia/Sydney"),
    "australia": ("Sydney (Australia)", "Australia/Sydney"),
    "paris": ("Paris (France)", "Europe/Paris"),
    "france": ("Paris (France)", "Europe/Paris"),
    "berlin": ("Berlin (Germany)", "Europe/Berlin"),
    "germany": ("Berlin (Germany)", "Europe/Berlin"),
    "toronto": ("Toronto (Canada)", "America/Toronto"),
    "canada": ("Toronto (Canada)", "America/Toronto")
}

def check_time_query(query: str):
    clean_q = query.lower()
    is_time_ask = any(w in clean_q for w in ["time", "clock", "timing", "hour"])
    if not is_time_ask:
        return None

    # Indian Cities & States
    for region in INDIAN_REGIONS:
        if region in clean_q:
            now = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
            time_str = now.strftime("%A, %I:%M %p (%B %d, %Y)")
            return f"The current time in **{region.title()} (IST)** is **{time_str}**."

    # Global Cities
    for city_key, (label, tz_name) in GLOBAL_CITIES.items():
        if city_key in clean_q:
            now = datetime.datetime.now(ZoneInfo(tz_name))
            time_str = now.strftime("%A, %I:%M %p (%B %d, %Y)")
            return f"The current time in **{label}** is **{time_str}**."

    # Generic local time
    if any(phrase in clean_q for phrase in ["what is the time", "what is the current time", "time now", "current time"]):
        now = datetime.datetime.now()
        return f"The current local time is **{now.strftime('%A, %I:%M %p (%B %d, %Y)')}**."

    return None


# =====================================================================
# TOOL 2: LIVE REAL-TIME WEATHER (Population-Sorted)
# =====================================================================

WEATHER_CODES = {
    0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
    45: "Foggy 🌫️", 51: "Light drizzle 🌦️", 61: "Rain 🌧️", 71: "Snow ❄️", 80: "Showers 🌦️", 95: "Thunderstorm ⛈️"
}

def get_live_weather(query: str):
    clean_q = query.lower()
    city = None
    known_cities = {
        "bangalore": "Bengaluru", "bengaluru": "Bengaluru", "chennai": "Chennai", 
        "delhi": "New Delhi", "mumbai": "Mumbai", "kolkata": "Kolkata", "hyderabad": "Hyderabad",
        "new york": "New York", "london": "London", "dubai": "Dubai", "tokyo": "Tokyo", 
        "paris": "Paris", "berlin": "Berlin", "sydney": "Sydney", "toronto": "Toronto", "singapore": "Singapore"
    }
    
    for c_key, c_name in known_cities.items():
        if c_key in clean_q:
            city = c_name
            break

    if not city:
        match = re.search(r"(?:temperature|weather|climate)\s+(?:in|of|at)\s+([a-zA-Z\s]+)", clean_q)
        if match:
            city = match.group(1).replace("now", "").replace("today", "").strip()

    if not city:
        return None

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=5).json()
        results = geo_res.get("results")
        if not results:
            return None
        
        loc = max(results, key=lambda x: x.get("population", 0))
        lat, lon = loc["latitude"], loc["longitude"]
        city_name = loc.get("name", city.title())
        country = loc.get("country", "")
        admin = loc.get("admin1", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
        w_res = requests.get(weather_url, timeout=5).json()
        current = w_res.get("current", {})
        temp_c = current.get("temperature_2m")
        temp_f = round((temp_c * 9/5) + 32, 1) if temp_c is not None else None
        code = current.get("weather_code", 0)
        condition = WEATHER_CODES.get(code, "Clear")
        humidity = current.get("relative_humidity_2m", "N/A")

        location_display = f"{city_name}, {admin}, {country}" if admin else f"{city_name}, {country}"

        return (
            f"The current temperature in **{location_display}** is **{temp_c}°C** ({temp_f}°F). "
            f"Conditions are **{condition}** with **{humidity}%** humidity."
        )
    except Exception:
        return None


# =====================================================================
# TOOL 3: ACCURATE CURATED KNOWLEDGE & RESPONSES
# =====================================================================

def check_curated_facts(prompt: str):
    clean = prompt.lower().strip()

    # 1. Greetings (All variations: hi, hy, hii, heyy, namaste, etc.)
    greetings = ["hi", "hy", "hii", "hiii", "hey", "heyy", "hello", "yo", "sup", "namaste", "vanakkam", "halo"]
    if clean in greetings or any(clean.startswith(g) for g in ["good morning", "good afternoon", "good evening", "good day"]):
        return "Hello! I am your personal AI assistant. How can I help you today?"

    # 2. Who are you / Abilities
    if any(phrase in clean for phrase in ["who are you", "what are you", "what can you do", "introduce yourself"]):
        return (
            "I am an Executive AI Assistant created by Sriharan. I can provide real-time world clocks, "
            "live weather for any city, precision arithmetic, facts, and concise knowledge in under 100 words."
        )

    # 3. How are you
    if "how are you" in clean:
        return "I am functioning smoothly and ready to assist you! What can I solve or look up for you today?"

    # 4. Facts (fact for the day, tell me a fact, random fact, etc.)
    if any(w in clean for w in ["fact", "facts", "knowledge"]):
        return random.choice(CURATED_FACTS)

    # 5. Jokes
    if any(w in clean for w in ["joke", "jokes"]):
        return random.choice(CURATED_JOKES)

    # 6. Districts in Tamil Nadu
    if ("district" in clean or "districts" in clean) and ("tamil nadu" in clean or "tamilnadu" in clean or "tn" in clean):
        return (
            "Tamil Nadu has **38 districts**: Ariyalur, Chengalpattu, Chennai, Coimbatore, Cuddalore, "
            "Dharmapuri, Dindigul, Erode, Kallakurichi, Kanchipuram, Kanyakumari, Karur, Krishnagiri, "
            "Madurai, Mayiladuthurai, Nagapattinam, Namakkal, Nilgiris, Perambalur, Pudukkottai, "
            "Ramanathapuram, Ranipet, Salem, Sivaganga, Tenkasi, Thanjavur, Theni, Thoothukudi, "
            "Tiruchirappalli, Tirunelveli, Tirupathur, Tiruppur, Tiruvallur, Tiruvannamalai, Tiruvarur, "
            "Vellore, Viluppuram, and Virudhunagar."
        )

    # 7. Tamil Nadu Country / Geography
    if "tamilnadu" in clean or "tamil nadu" in clean:
        if any(w in clean for w in ["country", "which country", "where is"]):
            return "**Tamil Nadu** is a state located in the southern part of **India**."

    # 8. States of India
    if "states in india" in clean or "states of india" in clean:
        return (
            "India has **28 states**: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, "
            "Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, "
            "Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, "
            "Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, and West Bengal."
        )

    # 9. Google CEO
    if "ceo of google" in clean:
        return (
            "**Sundar Pichai** became the CEO of Google on **August 10, 2015**, and later also became "
            "the CEO of Google's parent company, **Alphabet**, in **December 2019**."
        )

    # 10. Actor Vijay
    if "actor vijay" in clean or ("vijay" in clean and "now" in clean):
        return (
            "Actor Vijay launched his political party, **Tamilaga Vettri Kazhagam (TVK)**, in 2024. "
            "He has transitioned from mainstream cinema to focus full-time on his political career in Tamil Nadu."
        )

    # 11. Tamil Nadu CM
    if "tamilnadu cm" in clean or "tamil nadu cm" in clean or "cm of tn" in clean or "cm of tamil nadu" in clean:
        return "**M. K. Stalin** is the Chief Minister of Tamil Nadu, leading the DMK government since May 2021."

    # 12. Freshers
    if "fresher" in clean and ("problem" in clean or "challenges" in clean or "job" in clean):
        return (
            "Key challenges for fresh graduates in India include:\n"
            "1. **Skill Mismatch:** Theory vs. hands-on industry requirements.\n"
            "2. **Competition:** High applicant volumes for entry-level positions.\n"
            "3. **Experience Paradox:** Entry-level openings requiring prior experience.\n"
            "4. **Campus Hiring Cycles:** Selective intake across tech sectors."
        )

    # 13. Literacy Rate
    if "literacy" in clean and "india" in clean:
        return (
            "According to official National Sample Survey (PLFS) data, India's overall literacy rate "
            "is approximately **80.9%** (around 90% in urban areas and 77% in rural areas), with male "
            "literacy at ~88% and female literacy at ~81%."
        )

    return None


# =====================================================================
# TOOL 4: GOOGLE GEMINI CLOUD LLM
# =====================================================================

def query_gemini_cloud(prompt: str, api_key: str):
    """Calls Google Gemini with strict <100 words prompt."""
    clean_key = api_key.strip()
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Answer concisely, factually, and strictly under 80 words:\n\n{prompt}"}]
            }
        ]
    }

    for model_name in ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            data = res.json()
            if res.status_code == 200 and "candidates" in data:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return enforce_under_100_words(text)
        except Exception:
            continue
    return None


# --- Instant Math Evaluator (<0.0001s) ---
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


# =====================================================================
# MASTER AGENT BRAIN
# =====================================================================

def master_agent_respond(prompt: str, api_key: str):
    # 1. Math Check (0.0001s)
    math_ans = try_instant_math(prompt)
    if math_ans:
        return math_ans

    # 2. Curated Direct Facts & Greetings (Handles hy/hi, facts, jokes, states, districts, CM, etc.)
    curated = check_curated_facts(prompt)
    if curated:
        return enforce_under_100_words(curated)

    # 3. Live Weather Check (Population-sorted)
    if any(w in prompt.lower() for w in ["temperature", "weather", "climate", "degree"]):
        weather_ans = get_live_weather(prompt)
        if weather_ans:
            return weather_ans

    # 4. World Time Check (Handles Delhi, Chennai, Bangalore, US, UK, etc.)
    time_ans = check_time_query(prompt)
    if time_ans:
        return time_ans

    # 5. Google Gemini Cloud LLM (If API Key is provided)
    if api_key:
        gemini_ans = query_gemini_cloud(prompt, api_key)
        if gemini_ans:
            return gemini_ans

    # 6. Fallback Response (Clean & Under 100 Words)
    return enforce_under_100_words(
        f"I am ready to help with '{prompt}'. Ask me for **daily facts**, **live weather**, "
        "**world clocks**, **geography**, or **math**, and I will answer directly in under 100 words!"
    )


# --- User Input Box ---
user_query = st.chat_input("Ask any question, request facts, live weather, time, or math...")

if user_query:
    # 1. User Message
    st.session_state.chat_history.append({"role": "user", "avatar": "👤", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # 2. Assistant Processing
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Processing..."):
            final_answer = master_agent_respond(user_query, api_key_input)
            st.markdown(final_answer)

    st.session_state.chat_history.append({"role": "assistant", "avatar": "✨", "content": final_answer})
