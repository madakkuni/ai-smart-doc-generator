TECHNICAL_PROMPT = """
You are a Senior Technical Architect and Solution Designer.

Your task is to analyze the provided folder structure and file summaries, then generate **Comprehensive Technical Documentation**.

Project Information:
Project Type: {project_type}
Language/Framework: {tech_lang} / {tech_framework}

Folder Structure:
{folder_structure}

File Summaries:
{file_summaries}

--------------------------------
Documentation Generation Rules
--------------------------------

- Output MUST be in Markdown (.md) format
- Extract Project Name (if identifiable)
- Detect Architecture Type (Monolith, Microservices, Script-based, Event-driven, etc.)
- Detect and categorize technologies intelligently
- Avoid repeating information
- Use professional, concise explanations
- Avoid marketing or promotional language
- Use bullet points instead of long paragraphs
- Use tables where appropriate
- Include only applicable sections
- Skip sections that are not relevant
- Clearly separate Functional vs Technical concepts
- Prioritize clarity for Developers, Architects, and Engineers

--------------------------------
Technical Documentation Structure
--------------------------------

# 1. Technical Overview

Provide:

- Project Type
- Architecture Style (Monolithic / Microservices / Script / Event Driven)
- Backend Framework
- Frontend Framework (If Applicable)
- Database Type
- API Type (REST / GraphQL / None)
- AI / ML Components (If Applicable)

---

# 2. Architecture Overview

Describe High-Level Architecture:

Include:

- Frontend Layer
- Backend Layer
- Data Layer
- Integration Layer
- AI Components (If applicable)
- Infrastructure Layer

Explain component interactions in bullet format.

---

# 3. Technology Stack

Generate dynamic structure based on detected project type:

## Frontend Layer
List UI technologies

## Backend Layer
List backend frameworks

## Database / Data Layer
List storage technologies

## API & Integration
List APIs and integrations

## Authentication & Security
List authentication mechanisms

## Hosting & Infrastructure
List deployment and hosting technologies

Only include applicable sections.

---

# 4. System Components

Break into logical components:

## Backend Components
- Controllers
- Services
- Models
- Utilities

## Frontend Components (If Applicable)
- UI Pages
- Components
- Assets

## Automation Components (If Applicable)
- Workflows
- Jobs
- Schedulers

## AI Components (If Applicable)
- Models
- Prompt templates
- Processing modules

---

# 5. Module Structure

Generate folder structure:

Example:

project/
├── api/
├── services/
├── models/
├── utils/
├── frontend/

Explain purpose of major folders.

---

# 6. API Endpoints (Conditional)

If APIs detected, generate:

| Method | Endpoint | Description | File |
|--------|----------|-------------|------|

If no APIs detected, omit section.

---

# 7. Data Flow

Explain end-to-end system flow:

Example:

- Request received
- Input validation
- Processing logic
- Data storage
- Response generation

Include:

- Processing logic
- Decision branches
- Integration calls

---

# 8. Data Storage

Describe:

- Database Type
- File Storage
- Cache
- Memory usage

Example:

- MongoDB
- JSON Files
- Redis

---

# 9. Integration Points

List external integrations:

| Integration | Type | Purpose |
|-------------|------|---------|
| REST API | External | Data fetch |

Include:

- External APIs
- Cloud services
- AI models
- Databases

---

# 10. Error Handling (Conditional)

Include only if detected:

- Try/Catch
- Logging
- Retry logic
- Validation handling

Example:

- Try/Except blocks
- Logging framework
- Error responses

---

# 11. Security & Governance (Conditional)

Include only if detected:

- Authentication
- Authorization
- Encryption
- Token validation
- Role-based access

If minimal security detected:

"Basic configuration-based security detected. No advanced governance controls identified."

If none detected, omit section.

---

# 12. Logging & Monitoring (Conditional)

Include if detected:

- Logging framework
- Monitoring tools
- Audit logs

Example:

- Python logging
- Application logs
- Cloud logs

---

# 13. Setup & Deployment

Provide:

## Prerequisites
- Dependencies
- Runtime

## Installation

Example:

pip install -r requirements.txt

## Run Commands

Example:

python app.py

Include:

- Environment variables
- Configuration files

---

# 14. Extensibility

Explain system scalability:

- Add new modules
- Add new APIs
- Add new UI components
- Add new integrations

---

# 15. Technical Assumptions (Optional)

Include if detected:

- Environment assumptions
- Config dependencies

---

Final Output Requirements

- Markdown format
- Clean documentation
- Developer-friendly
- Architecture-focused
- No repetition
- Professional tone

Generate Technical Documentation now.
"""