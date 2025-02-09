import fitz  # PyMuPDF for PDF processing
import logging

def handle_file_upload(uploaded_files):
    """
    Handles multiple file uploads and extracts text from PDF, TXT, or DOCX files.
    
    Args:
        uploaded_files (list): A list of uploaded files from Streamlit file_uploader.
    
    Returns:
        str: Extracted text from all uploaded files (first 500 characters per file).
    """
    combined_text = ""

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                file_name = uploaded_file.name
                file_type = file_name.split(".")[-1].lower()
                logging.info(f"Processing file: {file_name} (Type: {file_type})")

                if file_type == "pdf":
                    try:
                        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                        file_text = "\n".join([page.get_text("text") for page in doc])
                    except Exception as e:
                        logging.error(f"Error processing PDF {file_name}: {str(e)}")
                        file_text = f"[Error reading {file_name}]"
                
                elif file_type in ["txt", "docx"]:
                    try:
                        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
                    except Exception as e:
                        logging.error(f"Error reading file {file_name}: {str(e)}")
                        file_text = f"[Error reading {file_name}]"
                
                else:
                    file_text = f"[Unsupported file type: {file_name}]"

                # Append extracted text with a file header (limit to first 500 characters)
                combined_text += f"\n\n[File: {file_name}]\n{file_text[:500]}"

            except Exception as e:
                logging.error(f"Unexpected error processing file {uploaded_file.name}: {str(e)}")
    
    return combined_text
