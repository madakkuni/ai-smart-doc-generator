import os
import yaml
from utils.logger import logger

def detect_technology(file_summaries):
    """
    Heuristics based technology detection driven by tech_config.yaml.
    file_summaries is a dict of {rel_path: content}
    """
    logger.info("Detecting technology dynamically...")
    
    # Load configuration
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'config', 'tech_config.yaml')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load tech_config.yaml: {e}")
        return {"language": "Unknown", "framework": "None"}
        
    files = list(file_summaries.keys())
    
    techs = set()
    frameworks_dbs = set()
    
    # Fast path: build combined content string
    all_pkg_contents = []
    all_code_contents = []
    
    pkg_extensions_to_check = set()
    code_extensions_to_check = set()
    
    langs_config = config.get('languages', {})
    if isinstance(langs_config, dict):
        for lang, rules in langs_config.items():
            if isinstance(rules, dict):
                if 'pkg_files' in rules:
                    pkg_extensions_to_check.update(rules['pkg_files'])
                if 'extensions' in rules:
                    code_extensions_to_check.update(rules['extensions'])
            
    if not code_extensions_to_check:
        code_extensions_to_check.update(['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.h', '.cs', '.dart', '.swift', '.kt'])
    if not pkg_extensions_to_check:
        pkg_extensions_to_check.update(['package.json', 'requirements.txt', 'pom.xml', 'gemfile', 'go.mod', 'cargo.toml', 'pubspec.yaml', 'build.gradle'])
        
    code_extensions_to_check.update(['.json', '.pad', '.pas', '.dfm', '.dpr', '.dproj', '.dpk'])
            
    for f, content in file_summaries.items():
        f_lower = f.lower()
        if any(f_lower.endswith(pkg) for pkg in pkg_extensions_to_check):
            all_pkg_contents.append(content.lower())
        if any(f_lower.endswith(ext) for ext in code_extensions_to_check):
            all_code_contents.append(content.lower())
            
    pkg_text = "\n".join(all_pkg_contents)
    code_text = "\n".join(all_code_contents)
    
    # 1. Detect Languages
    if isinstance(langs_config, dict):
        for lang, rules in langs_config.items():
            if isinstance(rules, dict):
                extensions = rules.get('extensions', [])
                pkg_files = rules.get('pkg_files', [])
                has_ext = any(any(f.endswith(ext) for ext in extensions) for f in files)
                has_pkg = any(any(f.endswith(pkg) for pkg in pkg_files) for f in files)
                if has_ext or has_pkg:
                    techs.add(lang)
            elif isinstance(rules, list):
                for item in rules:
                    if item.lower() in pkg_text or item.lower() in code_text:
                        techs.add(item)
            
    # 2. Detect Frameworks
    fw_config = config.get('frameworks', {})
    if isinstance(fw_config, dict):
        for category, category_frameworks in fw_config.items():
            if isinstance(category_frameworks, dict):
                for fw_name, fw_rules in category_frameworks.items():
                    if isinstance(fw_rules, dict):
                        keywords = fw_rules.get('keywords', [])
                        imports = fw_rules.get('imports', [])
                        if any(kw.lower() in pkg_text for kw in keywords):
                            frameworks_dbs.add(fw_name)
                            continue
                        if any(imp.lower() in code_text for imp in imports):
                            frameworks_dbs.add(fw_name)
                    elif isinstance(fw_rules, list):
                        for item in fw_rules:
                            if item.lower() in pkg_text or item.lower() in code_text:
                                frameworks_dbs.add(item)
            elif isinstance(category_frameworks, list):
                for item in category_frameworks:
                    if item.lower() in pkg_text or item.lower() in code_text:
                        frameworks_dbs.add(item)
                
    # 3. Detect Databases
    db_config = config.get('databases', {})
    if isinstance(db_config, dict):
        for db_category, db_rules in db_config.items():
            if isinstance(db_rules, dict):
                keywords = db_rules.get('keywords', [])
                if any(kw.lower() in pkg_text or kw.lower() in code_text for kw in keywords):
                    frameworks_dbs.add(db_category)
            elif isinstance(db_rules, list):
                for item in db_rules:
                    if item.lower() in pkg_text or item.lower() in code_text:
                        frameworks_dbs.add(item)

    # 4. Check Flat Lists for new categories
    for cat, cat_list in config.items():
        if cat not in ('languages', 'frameworks', 'databases') and isinstance(cat_list, list):
            for item in cat_list:
                parts = [p.strip() for p in item.replace('+', '/').split('/') if p.strip()] if '+' in item or '/' in item else [item]
                for p in parts:
                    if len(p) > 2 and (p.lower() in pkg_text or p.lower() in code_text):
                        if cat in ['web_stacks_and_languages', 'mobile_and_game_development']:
                            techs.add(p)
                        else:
                            frameworks_dbs.add(p)
                            
    # 5. Check specifically for Power Automate Cloud vs Desktop via core heuristics
    if "https://schema.management.azure.com/providers/microsoft.logic" in code_text or "workflowdefinition.json" in code_text or "workflowdefinition.json" in pkg_text:
        frameworks_dbs.add("Power Automate Cloud")
    if "desktopflow" in code_text or "robin" in code_text or any(f.lower().endswith('.pad') for f in files):
        frameworks_dbs.add("Power Automate Desktop")
        
    # 6. Check specifically for Delphi / Object Pascal (RAD Studio)
    if any(f.lower().endswith(('.pas', '.dfm', '.dpr', '.dproj', '.dpk')) for f in files):
        techs.add("Delphi / Object Pascal")
        frameworks_dbs.add("Embarcadero RAD Studio")
            
    language_str = ", ".join(sorted(list(techs))) if techs else "Unknown"
    framework_str = ", ".join(sorted(list(frameworks_dbs))) if frameworks_dbs else "None"
    
    logger.info(f"Detected Languages: {language_str}, Frameworks/DBs: {framework_str}")
    
    return {
        "language": language_str,
        "framework": framework_str
    }

