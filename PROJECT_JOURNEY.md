# Startup Blueprint Generator Agent — The Journeyy

---

## 1. The start

The goal: turn a plain-language startup idea into a full business blueprint, using IBM's AI tools. Solo build, tight time limit, and internet that's genuinely expensive to burn through — that last part ended up shaping almost every decision that followed.

---

## 2. First try: Langflow (didn't work out)

The first plan was to build a proper RAG pipeline visually in Langflow: load documents, split them into chunks, turn them into embeddings with watsonx.ai, store them in a Chroma vector database, retrieve the relevant ones per query, and feed all of that into Granite. This is the "textbook correct" way to do retrieval-augmented generation, which is why it was the first attempt.

It stalled out for a few reasons:
- Langflow Desktop took a long time to even finish launching the first time (it has to unpack its own Python backend on first run).
- Installing it via `pip install langflow` failed outright on Python 3.13 — pip couldn't find a matching version.
- Even ignoring the errors, the sheer size of everything it needed to download (LangChain, ChromaDB, embedding libraries, and so on) was a real cost given how limited and expensive the internet was.

Nothing usable came out of this attempt. The time and data spent here didn't come back, but the IBM Cloud/watsonx.ai project and credentials set up during this phase carried over directly into the next attempt.

---

## 3. What actually got built: a Flask app

Instead of the visual pipeline, the working version is a small Flask app (`app.py`) that talks to `ibm-watsonx-ai` directly.

Here's what happens when someone uses it:
1. They open the page — Flask serves `templates/index.html`, styled by `static/style.css`.
2. They type a startup idea into a textarea and hit **Generate Blueprint**.
3. `static/script.js` shows a quick "Generating Blueprint..." message, then sends the idea to the backend as a `POST /generate` request.
4. `app.py` builds one big prompt: the idea, instructions on which of 19 possible blueprint sections to include (only the relevant ones, aiming for 500–900 words), a block of reference facts, and some ground rules — don't invent schemes or numbers, and politely refuse anything unrelated to startups.
5. That whole prompt goes to `ibm/granite-4-h-small` with fairly conservative generation settings (greedy decoding, low temperature) so the output stays consistent rather than creative.
6. The response comes back as plain text and gets displayed as-is in the browser.

Credentials (`API_KEY`, `PROJECT_ID`, `URL`) live in a `.env` file, read through `config.py` — never hardcoded in `app.py`.

**Worth being upfront about:** this isn't real retrieval-augmented generation. There's no embedding step, no vector database, nothing searched per query. It's the same fixed block of facts (Startup India's SISFS scheme, the 9-part Business Model Canvas, a go-to-market framework, common funding sources) pasted into every single prompt. That's a perfectly reasonable way to ground a model's output, it's just not RAG in the strict sense — more like giving the model a cheat sheet every time rather than letting it look things up. Adding real retrieval later would be a natural next step, not a rebuild.

---

## 4. The UI

`templates/index.html`, `static/style.css`, and `static/script.js` together are the actual, only frontend — fully connected to the backend, nothing mocked or disconnected sitting alongside it.

It's a simple single page: a purple-to-cyan gradient background, two frosted-glass cards (one for the idea input, one for the output), and the generated blueprint shows up as plain formatted text once it's ready.

---

## 5. Where deployment stands

Not deployed yet — it only runs locally. `requirements.txt` already includes `gunicorn`, which is a hint that deployment was on the radar even if it hasn't happened. A separate deployment plan lays out the options (Render, PythonAnywhere, IBM Cloud Code Engine) with tradeoffs for each.

---

## 6. What's actually been confirmed working

- The full flow — typing an idea, hitting generate, getting a real Granite response back — works locally.
- The model picks a relevant subset of the 19 possible sections rather than dumping all of them every time.
- Numbers and scheme names in the output match the reference facts rather than being made up, on the samples checked so far.

---

## 7. Future Enhancements

- Add real retrieval (embeddings + vector search) instead of the fixed reference block.
- Actually deploy it somewhere public.
- Add automated tests — right now it's just a manual connectivity script and spot-checking outputs by hand.
- Handle multiple users at once and add proper error handling beyond a basic try/catch.
- Actually test the "politely refuse unrelated questions" behavior instead of just trusting the prompt.
- Run a broader, more structured check of output quality across many different startup ideas, not just a handful.
