# Chat with any PDF

Upload a PDF, ask it questions, and get answers that name the page they came from.
If the answer isn't in the PDF, it says "I don't know" instead of making one up.

Built step by step, with free tools only, in the **Build with me** reel series (#31–#40) on
Instagram [@ai.with.pranay](https://www.instagram.com/ai.with.pranay/) and [drpranayjha.com](https://drpranayjha.com).

## How it works (RAG in 4 steps)

1. **Read**: pypdf pulls the text out of each page.
2. **Embed**: `all-MiniLM-L6-v2` turns each page into 384 numbers that capture its meaning.
3. **Search**: Chroma finds the 3 pages closest in meaning to your question.
4. **Answer**: an AI model answers using only those pages, and ends with `SOURCE: page N`.
   The app shows that page only if it was one of the 3 searched.

## Run it on your laptop (free, offline)

1. Install [Ollama](https://ollama.com), then:
   ```
   ollama pull llama3.2
   ```
2. Install the Python packages (Python 3.10+):
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   streamlit run app.py
   ```

It opens with `HR_Policy.pdf`, a made-up 12-page handbook for a fictional company. Try:
- "How many vacation days do I get?" (page 4)
- "Where can I park my car?" (page 8)
- "Who is the CEO?" (not in the PDF, so: "I don't know.")

## Put it online (free)

Online there is no Ollama, so the app uses [Groq](https://console.groq.com)'s free API instead.

1. Fork this repo.
2. Get a free API key at console.groq.com.
3. On [share.streamlit.io](https://share.streamlit.io), create an app from your fork with `app.py` as the main file.
4. Under **Advanced settings → Secrets**, add:
   ```
   GROQ_API_KEY = "your-key-here"
   ```
5. Deploy. Never put the key in the code or commit it.

## The step-by-step files

| File | Step |
|---|---|
| `step3_first_call.py`, `step3_clear.py` | First call to a local AI model |
| `step4_read_pdf.py` | Read the PDF |
| `step5_embed.py` | Turn text into numbers |
| `step6_store.py`, `step6_check.py` | Store them in a vector database |
| `step7_search.py` | Find the right pages |
| `step8_answer.py` | First real answer |
| `app.py` | The web app |
| `make_hr_policy.py` | Builds the sample PDF |

`TESTING.md` has the real outputs from every step, including the bugs found along the way.
