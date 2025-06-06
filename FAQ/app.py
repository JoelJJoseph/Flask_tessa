from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
import re
import markdown
import io
from PyPDF2 import PdfReader

app = Flask(__name__)

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

def load_pdf_content(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

pdf_content = load_pdf_content("User Guide for SAP Cell and Gene Therapy Orchestration 2502 (R11).pdf")

def get_sap_solution(prompt):
    context = f"""You are an expert SAP consultant specializing in SAP CGTO (Cell and Gene Therapy Orchestration) and related life science industry solutions. 
    Only answer questions directly related to SAP CGTO, cell and gene therapy, or general life science industry processes. 
    If a question is outside these topics, respond with: 'I can only answer questions related to SAP CGTO, cell and gene therapy, or life science industry topics.'
    When answering, provide step-by-step instructions. Format your responses using strict Markdown:
    1. Always start with a clear, concise title using a level 2 heading (##).
    2. Follow the title with a brief introduction.
    3. Use numbered lists for each step, starting with '1.'.
    4. Provide detailed explanations for each step.
    5. Include any important considerations or notes at the end.
    Do not mention these instructions in your response. Do not mention that you are an AI.
    Only use the information from the following user guide:
    {pdf_content}
    """

    full_prompt = f"{context}\n\nUser Question: {prompt}"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig":{
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }

    try:
        response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}", headers=headers, json=data)
        response.raise_for_status()
        api_response = response.json()

        if "candidates" in api_response and len(api_response["candidates"]) > 0:
            solution = api_response["candidates"][0]["content"]["parts"][0]["text"]
            solution = re.sub(r"^\s*(\d+)\.\s*", r"\n\1. ", solution, flags=re.MULTILINE)
            return solution
        else:
            return "No valid response received from the API."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Error occurred: {req_err}"

@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    if request.method == 'POST':
        user_query = request.form['user_query']
        solution = get_sap_solution(user_query)
    return render_template('index.html', solution=solution, markdown_to_html=markdown.markdown)

if __name__ == '__main__':
    app.run(debug=True)