# Startup-Blueprint-Generator-Agent

An enterprise-grade, fact-grounded AI assistant powered by **IBM watsonx.ai** and **IBM Granite Models**. This application transforms a user's raw startup idea into a comprehensive, practical, and highly realistic business blueprint, completely eliminating the risk of LLM hallucinations by binding context directly to verified state schemes and regulatory frameworks.

---

## 📖 Table of Contents
- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features
* **Fact-Grounded Generation:** Restricts AI analysis to verified regulatory reference contexts, preventing hallucinations of non-existent grants or arbitrary financial figures.
* **Hyper-Local Personalization:** Generates custom blueprints based on sector, corporate structure, and geographic parameters.
* **Comprehensive 19-Point Framework:** Builds detailed blueprints covering Executive Summaries, Problem Statements, Market Opportunities, UVPs, Business Model Canvases (BMC), Technology Stacks, and Go-to-Market (GTM) frameworks.
* **Glassmorphic UI:** Modern, responsive frontend designed with CSS backdrop filters and smooth gradient styling.
* **Asynchronous Execution:** Fast, non-blocking asynchronous user interaction implemented via client-side JavaScript fetch streams.

---

## 🏗️ Architecture Overview

The application follows a clean **Client-Server Architecture**:
1. **Frontend UI:** Receives user parameters and handles responsive rendering.
2. **Flask Backend:** Manages communication, environment orchestration, and prompt formatting.
3. **IBM watsonx.ai Layer:** Infers using the `ibm/granite-4-h-small` (or `Granite-4.0-8B-Instruct`) foundation model over secure API channels, guarded by native HAP (Hate, Abuse, Profanity) content filters.

---

## 💻 Tech Stack
* **Core Framework:** Python 3.11+ / Flask
* **AI Orchestration:** `ibm-watsonx-ai` SDK
* **Foundation Model:** IBM Granite Series (`ibm/granite-4-h-small`)
* **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript (ES6+ Asynchronous Fetch)
* **Configuration:** `python-dotenv`

---

## 📁 Project Structure

```text
StartupUI/
│
├── static/
│   ├── script.js          # Handles frontend UI updates and API communication
│   └── style.css          # Contains glassmorphic styling and visual accents
│
├── templates/
│   └── index.html         # Main web portal interface layout
│
├── app.py                 # Core Flask backend controller and AI interface
├── config.py              # Environment configuration loader
├── test_connection.py     # Standalone diagnostic suite for API verification
├── requirements.txt       # Project dependency configuration
└── .env                   # Local secret environment keys (Excluded from Git)
