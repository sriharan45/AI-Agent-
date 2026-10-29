# 🤖 1st Project: My First AI Agent

Welcome to your first real AI project! This project demonstrates how an AI agent works using Python and the Google Gemini API.

---

## 📂 Project Structure

* **`agent.py`**: The complete agent script. It defines tools (`calculate`, `get_current_time`, `save_note`) and shows how an AI brain decides which tool to use.
* **`my_notes.txt`**: Created automatically when the agent uses its `save_note` tool.

---

## 🚀 How to Run This on Your Laptop (3 Easy Steps)

### Step 1: Install Python
1. Go to [python.org/downloads](https://www.python.org/downloads/) and download Python for Windows.
2. When the installer starts, **make sure to check the box: `[✓] Add python.exe to PATH`** (this is very important!).
3. Click **Install Now**.

### Step 2: Install the Gemini Library
Open PowerShell or Command Prompt, and type:
```powershell
pip install google-generativeai
```

### Step 3: Get a Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key** (it is free for personal/developer use).
3. Copy your key, and in your terminal run:
   ```powershell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```

### Step 4: Run the Agent!
In your terminal, navigate to this project folder and run:
```powershell
python agent.py
```

*(Note: Even without an API key yet, running `python agent.py` will launch in Demo Mode so you can see the reasoning loop in action right away!)*
