import streamlit as st
import datetime
import re
import random
from zoneinfo import ZoneInfo

# --- Page Configuration ---
st.set_page_config(
    page_title="I am here to help you",
    page_icon="👋",
    layout="centered"
)

# --- Professional, Calming Glassmorphism Theme (Black & Sky Blue Glow) ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Deep Midnight Ambient Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #0c1a30 0%, #040711 70%, #02040a 100%) !important;
        color: #e0f2fe !important;
    }

    /* Ambient glow at the top */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 250px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* Title Styling: Gradient Sky Blue */
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7dd3fc 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        margin-bottom: 1.5rem;
    }

    /* Quick Suggestion Pills */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 1.5rem;
    }

    .pill {
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #7dd3fc;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }

    /* Chat Messages - Elevated Modern Glass Cards */
    [data-testid="stChatMessage"] {
        background: rgba(11, 20, 38, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(56, 189, 248, 0.35) !important;
    }

    /* Chat Message Text */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div {
        color: #e2e8f0 !important;
        font-size: 1.02rem !important;
        line-height: 1.6 !important;
    }

    /* Result highlight cards */
    .result-card {
        background: rgba(14, 165, 233, 0.08);
        border-left: 3px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        margin: 6px 0;
        color: #f0f9ff;
    }

    /* Calculation bold accent */
    .math-result {
        font-size: 1.25rem;
        font-weight: 600;
        color: #38bdf8;
        letter-spacing: 0.5px;
    }

    /* Time badge */
    .time-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #7dd3fc;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        margin-right: 6px;
    }

    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
    }

    [data-testid="stChatInput"] textarea {
        background: rgba(11, 20, 38, 0.85) !important;
        color: #f0f9ff !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-size: 0.98rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* Hide Streamlit default deploy button & footer header margins */
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Header Section with Welcoming Human Avatar ---
st.markdown("""
<div style="padding-top: 10px;">
    <div class="main-title">
        <span>👋</span> I am here to help you
    </div>
    <div class="sub-title">
        Ask for world times, facts, or notes
    </div>
</div>
""", unsafe_allow_html=True)

# --- World Timezone Database ---
TIMEZONE_REGIONS = {
    # United States / America
    "us": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "usa": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "america": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "united states": [("New York (Eastern)", "America/New_York"), ("Los Angeles (Pacific)", "America/Los_Angeles")],
    "new york": [("New York (Eastern)", "America/New_York")],
    "california": [("California (Pacific)", "America/Los_Angeles")],
    "los angeles": [("Los Angeles (Pacific)", "America/Los_Angeles")],
    "chicago": [("Chicago (Central)", "America/Chicago")],
    "texas": [("Texas (Central)", "America/Chicago")],

    # India
    "india": [("India (IST)", "Asia/Kolkata")],
    "ist": [("India (IST)", "Asia/Kolkata")],
    "delhi": [("New Delhi", "Asia/Kolkata")],
    "mumbai": [("Mumbai", "Asia/Kolkata")],
    "chennai": [("Chennai", "Asia/Kolkata")],
    "bangalore": [("Bengaluru", "Asia/Kolkata")],

    # UK & Europe
    "uk": [("London (UK)", "Europe/London")],
    "united kingdom": [("London (UK)", "Europe/London")],
    "london": [("London (UK)", "Europe/London")],
    "england": [("London (UK)", "Europe/London")],
    "france": [("Paris (France)", "Europe/Paris")],
    "paris": [("Paris (France)", "Europe/Paris")],
    "germany": [("Berlin (Germany)", "Europe/Berlin")],
    "berlin": [("Berlin (Germany)", "Europe/Berlin")],
    "italy": [("Rome (Italy)", "Europe/Rome")],
    "rome": [("Rome (Italy)", "Europe/Rome")],
    "spain": [("Madrid (Spain)", "Europe/Madrid")],
    "russia": [("Moscow (Russia)", "Europe/Moscow")],

    # Middle East & Asia
    "dubai": [("Dubai (UAE)", "Asia/Dubai")],
    "uae": [("Dubai (UAE)", "Asia/Dubai")],
    "singapore": [("Singapore", "Asia/Singapore")],
    "japan": [("Tokyo (Japan)", "Asia/Tokyo")],
    "tokyo": [("Tokyo (Japan)", "Asia/Tokyo")],
    "china": [("Beijing (China)", "Asia/Shanghai")],
    "beijing": [("Beijing (China)", "Asia/Shanghai")],
    "hong kong": [("Hong Kong", "Asia/Hong_Kong")],
    "korea": [("Seoul (South Korea)", "Asia/Seoul")],
    "seoul": [("Seoul (South Korea)", "Asia/Seoul")],
    "saudi": [("Riyadh (Saudi Arabia)", "Asia/Riyadh")],
    "qatar": [("Doha (Qatar)", "Asia/Qatar")],

    # Australia & Canada
    "australia": [("Sydney (Australia)", "Australia/Sydney")],
    "sydney": [("Sydney (Australia)", "Australia/Sydney")],
    "melbourne": [("Melbourne (Australia)", "Australia/Melbourne")],
    "canada": [("Toronto (Canada)", "America/Toronto"), ("Vancouver (Canada)", "America/Vancouver")],
    "toronto": [("Toronto (Canada)", "America/Toronto")],
    
    # Universal UTC
    "utc": [("UTC", "UTC")],
    "gmt": [("GMT", "UTC")],
}

# --- Mind-Refreshing Facts Collection ---
FUN_FACTS = [
    "✨ Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
    "🌌 There are more trees on Earth (about 3 trillion) than there are stars in the Milky Way galaxy (about 100–400 billion).",
    "🌊 An octopus has three hearts, nine brains, and blue blood!",
    "🚀 A day on Venus is longer than a year on Venus. It takes Venus 243 Earth days to rotate once, but only 225 Earth days to travel around the Sun.",
    "🌿 When you take a deep breath, about 20% of the oxygen you inhale is used directly by your brain to keep you sharp and relaxed.",
    "🐬 Dolphins have names for each other—they use unique signature whistles to call out to specific friends.",
    "🪐 Saturn's moon Titan has a thick atmosphere and liquid methane lakes—you could fly there just by flapping artificial wings strapped to your arms!",
    "☕ The aroma of fresh coffee alone can alter the activity of certain genes in the brain, reducing the effects of stress."
]

# --- Direct Time Helper (No Robotic Labels) ---
def get_clean_world_time(prompt: str) -> str:
    clean_prompt = prompt.lower()
    words = set(re.findall(r'\b[a-zA-Z]+\b', clean_prompt))
    matched_entries = []

    for key, tz_list in TIMEZONE_REGIONS.items():
        if " " in key:
            if key in clean_prompt:
                matched_entries.extend(tz_list)
        else:
            if key in words:
                matched_entries.extend(tz_list)

    if matched_entries:
        seen = set()
        unique_matches = []
        for label, tz_name in matched_entries:
            if label not in seen:
                seen.add(label)
                unique_matches.append((label, tz_name))

        lines = []
        for label, tz_name in unique_matches:
            try:
                now = datetime.datetime.now(ZoneInfo(tz_name))
                time_str = now.strftime("%A, %I:%M %p (%B %d)")
                lines.append(f"• **{label}**: {time_str}")
            except Exception:
                pass
        return "\n\n".join(lines)

    # Local fallback
    local_now = datetime.datetime.now()
    return f"Right now it is **{local_now.strftime('%A, %I:%M %p (%B %d)')}**."

# --- Direct Math Calculation (Clean '4 - 3 = 1' without tool labels) ---
def clean_calculate(expression: str) -> str:
    try:
        allowed = set("0123456789+-*/(). ")
        if all(c in allowed for c in expression):
            answer = eval(expression)
            # Format clean decimals if needed
            if isinstance(answer, float) and answer.is_integer():
                answer = int(answer)
            return f"**{expression.strip()} = {answer}**"
        return "I can calculate that once you provide numbers and symbols (e.g., 25 * 4)."
    except Exception:
        return "Couldn't solve that math expression. Try something like 45 * 12."

# --- Direct Note Saver ---
def clean_save_note(note_text: str) -> str:
    with open("my_notes.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {note_text}\n")
    return f"Saved to your notes: *\"{note_text}\"*"

# --- Agent Responder (Human, Friendly & Crisp) ---
def agent_respond(prompt: str) -> str:
    lower_prompt = prompt.lower().strip()

    # 1. Math Intent (Check pure math or calculation words)
    is_math = bool(re.search(r'\d+\s*[\+\-\*\/]\s*\d+', prompt)) or any(w in lower_prompt for w in ["calculate", "multiply", "divide", "plus", "minus"])
    if is_math:
        expr = "".join([c for c in prompt if c in "0123456789+-*/. "]).strip()
        if expr:
            return clean_calculate(expr)

    # 2. Time Intent
    if any(w in lower_prompt for w in ["time", "clock", "hour", "timing"]):
        return get_clean_world_time(prompt)

    # 3. Facts Intent
    if any(w in lower_prompt for w in ["fact", "facts", "refresh", "knowledge", "tell me something"]):
        return random.choice(FUN_FACTS)

    # 4. Note Saving Intent
    if any(w in lower_prompt for w in ["note", "remember", "save note", "save"]):
        clean_note = prompt
        for keyword in ["save note", "save", "remember", "write down"]:
            clean_note = re.sub(rf"(?i)\b{keyword}\b[:\s]*", "", clean_note)
        clean_note = clean_note.strip()
        if clean_note:
            return clean_save_note(clean_note)

    # 5. Welcoming General Conversation
    return (
        "Hello! I am ready to help. Here are a few things you can ask me:\n\n"
        "• **Time:** *'What is the time in America?'* or *'Time in Dubai'*\n"
        "• **Math:** *'25 * 4'* or *'4 - 3'*\n"
        "• **Facts:** *'Tell me a fact'*\n"
        "• **Notes:** *'Save note: Call John at 4 PM'*"
    )

# --- Session Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "avatar": "👋",
            "content": "Hi there! I am here to help you. What would you like to check today?"
        }
    ]

# Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar", "👋" if msg["role"] == "assistant" else "👤")):
        st.markdown(msg["content"])

# --- Chat Input ---
user_input = st.chat_input("Ask for world times, facts, or notes...")

if user_input:
    # 1. User Message with User Avatar
    st.session_state.messages.append({"role": "user", "avatar": "👤", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # 2. Assistant Response with Friendly Wave Avatar
    with st.chat_message("assistant", avatar="👋"):
        reply = agent_respond(user_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "avatar": "👋", "content": reply})
