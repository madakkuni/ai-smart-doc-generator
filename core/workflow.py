import concurrent.futures
from core.doc_generator import generate_doc
from utils.logger import logger

def run_pipeline(selected_docs, tech_info, project_type, folder_structure, file_summaries, progress_callback=None):
    logger.info("Starting hybrid AI pipeline...")
    
    results = {}
    
    docs_to_generate = selected_docs.copy()
    if "Both" in docs_to_generate or set(["Functional Documentation", "Technical Documentation"]).issubset(set(docs_to_generate)):
        docs_to_generate = ["Functional Documentation", "Technical Documentation", "Architecture"]
    elif "Both" in docs_to_generate:
        docs_to_generate = ["Functional Documentation", "Technical Documentation", "Architecture"]
    else:
        # Include base architecture by default
        docs_to_generate.append("Architecture")
        docs_to_generate = list(set(docs_to_generate))
        
    total_tasks = len(docs_to_generate)
    completed = 0
    total_tokens_used = {"prompt": 0, "completion": 0, "total": 0, "successful_requests": 0}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_doc = {
            executor.submit(generate_doc, doc, tech_info, project_type, folder_structure, file_summaries): doc
            for doc in docs_to_generate
        }
        
        for future in concurrent.futures.as_completed(future_to_doc):
            doc = future_to_doc[future]
            try:
                res = future.result()
                if isinstance(res, dict):
                    results[doc] = res.get("content", f"Error missing content for {doc}")
                    tokens = res.get("tokens")
                    if tokens:
                        total_tokens_used["prompt"] += tokens.get("prompt", 0)
                        total_tokens_used["completion"] += tokens.get("completion", 0)
                        total_tokens_used["total"] += tokens.get("total", 0)
                        total_tokens_used["successful_requests"] += tokens.get("successful_requests", 0)
                else:
                    results[doc] = res
                    
                completed += 1
                if progress_callback:
                    progress_callback(doc, completed, total_tasks)
            except Exception as e:
                logger.error(f"Agent failed for {doc}: {str(e)}")
                results[doc] = f"Error: {str(e)}"
                
    # Combine outputs
    final_markdown = f"# Project Documentation\n\n"
    final_markdown += f"**Detected Language:** {tech_info.get('language')}\n"
    final_markdown += f"**Detected Framework:** {tech_info.get('framework')}\n"
    final_markdown += f"**Project Type:** {project_type}\n\n"
    
    if "Architecture" in results:
        final_markdown += f"---\n\n{results['Architecture']}\n\n"
    if "Functional Documentation" in results:
        final_markdown += f"---\n\n{results['Functional Documentation']}\n\n"
    if "Technical Documentation" in results:
        final_markdown += f"---\n\n{results['Technical Documentation']}\n\n"
        
    return final_markdown, total_tokens_used
