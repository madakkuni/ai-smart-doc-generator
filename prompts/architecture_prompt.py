ARCHITECTURE_PROMPT = """
You are an expert Software Architect.
Based on the provided information, generate an Architecture Overview.
Project Type: {project_type}
Language/Framework: {tech_lang} / {tech_framework}

Folder Structure:
{folder_structure}

File Summaries:
{file_summaries}

Please output in markdown format. Include:
1. High-level Architecture
2. Logic Flow
3. Identified Risks
"""
