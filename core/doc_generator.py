import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.callbacks.manager import get_openai_callback
from core.prompt_builder import build_prompt
from utils.logger import logger

def generate_doc(doc_type, tech_info, project_type, folder_structure, file_summaries):
    logger.info(f"Generating {doc_type} using LLM...")
    
    prompt = build_prompt(doc_type, tech_info, project_type, folder_structure, file_summaries)
    
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if not api_key:
        return {"content": f"# Error: Missing AZURE_OPENAI_API_KEY.\nCannot generate {doc_type}.", "tokens": None}
        
    try:
        llm = AzureChatOpenAI(
            azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=api_key,
            temperature=0.2
        )
        with get_openai_callback() as cb:
            response = llm.invoke([HumanMessage(content=prompt)])
            
            logger.info(f"LLM Token Usage [{doc_type}] - Input: {cb.prompt_tokens} | Output: {cb.completion_tokens} | Total: {cb.total_tokens}")
            
            return {
                "content": response.content,
                "tokens": {
                    "prompt": cb.prompt_tokens,
                    "completion": cb.completion_tokens,
                    "total": cb.total_tokens,
                    "successful_requests": cb.successful_requests
                }
            }
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        return {"content": f"# Error generating {doc_type}\n{str(e)}", "tokens": None}

