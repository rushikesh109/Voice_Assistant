# Voice Assistant using Gemini API (Wake Word: Alexa)

## How to Use

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your Gemini API key:**
   Open `voice_assistant_alexa.py` and replace:
   ```python
   genai.configure(api_key="YOUR_GEMINI_API_KEY")
   ```

3. **Run the assistant:**
   ```bash
   python voice_assistant_alexa.py
   ```

4. **Talk to it!**
   Say: `Alexa, what’s the weather today?`
   Say: `That's all` to end the session.

---

## Dependencies

Listed in `requirements.txt`. Install with:

```bash
pip install -r requirements.txt
```

---

## Requirements

- Python 3.7+
- Microphone
- Speaker output
- Internet connection

Tested on Windows and Linux laptops.
