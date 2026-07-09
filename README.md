# Startup Blueprint Generator Agent

A prototype web application that converts a plain-language startup idea into a structured business blueprint, using IBM Granite on watsonx.ai. Built for IBM SkillsBuild University — Problem Statement #20.

## Status

Prototype. Runs locally. Not yet deployed. See [`PROJECT_JOURNEY.md`](./PROJECT_JOURNEY.md) for a full account of what was built, what was tried and abandoned, and current limitations.

## What it does

Takes a startup idea as input and returns an adaptive blueprint drawn from up to 19 possible sections — executive summary, problem statement, market opportunity, existing solutions & limitations, proposed solution, USP, business model (including a Business Model Canvas), revenue model, technology stack, estimated budget, go-to-market strategy, competitor analysis, SWOT, risks & challenges, relevant government schemes, potential funding sources, implementation roadmap, expected impact, and conclusion. The model is instructed to include only the sections relevant to the given idea rather than forcing all 19 into every response, targeting roughly 500–900 words.

Output is grounded in a fixed, fact-checked reference context (Startup India Seed Fund Scheme details, the 9-block Business Model Canvas structure, a go-to-market framework, and a list of common Indian early-stage funding sources), with explicit instructions not to invent facts, statistics, schemes, or market data outside that context. The model also declines, with a fixed three-sentence response, any request unrelated to startup planning.

**Note on architecture:** this is context-injection grounding, not a vector-retrieval RAG pipeline. There is no embedding step or vector database — the same reference-context block is included in every prompt. See `PROJECT_JOURNEY.md` for why, and for the planned next iteration.

## Tech stack

- **Backend:** Python, Flask
- **AI:** IBM Granite (`ibm/granite-4-h-small`) via the `ibm-watsonx-ai` SDK, IBM watsonx.ai
- **Frontend:** HTML, CSS (gradient/glassmorphism styling), vanilla JavaScript (`fetch` for async requests)
- **Config:** `python-dotenv` for environment variable management
- **Included but not yet used:** `gunicorn` is already in `requirements.txt`, anticipating a production deployment step

## Project structure

```
.
├── app.py                # Flask app, routes, watsonx.ai integration (POST /generate)
├── config.py              # Reads credentials from environment into app.py
├── .env                   # Local-only credentials (never committed — see below)
├── .gitignore              # Excludes .env and Python artifacts from version control
├── requirements.txt        # Pinned/listed dependencies
├── test_connection.py      # Standalone watsonx.ai connectivity check
├── static/
│   ├── style.css           # UI styling (gradient background, glass-panel cards)
│   └── script.js            # Form submission, async fetch, response rendering
└── templates/
    └── index.html           # Main page layout and input form
```

## Setup

### Prerequisites
- Python 3.10–3.12 recommended (some dependencies in this stack have had compatibility issues on 3.13 — see `PROJECT_JOURNEY.md`)
- An IBM Cloud account (Lite tier is sufficient) with a watsonx.ai project, an associated Watson Machine Learning instance, and an IBM Cloud API key

### Installation

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root (excluded from version control by `.gitignore` — verify this before your first commit):

```
API_KEY=your_ibm_cloud_api_key
PROJECT_ID=your_watsonx_project_id
URL=your_watsonx_region_endpoint   # e.g. https://us-south.ml.cloud.ibm.com
```

### Running locally

```bash
python app.py
```

Then open `http://localhost:5000` (or whichever port Flask reports) in a browser.

### Verifying your IBM Cloud connection independently

```bash
python test_connection.py
```

Sends a minimal "say hello" prompt directly to the model, bypassing the web layer — use this to isolate credential/network issues from application-level bugs.

## Deployment

Not yet deployed. `requirements.txt` already includes `gunicorn`, anticipating this step. A comparison of deployment options (Render, PythonAnywhere, IBM Cloud Code Engine, and others) with a recommended phased path has been documented separately as this project's deployment plan.

## Limitations

- Context-injection grounding, not true vector-retrieval RAG (see Architecture note above)
- No automated test suite beyond the manual `test_connection.py` connectivity script
- No rate limiting, concurrency handling, or production-grade error handling beyond a basic try/catch on the frontend fetch call
- Output has been spot-checked manually on a small number of sample ideas, not formally evaluated at scale
- The off-topic refusal behavior is defined in the prompt but has not been explicitly verified against adversarial or unrelated inputs

## Disclaimer

Output is guidance only and does not constitute legal or financial advice.

## Acknowledgments

Built with IBM Granite and IBM watsonx.ai as part of IBM SkillsBuild University.
