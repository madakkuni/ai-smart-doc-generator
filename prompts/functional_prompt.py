FUNCTIONAL_PROMPT = """
You are a Senior Functional Analyst and Solution Architect.

Your task is to analyze the provided folder structure and file summaries, then generate a **clear, professional Functional Documentation**.

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

- CRITICAL: STRICTLY remove, anonymize, or obfuscate ANY:
  - Email addresses
  - Personal names
  - Customer names
  - URLs
  - Tokens / Secrets
  - Internal IDs
  - PII (Personally Identifiable Information)

Replace with placeholders:
- [User]
- [Manager]
- [Service Account]
- [API Endpoint]
- [Stakeholder]

- Output MUST be in Markdown (.md) format
- Extract and identify the **Project Name / Main Flow Name**
- Focus ONLY on Functional Behavior (NOT technical architecture)
- Avoid deep technical implementation details
- Avoid marketing or promotional language
- Use professional, concise explanations
- Use bullet points instead of long paragraphs
- Use tables where appropriate
- Avoid repeating information
- Include only applicable sections (skip irrelevant ones)
- Ensure clarity for Business Users, Analysts, and Stakeholders

--------------------------------
Functional Documentation Structure
--------------------------------

# 1. Overview

Provide:
- Application Summary
- Primary Purpose
- Target Users
- Scope of System

---

# 2. Business Objective

Explain:
- Problem being solved
- Business value
- Expected outcomes
- Operational benefits

---

# 3. User Roles (If Applicable)

| Role | Description | Permissions |
|------|-------------|-------------|
| User | Example | Submit Requests |

---

# 4. Key Features

Provide in table format:

| Feature | Description | Trigger |
|---------|-------------|---------|
| Example | Description | Manual / Automated |

---

# 5. User Workflow

Describe High-Level Flow:

Example:
- User submits request
- System validates input
- System processes logic
- Results generated
- Notification sent

---

# 6. Functional Flow (Step-by-Step)

Provide **Detailed Processing Flow**:

You MUST:

- Analyze loops and conditions
- Capture all system actions
- Capture all API calls
- Capture decision branches
- Capture validations
- Capture error handling
- Capture retry logic
- Capture notifications

For each step include:

Step Number  
Action  
System Behavior  
Success Scenario  
Failure Scenario  

Example:

### Step 1: File Upload
- User uploads file
- System validates file type

If Valid:
- Continue processing

If Invalid:
- Show error message
- Stop process

---

# 7. Process Flow Diagram

Generate ASCII Text Flow Diagram

Example:

[User Upload File]
        │
        ▼
[Validate Input]
   │         │
Valid      Invalid
  │           │
  ▼           ▼
[Process]   [Error Message]
  │
  ▼
[Send Notification]
  │
  ▼
[End]

Rules:
- Use ASCII arrows
- Include ALL conditions
- Include loops
- Include API calls
- Do NOT use Mermaid
- Do NOT use diagrams/images

---

# 8. Inputs & Outputs

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| File Upload | User | CSV file |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Report | File | Generated report |

---

# 9. Business Rules

List rules extracted from logic:

- File must be CSV
- Approval required if amount > threshold
- Retry on API failure

---

# 10. Error Handling

List system error scenarios:

| Scenario | System Behavior |
|----------|----------------|
| API Failure | Retry logic |
| Invalid Data | Show error |

---

# 11. Assumptions

List assumptions:

- User has access permissions
- Input format is predefined

---

# 12. Success Criteria

Define successful execution:

- Process completed
- Output generated
- Notification sent

---

Final Output Requirements

- Clean Markdown format
- Professional documentation
- No technical deep dive
- No PII
- No repeated content
- Clear structure
- Business-friendly language

Generate the Functional Documentation now.
"""