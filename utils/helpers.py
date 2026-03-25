import os
import zipfile

def extract_zip(zip_path, extract_to):
    """Extracts a zip file to the specified directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def get_folder_structure(root_dir):
    """Returns a string representation of the folder structure."""
    structure: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore common ignored dirs
        new_dirnames = [d for d in dirnames if d not in ['.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode']]
        dirnames.clear()
        dirnames.extend(new_dirnames)
        rel_path = os.path.relpath(dirpath, root_dir)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            structure.append(f"{subindent}{f}")
    return "\n".join(structure)

def read_file_content(file_path, max_length=10000):
    """Reads the content of a file, with a length limit."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > max_length:
                return content[:max_length] + f"\n... (truncated, original length: {len(content)})"
            return content
    except UnicodeDecodeError:
        return "[Binary or non-UTF-8 file]"
    except Exception as e:
        return f"[Error reading file: {e}]"
