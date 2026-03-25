# 📄 Smart Document Generator

The Smart Document Generator is a production-ready Streamlit application that automatically analyzes an uploaded ZIP project and generates intelligent documentation (Functional, Technical, or Architecture overviews) using LangChain and OpenAI. 

It is capable of automatically detecting the project's technology stack, classifying the project type, and reading file structures to create comprehensive Markdown reports.

## Features

- **Deep Technology Detection**: Dynamically parses projects to natively identify everything from modern Web App stacks (React, FastAPI, Python) and Automation workflows (Power Automate Cloud, Power Automate Desktop, Selenium), to legacy tools (Delphi / Embarcadero RAD Studio) and Scripting engines (PowerShell).
- **Intelligent Project Classification**: Maps the exact detected stack to classify the project architecture (e.g., `Desktop Application`, `Power Automate Cloud Automation`, `API Service`), fundamentally dictating how the AI structures the outputs.
- **Dynamic Technical Layering**: Uniquely groups the "Technology Stack" in Technical Documentation into perfectly categorized logical layers tailored to the codebase (e.g., grouping Automation Platforms vs. Scripting Execution Environments).
- **Granular Functional Extraction**: Strictly extracts every atomic API call, conditional logical branch (If Yes/No), and targeted notification flow natively from complex sources like Microsoft Logic JSONs and loops.
- **Cost & API Usage Tracking**: Integrates `langchain_community` callbacks to securely monitor, log, and aggregate LLM token usage (Prompt, Completion, Total) across concurrent agent tasks, displaying live metrics in the Streamlit UI.
- **Hybrid AI Pipeline**: Orchestrates parallel `langchain` chains backed by OpenAI models to synchronously generate multidimensional documentation.

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- Valid OpenAI API Key

### 2. Installation

1. Clone or navigate to the project repository:
   ```bash
   cd C:\My_Projects\ai-smart-doc-generator
   ```

2. (Optional but recommended) Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Environment Variables:
   Create a `.env` file in the root of the project with your OpenAI credentials:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

### 3. Running the Application

Execute the Streamlit application using:
```bash
streamlit run app.py
```

## ⚙️ How It Works: The Generation Pipeline

When a `.zip` project is uploaded to the application, it goes through a rigorous, multi-step automated pipeline:

1. **Extraction & Indexing (`core/processor.py`)**: The `.zip` archive is securely extracted into memory. The system recursively indexes the folder structure while automatically filtering out irrelevant binaries, build nodes (e.g., `node_modules`, `venv`), and hidden directories.
2. **Data Sanitization & PII Scrubbing (`core/sanitizer.py`)**: Before any analysis occurs, a comprehensive regex-based engine scrubs the raw code. It permanently masks API tokens, database connection strings, passwords, explicit physical URLs, and Personally Identifiable Information (Emails/Names) to guarantee absolute data privacy.
3. **Deep Technology Detection (`core/tech_detector.py`)**: The system ingests the sanitized code payloads and precisely evaluates file extensions, imports, and core logic against `config/tech_config.yaml`. It seamlessly identifies exactly which Languages (e.g., Python, Object Pascal), Frameworks (e.g., React, Embarcadero RAD Studio), and Automation Platforms (e.g., Power Automate, Selenium) the project relies on.
4. **Intelligent Project Classification (`core/project_classifier.py`)**: Utilizing the detected technology map, the system categorizes the overall architectural domain (e.g., `Desktop Application`, `API Service`, `Power Automate Cloud Automation`, `Static Website`). This explicit classification dynamically dictates how the AI structures the ensuing documentation.
5. **Dynamic Prompt Assembly (`core/prompt_builder.py`)**: The sanitized codebase, technology stack, folder structure, and overarching project classification are perfectly compiled into strict, intuitively engineered `prompt` templates ensuring zero hallucination.
6. **Concurrent LLM Processing (`core/workflow.py` & `core/doc_generator.py`)**: The assembled context is dispatched simultaneously across parallel `langchain` agents backed by OpenAI's API. The system strictly enforces the prompt rules—such as dynamic technical layering and meticulous functional branching (If Yes/No)—while actively monitoring and aggregating Prompt/Completion token costs via tracking callbacks.
7. **Stitching & UI Output (`app.py`)**: The generated Markdown documents (Functional, Technical, and Architecture) are stitched together and rendered live in the Streamlit UI alongside an Executive API Usage Dashboard quantifying token consumption.

## 🧠 Dynamic Prompt Engineering

The true intelligence of the Smart Document Generator resides within its extensively engineered prompt templates (located in the `prompts/` directory). Rather than passing raw code blindly to the LLM, these prompts enforce strict, professional boundaries:

- **`functional_prompt.py`**: Designed to extract exact business processes. It explicitly forces the LLM to map out atomic API calls, specific "If Yes/If No" logical branches, and targeted user notifications without diving into the underlying code syntax. It mandates a strict logical flow diagram generated natively from complex inputs like Power Automate definitions.
- **`technical_prompt.py`**: Intelligently adapts its output based entirely on the project type. It categorizes the project's "Technology Stack" into explicitly defined logical architecture layers based on the context (e.g., separating Web Apps from Desktop Apps or Workflow Automation platforms).
- **Hardened Security Prompts**: **Every** prompt inherently instructs the AI to strictly mask, anonymize, and obfuscate any residual Personally Identifiable Information (emails, customer names), passwords, and valid HTTP endpoints that may have bypassed the initial sanitization regex check, enforcing ironclad security.

## 📝 System Logging & Token Auditing

The system utilizes an enterprise-grade robust logging mechanism (`utils/logger.py`) to asynchronously record all pipeline activities securely in the background without cluttering the UI. 

- **Auditable Traceability**: All folder extractions, deep tech detections, code sanitization hits, and project classification decisions are time-stamped and recorded in the isolated daily log file (e.g., `logs/SmartDocGen_20260325.log`).
- **Token Financial Tracking**: Every simultaneous generation request sent to OpenAI is meticulously wrapped in a `langchain_community` callback. The engine rigorously captures and inserts the precise `Input Tokens`, `Completion Tokens`, and `Total Tokens` consumed for every distinct section directly into the local log file. This translates to a highly accurate financial tracker, allowing administrators to monitor exact LLM consumption costs scaling against massive codebase evaluations.

## 🛠️ Configuration-Driven Detection (`tech_config.yaml`)

The entire technology detection engine is inherently dynamic and modular. The underlying backend heuristics rely heavily on `config/tech_config.yaml`—a centralized mapping file that administrators can instantly update to expand system knowledge natively without altering any backend Python code. 

By default, the engine seamlessly identifies, categorizes, and documents the following extensive list of architectures natively sourced from the configuration mappings:

### 🌐 Frontend Layers & Web Stacks
- JavaScript, TypeScript, HTML5, CSS3 
- React.js, Next.js (MERN stacks), Vue.js, Angular, Svelte
- Layout Frameworks: Bootstrap

### ⚙️ Backend Logic & APIs
- Python Frameworks: Django, Flask, FastAPI
- Enterprise APIs: Spring Boot (Java), Node.js / Express
- Systems Architecture: Go (Cloud), Rust

### 🗄️ Multi-Cloud Databases & Storage
- **Relational Databases (SQL):** PostgreSQL, MySQL, Microsoft SQL Server, Oracle, MariaDB, SQLite, Amazon Aurora, CockroachDB, YugabyteDB
- **NoSQL Document/Key-Value Storage:** MongoDB, Cassandra, Redis, Memcached, DynamoDB, CouchDB, Couchbase, Firebase Firestore, ArangoDB
- **Vector Stores (RAG context):** Pinecone, Weaviate, Qdrant, Chroma, FAISS, Milvus

### 🤖 Workflow Automation (RPA) & Scripting
- Microsoft Power Automate Cloud (Complex Flow JSONs)
- Microsoft Power Automate Desktop (PAD)
- Selenium Browser Automation
- Scripting Pipelines: PowerShell, Core Python

### 📱 Mobile & Native Architectures
- Modern Mobile: Flutter (Dart), React Native
- Native OS Stacks: Swift (iOS), Kotlin (Android)
- Legacy / Native Desktop: Delphi / Object Pascal (Embarcadero RAD Studio)
- Game Design: Unity

### 🧠 Distributed AI Engineering & Integration
- Deployed/Integrated Models: OpenAI, Anthropic (Claude), Google (Gemini), Meta (Llama), Mistral AI
- Model Integration Pipelines: LangChain, LlamaIndex, Vector Embeddings, RAG Architectures

## 📄 Expected Output Artifacts

When you upload your `.zip` sample source code or codebase, the system evaluates the payload and dynamically stitches together **clean, professional `.md` output files** ready for immediate download via the Streamlit UI:
- `Functional_Documentation.md`: Translates complex raw logic (like massive JSON maps) into non-technical operational features, rigorously extracting loops, conditions (If Yes/If No branches), and notification targets into ASCII Process Flow Diagrams.
- `Technical_Documentation.md`: Dissects and categorizes the underlying technology stack, intelligently structuring components based entirely on your architectural setup (e.g., placing Delphi gracefully into Desktop Layers, or Power Automate into Automation Platforms).

## Architectural Structure
```text
ai-smart-doc-generator/
│
├── app.py                      # Main Streamlit Frontend
├── requirements.txt            # Dependency configuration
│
├── core/
│   ├── processor.py            # Extracts zips, builds code structures
│   ├── tech_detector.py        # Identifies language/framework
│   ├── project_classifier.py   # Determines project domain
│   ├── sanitizer.py            # Masks keys, tokens, emails, urls
│   ├── prompt_builder.py       # Assembles AI prompts dynamically
│   ├── doc_generator.py        # Connects to OpenAI via Langchain
│   └── workflow.py             # Orchestrates the concurrent multi-agent flow
│
├── utils/
│   ├── logger.py               # Centralized logging logic
│   └── helpers.py              # File path logic and zip reading utilities
│
└── prompts/                    # Template files for specific agent roles
    ├── architecture_prompt.py
    ├── functional_prompt.py
    └── technical_prompt.py
```
