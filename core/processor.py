import os
from utils.helpers import read_file_content, get_folder_structure
from core.sanitizer import sanitize_content
from utils.logger import logger

class ProjectProcessor:
    def __init__(self, extract_dir):
        self.extract_dir = extract_dir
        # Exclude common binaries and massive dirs
        self.exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode'}
        self.exclude_exts = {'.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar', '.gz', '.pdf', '.exe', '.dll', '.so', '.class', '.pyc'}

    def process(self):
        logger.info(f"Processing directory: {self.extract_dir}")
        folder_struct = get_folder_structure(self.extract_dir)
        
        file_summaries = {}
        for root, dirs, files in os.walk(self.extract_dir):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.exclude_exts:
                    continue
                    
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.extract_dir)
                
                content = read_file_content(file_path)
                sanitized_content = sanitize_content(content)
                file_summaries[rel_path] = sanitized_content
                
        logger.info(f"Processed {len(file_summaries)} text files.")
        return folder_struct, file_summaries
