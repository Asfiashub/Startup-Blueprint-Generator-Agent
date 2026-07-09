# Startup Blueprint Generator Agent

A prototype web application that converts a plain-language startup idea into a structured business blueprint, using IBM Granite on watsonx.ai. Built for IBM SkillsBuild University — Problem Statement #20.

## Status

Prototype. Runs locally. Not yet deployed. See [`PROJECT_JOURNEY.md`](./PROJECT_JOURNEY.md) for a full account of what was built, what was tried and abandoned, and current limitations.

## What it does

Takes a startup idea as input and returns:
- Problem & Opportunity summary
- Business Model Canvas (all 9 blocks)
- Estimated budget by category
- Go-to-market strategy
- Relevant government funding schemes (India-focused)
- Potential investor types

Output is grounded in a fixed, fact-checked reference context (Startup India Seed Fund Scheme details, standard Business Model Canvas structure, a go-to-market framework, and common early-stage funding categories), with an explicit instruction to the model not to invent figures outside that context.

**Note on architecture:** this is context-injection grounding, not a vector-retrieval RAG pipeline. There is no embedding step or vector database. See `PROJECT_JOURNEY.md` for why, and for the planned next iteration.

## Tech stack

- **Backend:** Python, Flask
- **AI:** IBM Granite (via `ibm-watsonx-ai` SDK), IBM watsonx.ai
- **Frontend:** HTML, CSS, vanilla JavaScript (`fetch` for async requests)
- **Config:** `python-dotenv` for environment variable management

## Project structure

```
.
├── app.py                # Flask app, routes, watsonx.ai integration (POST /generate)
├── config.py              # Reads credentials from environment into app.py
├── .env                   # Local-only credentials (never committed — see below)
├── requirements.txt        # Pinned dependencies
├── test_connection.py      # Standalone watsonx.ai connectivity check
├── static/
│   ├── style.css           # UI styling
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

Create a `.env` file in the project root (this file is git-ignored and must never be committed):

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

Use this to isolate credential/network issues from application-level bugs.

## Deployment

Not yet deployed. A comparison of deployment options (Render, PythonAnywhere, IBM Cloud Code Engine, and others) with a recommended phased path is documented separately in the project's deployment plan.

## Limitations

- Context-injection grounding, not true vector-retrieval RAG (see Architecture note above)
- No automated test suite beyond a manual connectivity script
- No rate limiting, concurrency handling, or production-grade error handling
- Output has been spot-checked manually on a small number of sample ideas, not formally evaluated at scale

## Disclaimer

Output is guidance only and does not constitute legal or financial advice.

## Acknowledgments

Built with IBM Granite and IBM watsonx.ai as part of IBM SkillsBuild University.
