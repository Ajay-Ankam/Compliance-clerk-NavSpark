import streamlit as st
import pandas as pd
from services.processor import PDFProcessor
from services.extractor import DocumentExtractor
from database.db_manager import init_db, fetch_all_logs
from dotenv import load_dotenv

# Initialize 
load_dotenv()
init_db()  # Ensures the SQLite table exists on startup
extractor = DocumentExtractor()

st.set_page_config(page_title="The Compliance Clerk", page_icon="⚖️", layout="wide")

# --- UI Header ---
st.title("⚖️ The Compliance Clerk")
st.markdown("### Intelligent Document Extraction for eChallan & NA Permissions")
st.divider()

# --- Sidebar for Audit Logs ---
with st.sidebar:
    st.header("📋 Audit Trail")
    if st.button("Refresh Logs"):
        logs = fetch_all_logs()
        if logs:
            log_df = pd.DataFrame(logs, columns=["ID", "Time", "File", "Type", "Prompt", "Response", "Status"])
            st.dataframe(log_df[["Time", "File", "Status"]], use_container_width=True)
        else:
            st.info("No logs found yet.")

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Document")
    uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"])
    
    if uploaded_file:
        doc_type = st.radio("Select Document Type", ["eChallan", "NA Permission"], horizontal=True)
        
        if st.button("⚡ Extract Structured Data", type="primary"):
            with st.spinner("Gemini is analyzing the document..."):
                # 1. Extract Text
                pdf_text = PDFProcessor.extract_text(uploaded_file.getvalue())
                
                if pdf_text:
                    # 2. Extract Data via LLM
                    result = extractor.extract(pdf_text, doc_type, uploaded_file.name)
                    
                    if result:
                        st.session_state['last_result'] = result.model_dump()
                        st.success("Extraction Successful!")
                    else:
                        st.error("Extraction failed. Check the Audit Trail for details.")
                else:
                    st.error("Could not read the PDF file.")

with col2:
    st.subheader("📊 Extraction Result")
    if 'last_result' in st.session_state:
        data = st.session_state['last_result']
        
        # Display as JSON for verification
        st.json(data)
        
        # Convert to DataFrame for Report Generation
        df = pd.DataFrame([data])
        
        st.divider()
        st.subheader("📥 Export Report")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"report_{uploaded_file.name}.csv",
            mime="text/csv",
        )
    else:
        st.info("Upload and process a document to see results here.")