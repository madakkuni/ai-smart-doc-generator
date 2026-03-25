from prompts.functional_prompt import FUNCTIONAL_PROMPT
from prompts.technical_prompt import TECHNICAL_PROMPT
from prompts.architecture_prompt import ARCHITECTURE_PROMPT

def build_prompt(doc_type, tech_info, project_type, folder_structure, file_summaries):
    # Formats the right prompt
    file_summaries_text = ""
    for k, v in file_summaries.items():
        file_summaries_text += f"\n--- File: {k} ---\n{v[:2000]}\n" # limit per file size

    kwargs = {
        "project_type": project_type,
        "tech_lang": tech_info.get("language", "Unknown"),
        "tech_framework": tech_info.get("framework", "None"),
        "folder_structure": folder_structure,
        "file_summaries": file_summaries_text
    }
    
    if doc_type == "Functional Documentation":
        return FUNCTIONAL_PROMPT.format(**kwargs)
    elif doc_type == "Technical Documentation":
        return TECHNICAL_PROMPT.format(**kwargs)
    elif doc_type == "Architecture":
        return ARCHITECTURE_PROMPT.format(**kwargs)
    return ""
