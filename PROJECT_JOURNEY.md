# Startup Blueprint Generator Agent — Project Journey (Transparent Account)

This document records what was actually built, what was tried and abandoned, and what the current prototype does and does not do. Written for accuracy over presentation.

---

## 1. Brief and constraints

Built for IBM SkillsBuild University, Problem Statement #20: a RAG-powered agent that converts a plain-language startup idea into a structured business blueprint (Business Model Canvas, budget estimate, go-to-market plan, relevant government schemes, investor categories), grounded in real data rather than model guesswork. Mandatory technology: IBM Cloud Lite services / IBM Granite.

Working constraints: solo build, no prior experience with IBM Cloud or AI orchestration tooling, a hard time budget, and limited/costly internet bandwidth — the last constraint ended up shaping the final architecture more than any design preference did.

---

## 2. First approach: Langflow-based RAG pipeline (abandoned)

The original plan was a visual RAG pipeline in Langflow: document loader → text splitter → IBM watsonx.ai embeddings → Chroma vector store → retriever → prompt → IBM watsonx.ai Granite LLM → output. This is the architecturally "correct" way to build retrieval-augmented generation, and was chosen first for that reason.

It was abandoned after:
- Langflow Desktop took an extended time to complete first launch (it unpacks a bundled Python backend on first run).
- `pip install langflow` failed against the system's Python 3.13 install with a "no matching distribution" error, traced to a version-compatibility gap between the installed pip resolver and the package's supported range.
- The combined dependency tree (LangChain ecosystem, ChromaDB, embedding backends, etc.) represented a large download and disk footprint, which was a real cost given constrained/expensive internet access, not just an inconvenience.

No working pipeline was produced through this path. Time and bandwidth spent here were not recovered, but the watsonx.ai project, credentials, and reference documents created during this phase were reused directly in the next approach.

---

## 3. Second approach: lightweight custom Flask app (current, working, local-only)

Instead of a visual orchestrator, the working prototype is a small Flask web application that calls the `ibm-watsonx-ai` Python SDK directly.

**Request flow:**
1. Browser loads `GET /` → serves `templates/index.html`, styled by `static/style.css`.
2. User enters a startup idea and submits the form.
3. `static/script.js` sends an asynchronous `POST /generate` request with the idea as JSON.
4. `app.py` receives the request, combines the user's idea with a fixed, pre-written reference-context block, and sends it to the IBM Granite model via `.generate_text()`.
5. The model's response is returned as text/markdown and rendered in the browser without a full page reload.

**Credentials handling:** `.env` holds `API_KEY`, `PROJECT_ID`, and `URL`; `config.py` reads them via Python's `os` module so they never appear hardcoded in `app.py`.

**Important limitation, stated plainly:** this is not a vector-retrieval RAG pipeline. There is no embedding step and no vector database. The "retrieval" is a fixed block of fact-checked reference text (Startup India Seed Fund Scheme details, the 9 Business Model Canvas blocks, a go-to-market framework, and common Indian early-stage funding categories) injected directly into every prompt, combined with an explicit instruction not to invent facts outside that context. This is a legitimate and common grounding technique, but it is context-injection, not retrieval-augmented generation in the strict sense — the model is not searching a document store per query, it is reading the same static context every time. If this project continues past prototype stage, adding the vector-retrieval step from the abandoned Langflow design is the natural next iteration, not a redesign.

---

## 4. UI

A separate static HTML/CSS/JS mockup was also built to explore visual direction (a technical-blueprint aesthetic: grid background, drafting title block, a rendered Business Model Canvas grid, simulated generation states). This mockup is not wired to the live Flask backend — it's a design reference and demo asset, not part of the deployed app's actual code path.

---

## 5. Deployment status

Not deployed. Running locally only (`localhost`, Flask dev server). A deployment plan was written covering Render (free, no card, fastest path), PythonAnywhere (free, permanent, limited resources), and IBM Cloud Code Engine (strongest fit with the IBM ecosystem narrative, but requires a credit card on file even for its free tier — a real blocker under the "no card" constraint this project has operated under so far).

---

## 6. What's proven to work

- End-to-end request flow from browser form to Granite-generated response, confirmed locally.
- Output reliably includes the six required sections (Problem & Opportunity, Business Model Canvas, Estimated Budget, Go-to-Market Strategy, Relevant Government Schemes, Investor Types) when tested against sample startup ideas.
- Output correctly reflects the seeded reference facts (e.g. correct SISFS grant figures) rather than inventing numbers, when spot-checked.

## 7. What's not proven / not done

- No real retrieval pipeline (see Section 3 limitation).
- No deployment — no public URL exists yet.
- No automated testing beyond a manual connection-check script (`test_connection.py`) and manual spot-checks of generated output.
- No handling for concurrent users, rate limiting, or error states beyond basic request/response flow.
- No formal evaluation of output quality across a broad set of startup ideas — testing was limited to a small number of manual samples.
