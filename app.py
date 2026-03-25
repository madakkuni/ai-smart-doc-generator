import streamlit as st
import os
import shutil
import tempfile
from core.processor import ProjectProcessor
from core.tech_detector import detect_technology
from core.project_classifier import classify_project
from core.workflow import run_pipeline
from utils.helpers import extract_zip
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Smart Document Generator", page_icon="📄", layout="wide")

st.title("📄 Smart Document Generator")
st.markdown("Automatically analyze an uploaded ZIP project and generate intelligent documentation using AI.")

# 1. Project Input Section
st.header("1. Project Input")
col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("Project Name", value="My Project")
    main_entry_file = st.text_input("Main Entry File (Optional)", placeholder="e.g. app.py, main.java")

with col2:
    uploaded_file = st.file_uploader("Upload ZIP File", type="zip")

# 2. Document Type Selection
st.header("2. Document Type Selection")
doc_types = st.multiselect(
    "Choose Documentation Types to Generate:",
    options=["Functional Documentation", "Technical Documentation", "Both"],
    default=["Functional Documentation", "Technical Documentation"]
)

if "Both" in doc_types:
    doc_types = ["Both"]

# 3. Generate Button
if st.button("Generate Smart Documentation"):
    if not uploaded_file:
        st.error("Please upload a ZIP file to proceed.")
    elif not doc_types:
        st.error("Please select at least one document type.")
    elif not os.environ.get("AZURE_OPENAI_API_KEY"):
        st.error("Missing AZURE_OPENAI_API_KEY. Please add it to your .env file or environment variables.")
    else:
        with st.status("Processing Project...", expanded=True) as status_box:
            try:
                # Step 1: Extract Zip
                st.write("Extracting ZIP file...")
                temp_dir = tempfile.mkdtemp()
                zip_path = os.path.join(temp_dir, "uploaded.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                extract_dir = os.path.join(temp_dir, "extracted")
                os.makedirs(extract_dir, exist_ok=True)
                extract_zip(zip_path, extract_dir)
                
                # Step 2: Read files and Folder Structure
                st.write("Reading folder structure and files...")
                processor = ProjectProcessor(extract_dir)
                folder_struct, file_summaries = processor.process()
                st.write(f"Processed {len(file_summaries)} files.")
                
                # Step 3: Technology Detection
                st.write("Detecting technology stack...")
                tech_info = detect_technology(file_summaries)
                st.success(f"Detected Language: {tech_info['language']} | Framework: {tech_info['framework']}")
                
                # Step 4: Classification
                st.write("Classifying project type...")
                project_type = classify_project(tech_info, file_summaries)
                st.success(f"Project Type: {project_type}")
                
                # Step 5: AI Processing
                st.write("Generating AI Documentation (this might take a few minutes)...")
                
                progress_bar = st.progress(0)
                def progress_callback(doc_name, current, total):
                    progress_bar.progress(current / total)
                
                final_markdown, token_usage = run_pipeline(
                    selected_docs=doc_types,
                    tech_info=tech_info,
                    project_type=project_type,
                    folder_structure=folder_struct,
                    file_summaries=file_summaries,
                    progress_callback=progress_callback
                )
                
                status_box.update(label="Documentation Generated Successfully!", state="complete", expanded=False)
                
                if token_usage and token_usage.get("successful_requests", 0) > 0:
                    st.info(f"📊 **API Usage Metrics:**\n\n"
                            f"- **Executions:** {token_usage['successful_requests']}\n"
                            f"- **Prompt Tokens:** {token_usage['prompt']}\n"
                            f"- **Completion Tokens:** {token_usage['completion']}\n"
                            f"- **Total Tokens:** {token_usage['total']}")
                            
                st.session_state['generated_doc'] = final_markdown
                st.session_state['project_name'] = project_name
                
            except Exception as e:
                status_box.update(label="Error Processing Project", state="error", expanded=True)
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Execution error: {str(e)}")
            finally:
                # Cleanup
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)

# Preview and Download
if 'generated_doc' in st.session_state:
    st.header("3. Output Preview")
    st.markdown(st.session_state['generated_doc'])
    
    st.download_button(
        label="Download README.md",
        data=st.session_state['generated_doc'],
        file_name=f"{st.session_state.get('project_name', 'project').replace(' ', '_')}_README.md",
        mime="text/markdown"
    )
