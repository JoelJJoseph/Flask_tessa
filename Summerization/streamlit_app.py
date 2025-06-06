# Summerization/streamlit_app.py
import streamlit as st
import requests
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
import pandas as pd
import markdown

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

base_url = "https://generativelanguage.googleapis.com"
endpoint = "/v1beta/models/gemini-1.5-flash:generateContent"

# --- Function to Generate Summary ---
def generate_summary(text, prompt):
    if not GOOGLE_API_KEY:
        return "API key is not configured, cannot generate summary. Please check your .env file."

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{text}\n\n{prompt}"}
                ]
            }
        ]
    }
    try:
        response = requests.post(f"{base_url}{endpoint}?key={GOOGLE_API_KEY}", headers=headers, json=data)
        response.raise_for_status()
        api_response = response.json()

        if "candidates" in api_response and len(api_response["candidates"]) > 0:
            content = api_response["candidates"][0].get("content", {})
            if "parts" in content and len(content["parts"]) > 0:
                return content["parts"][0].get("text", "No 'text' field in 'parts'")
            else:
                return "No 'parts' field in 'content'"
        else:
            return "No 'candidates' field in response."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Error occurred: {req_err}"

# --- Streamlit UI Function ---
def summarization_app():
    # Removed st.set_page_config as it should be in app.py

    st.title("📄 PDF Summarizer with Tessa 🚀")

    st.write(
        "Upload a PDF document, and I'll summarize it using Google's Gemini 1.5 Flash model. "
        "You can also provide a custom prompt for the summary."
    )

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    default_prompt = (
        "Provide a detailed pointwise list of changes mentioned in the release notes along with page numbers "
        "and code snippets where applicable. Also, create a tabular representation of the changes."
    )
    prompt_input = st.text_area("Custom Prompt for Summary:", value=default_prompt, height=150)

    if uploaded_file is not None:
        if st.button("Generate Summary"):
            with st.spinner("Extracting text and generating summary..."):
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""

                    if not text:
                        st.warning("Could not extract any text from the PDF. Please try a different file.")
                    else:
                        summary = generate_summary(text, prompt_input)

                        st.subheader("Summary")
                        st.markdown(summary)

                        # --- CORRECTED Table Extraction Logic ---
                        table_start = -1
                        lines = summary.split('\n')
                        for i, line in enumerate(lines):
                            if "APPTABFIELDS" in line:
                                table_start = i
                                break

                        if table_start != -1: # If 'APPTABFIELDS' was found, attempt to parse the table
                            try:
                                table_data = []
                                headers = []
                                for line in lines[table_start:]:
                                    if line.startswith("APPTABFIELDS"):
                                        headers = [h.strip() for h in line.replace("APPTABFIELDS", "").split(",") if h.strip()]
                                    elif line.strip(): # Check if line is not empty
                                        row_data = [d.strip() for d in line.split(",") if d.strip()]
                                        if row_data: # Ensure there's actual data after stripping
                                            table_data.append(row_data)

                                if headers and table_data:
                                    cleaned_table_data = []
                                    for row in table_data:
                                        if len(row) == len(headers):
                                            cleaned_table_data.append(row)
                                        else:
                                            st.warning(f"Skipping a row due to column mismatch: {row}. Expected {len(headers)} columns, got {len(row)}.")

                                    if cleaned_table_data:
                                        st.subheader("Extracted Table")
                                        df = pd.DataFrame(cleaned_table_data, columns=headers)
                                        st.dataframe(df)
                                    else:
                                        st.info("No valid table data found after parsing.")
                                else:
                                    st.info("Could not parse a complete table from the summary, even though 'APPTABFIELDS' was found.")
                            except Exception as e: # Catch errors specifically during table parsing
                                st.error(f"Error during table parsing: {e}")
                        else: # This else correctly belongs to 'if table_start != -1:'
                            st.info("No 'APPTABFIELDS' keyword found in the summary to extract a table.")
                        # --- End CORRECTED Table Extraction Logic ---

                except Exception as e: # This except handles errors during PDF text extraction or summary generation
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Please upload a PDF file to get started.")

    st.markdown("---")