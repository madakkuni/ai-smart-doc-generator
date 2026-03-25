from utils.logger import logger

def classify_project(tech_info, file_summaries):
    """
    Classify project based on tech info and files.
    """
    logger.info("Classifying project type...")
    
    language = tech_info.get("language", "")
    framework = tech_info.get("framework", "")
    
    project_type = "Generic Project"
    
    if "Delphi" in language or "RAD Studio" in framework:
        project_type = "Desktop Application"
    elif "Power Automate Cloud" in framework or "Power Automate Cloud" in language:
        project_type = "Power Automate Cloud Automation"
    elif "Power Automate Desktop" in framework or "Power Automate Desktop" in language:
        project_type = "Power Automate Desktop Automation"
    elif "Selenium" in framework or "Power Automate" in language or "PowerShell" in language:
        project_type = "Automation Project"
    elif "Pandas" in framework or "NumPy" in framework or "Scikit-Learn" in framework or "TensorFlow" in framework or "PyTorch" in framework or "LangChain" in framework or "OpenAI" in framework:
        if "Streamlit" in framework or "Flask" in framework or "FastAPI" in framework or "Django" in framework or "React" in framework or "Next.js" in framework or "Vue" in framework or "Angular" in framework:
            project_type = "AI / ML Web Application"
        else:
            project_type = "AI / Machine Learning / Data Analysis Project"
    elif "Flask" in framework or "FastAPI" in framework or "Express" in framework or "Spring Boot" in framework or "Django" in framework:
        project_type = "API Service / Dynamic Web App"
    elif "React" in framework or "Angular" in framework or "Vue" in framework or "Streamlit" in framework or "Next.js" in framework or "Svelte" in framework:
        project_type = "Web Application"
    elif "HTML/CSS/JS" in language:
        project_type = "Static Website"
    elif any(f.lower().endswith('.ipynb') for f in file_summaries.keys()):
        project_type = "Machine Learning / Data Analysis Project"
        
    # Check Mobile App
    files = list(file_summaries.keys())
    if "android" in files or "ios" in files or any(f.endswith('AndroidManifest.xml') for f in files):
        project_type = "Mobile Application"
        
    pkg_file = next((f for f in files if f.endswith('package.json')), None)
    if pkg_file and "react-native" in file_summaries.get(pkg_file, "").lower():
        project_type = "Mobile Application"

    logger.info(f"Classified as: {project_type}")
    return project_type
