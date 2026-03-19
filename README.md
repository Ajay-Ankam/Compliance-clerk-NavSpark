# ⚖️ The Compliance Clerk: Intelligent Document Extraction

The Compliance Clerk is an AI-powered pipeline designed to automate the extraction of structured data from heterogeneous legal and government PDF documents. Built with Python, Streamlit, and Google Gemini-3, it transforms manual, error-prone data entry into a streamlined digital workflow.

---

## 🚀 Features

- **Multi-Format Parsing:** Specialized extraction logic for eChallan (traffic violations) and NA Permission (Non-Agricultural land) documents.  
- **LLM-Powered Intelligence:** Utilizes `gemini-3-flash-preview` for high-accuracy OCR and semantic understanding.  
- **Schema Enforcement:** Guaranteed valid data output using Pydantic models to ensure the UI and exports never break.  
- **Audit Trail:** A local SQLite database logs every raw LLM prompt and response for transparency and debugging.  
- **Atomic Evolution:** Developed using a strict atomic commit history to demonstrate the iterative refinement of logic and prompts.  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **AI Engine:** Google GenAI SDK (`gemini-3-flash-preview`)  
- **PDF Engine:** PyMuPDF (fitz)  
- **Data Validation:** Pydantic  
- **Database:** SQLite3  
- **Environment:** Python 3.10+  

---

## ⚙️ Setup & Installation

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/Ajay-Ankam/Compliance-clerk-NavSpark.git
cd compliance_clerk
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

The application requires a Google Gemini API Key to function.

Create a file named `.env` in the root directory and add:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

> Note: `.gitignore` is configured to prevent this key from being pushed to GitHub.

---

## 📖 How to Use

### Launch the App
```bash
streamlit run app.py
```

### Steps

1. **Upload:** Drag and drop an eChallan or NA Permission PDF into the uploader.  
2. **Select Type:** Choose the corresponding document type in the UI.  
3. **Extract:** Click "Extract Structured Data". The AI will parse the document and return a validated JSON result.  
4. **Export:** Download the results as a CSV/Excel report.  
5. **Audit:** View history and raw AI interactions in the sidebar. 

## 📂 Project Structure

```
app.py                     # Main Streamlit UI and orchestration logic
services/                 # Core logic for PDF processing and LLM extraction
schemas/                  # Pydantic models for data validation
database/                 # SQLite manager for audit trail
compliance_audit.db       # Auto-generated database for logs
```