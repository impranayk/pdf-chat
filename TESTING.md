# Test log: how each step was checked

Code shown in reels #31–#40. Every file here was run on a real laptop before it went into a video.

Setup (once):
- Install Ollama from ollama.com, then `ollama pull llama3.2` (2.0 GB)
- `pip install ollama`

## Sample document

`HR_Policy.pdf` is built by `make_hr_policy.py`: a 12-page FICTIONAL handbook for "Bluepeak Example Ltd".
Page 4 = annual leave (24 days); page 8 = expenses (claims within 30 days; parking free in Block B); page 9 = travel.

## Step 4: read the PDF (reel #34)

`step4_read_pdf.py` (pypdf). Real output, 2026-10-05:
```
12 pages
Bluepeak Example Ltd (fictional example for a tutorial)
Page 4
3. Annual Leave
Every full-time employee gets 24 days of paid annual leave each calendar year, plus
```
Note: the footer is extracted BEFORE the heading (PDF text comes out in drawing order).

## Step 5: text to numbers (reel #35)

`step5_embed.py`: one chunk per page (first 2 lines = footer, skipped), embedded with sentence-transformers
`all-MiniLM-L6-v2` (384 numbers; was already cached locally, so run with HF_HUB_OFFLINE=1). Real output, 2026-10-05:
```
12 chunks
384 numbers for page 4
[ 0.079 -0.016  0.039  0.056  0.035]
```
Page 4 chunk = 104 words. First run took ~1 min 49 s (mostly loading torch/the model).

## Step 6: store them (reel #36)

`step6_store.py` (chromadb 0.6.3, PersistentClient at `hr_db/`, our own embeddings passed in, so Chroma's
default embedder never downloads anything). `step6_check.py` reopens it in a NEW process.
Run with `HF_HUB_OFFLINE=1 ANONYMIZED_TELEMETRY=False`. Real output, 2026-10-05:
```
12 pieces saved in hr_db/
12 pieces still here
{'page': 4} 3. Annual Leave Every full-time employee gets
```
`hr_db/` = 1.9 MB. Store run ≈ 22 s.

## Step 7: find the right pieces (reel #37)

`step7_search.py`, real output 2026-10-05 for "How many vacation days do I get?" ("vacation" is NOT in the PDF):
```
page 4  distance 0.99
page 5  distance 1.04
page 9  distance 1.43
```
5 more questions, top-3 (page, distance):
- How many leave days do I get? → (4, 0.56) (5, 0.69) (2, 1.2)
- Where can I park my car? → (8, 1.64) (7, 1.75) (5, 1.79)
- Can I work from home? → (7, 0.84) (1, 1.44) (11, 1.53)
- How long do I have to submit a receipt? → (8, 1.29) (4, 1.33) (5, 1.53)  ← close call
- What if I lose my laptop? → (11, 1.3) (5, 1.78) (9, 1.8)

## Step 8: first real answer (reel #38)

`step8_answer.py` (top 3 pieces + prompt rules "use ONLY the context, say which page" and "say I don't know").
Real outputs 2026-10-05, 2 runs each:
- vacation days → "According to page 4, every full-time employee gets 24 days of paid annual leave each calendar year, plus public holidays." / "You get 24 days of paid annual leave each calendar year. [Page 4]"
- park my car → "According to page [page 8], parking is free for staff in Block B." / "Page 8. You can park your car for free in Block B."
- receipt → "You have to submit a receipt within 30 days of the expense. (Page 8)" / "According to page 8, expense claims must be filed within 30 days…"
- What does RAG mean? → "I don't know. There is no mention of "RAG" in the provided context." (both runs)
- Who is the CEO of Bluepeak? → "I don't know. There is no mention of the CEO…" / "I don't know. (page 1)"
Quirk: odd source formatting ("page [page 8]", a page cited on an "I don't know").

## Step 9: a web page (reel #39)

`app.py` (Streamlit 1.59.1, 68 lines). Start with `run_app.bat` (offline env vars, port 8790) or `streamlit run app.py`.
- Upload any PDF; falls back to HR_Policy.pdf. Index built in memory (Chroma EphemeralClient), cached per file.
- BUG FOUND + FIXED: collection named from the file name crashed on names like "My Policy (1).pdf"
  (Chroma ValueError). Now `doc-{zlib.crc32(name)}`.
- BUG FOUND + FIXED: first version labelled the source with the top search hit. For "Where can I park my car?"
  that gave page 7 (parking is on page 8). Fix: each page is labelled "[page N]" in the context, the model must end
  with "SOURCE: page N", and the app only shows it if that page was among the 3 searched. If the model leaves the
  line out, the app picks the searched page sharing the most words with the answer. No source on "I don't know".
- Test (Streamlit AppTest, 7 questions x 2 runs, llama3.2), 2026-10-05:
  - model-written SOURCE line alone: 9/14 right labels (5 missing lines, 1 source shown on "I don't know")
  - + "I don't know" check first: 10 exact, 4 missing lines, 0 wrong
  - + word-overlap fallback: 14/14 (pages 4, 8, 8, 7, 11; RAG and CEO questions -> "I don't know." with no source)
- Screenshots used in the reel: ai-reels/public/build/app_answer.jpg, app_dontknow.jpg.
- LIVE TEST 2026-10-06 (pdf-chat-pranay.streamlit.app, Groq openai/gpt-oss-20b): receipt question answered right
  ("within 30 days") but cited page 4. The prompt's example line "SOURCE: page 4" biased the model, and page 4 was
  among the 3 searched so the old check passed it. Fix: the app scores each searched page by shared words (4+ letters)
  with the answer and keeps the AI's page only if it is a top scorer; otherwise the top scorer. Rewording the example
  instead ("page <number>") made llama3.2 answer "I don't know" for parking, so the original wording stays.
  Local re-test after fix: 14/14.
- Online: `ask()` uses Groq (openai/gpt-oss-20b) when a GROQ_API_KEY secret is set, else local Ollama.
- Not yet tested through the UI: uploading a different PDF (the browser pane can't upload files).

## Step 3: your first AI call (reel #33)

`step3_first_call.py`, run 2026-10-05 with Ollama 0.35.1, llama3.2, ollama-python 0.5.3, ~10 s per call.

The vague question "Explain RAG in one sentence." got a confident, made-up answer on all 3 runs:
1. "RAG (Red Adenoma and Ganglioneuroma) syndrome is a rare genetic disorder…"
2. "RAG (Reassurance, Affirmation, and Goal) is a therapy approach…"
3. "RAG (Residual Activity Guideline) is a quality control (QC) guideline from the US Food and Drug Administration…"

`step3_clear.py` asks "What is retrieval-augmented generation? One sentence." and was correct on both runs, e.g.
"Retrieval-Augmented Generation (RAG) is a text generation technique that combines large language models with retrieval algorithms…"
