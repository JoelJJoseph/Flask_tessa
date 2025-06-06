# ai_presentation_apps.py
import streamlit as st
import pandas as pd
from PIL import Image

def release_report_summarizer_app():
    st.title("📝 Release Report Summarizer ")
    st.markdown("### Purpose:")
    st.write("To summarize SAP release notes PDFs and extract relevant insights. ")

    st.markdown("### Features:")
    st.markdown("""
    * Upload a release report PDF 
    * Prompt-based summarization 
    * Extracts and lists relevant content with page numbers 
    * Generates tabular summary of extracted data 
    """)

    st.markdown("### Workflow:")
    st.markdown("""
    1.  Upload SAP release report (PDF) 
    2.  Enter prompt/query based on what info you need 
    3.  Tool extracts relevant data 
    4.  Outputs summary with: 
        * Relevant content 
        * Page numbers 
        * Tabular format for quick viewing 
    """)

    # Relevant image for summarization/data extraction
    try:
        # Assuming you have an image like this in an 'images' folder for demonstration
        # If you don't have a specific image, you can remove this block
        image_path = "images/ai_lab.jpg" # Placeholder for a relevant image
        image = Image.open(image_path)
        st.image(image, caption="AI for Release Report Summarization", use_column_width=True)
    except FileNotFoundError:
        st.info("No specific image for Release Report Summarizer found. Add one to the 'images' folder for visual context.")


    uploaded_file = st.file_uploader("Upload SAP Release Report PDF", type="pdf")
    if uploaded_file is not None:
        st.success("PDF uploaded successfully!")
        st.write("You can now enter your prompt below.")
        user_prompt = st.text_area("Enter your prompt/query:", "Summarize the key changes in this release.")
        if st.button("Generate Summary"):
            st.info("Processing your PDF and generating summary...")
            # In a real application, you would integrate a PDF parsing and NLP model here.
            st.subheader("Summary:")
            st.write("*(This is a simulated summary based on your prompt and a placeholder for actual processing.)*")
            st.write("Relevant content from the uploaded PDF would appear here. For example:")
            st.write("- New UI features on page 5.")
            st.write("- Bug fixes in module X on page 12.")

            st.subheader("Tabular Summary:")
            data = {
                "Category": ["UI Enhancements", "Bug Fixes", "Performance Improvements"],
                "Details": ["Redesigned user interface", "Resolved login issues", "Optimized data loading"],
                "Page Numbers": ["5, 7", "12", "15-16"]
            }
            df = pd.DataFrame(data)
            st.table(df)

def faq_solving_tool_app():
    st.title("❓ FAQ Solving Tool ")
    st.markdown("### Purpose:")
    st.write("To provide answers to user queries based on the CGTO User Guide. ")

    st.markdown("### Features:")
    st.markdown("""
    * Prompt-based question input 
    * Searches CGTO user guide 
    * Returns concise answers with references 
    * Helps with onboarding, training, and issue resolution 
    """)

    st.markdown("### Workflow:")
    st.markdown("""
    * **Query:** "What is the standard workflow for CGTO batch release?" 
    * **Output:**
        * Concise explanation 
        * Reference to section/page in user guide 
        * Additional resources if needed 
    """)
    # Relevant image for FAQ assistant
    try:
        # Assuming you have an image like this in an 'images' folder for demonstration
        # If you don't have a specific image, you can remove this block
        image_path = "images/faq_assistant.jpg" # Placeholder for a relevant image
        image = Image.open(image_path)
        st.image(image, caption="AI for FAQ Assistance", use_column_width=True)
    except FileNotFoundError:
        st.info("No specific image for FAQ Assistant found. Add one to the 'images' folder for visual context.")


    user_query = st.text_input("Enter your question about the CGTO User Guide:")
    if st.button("Get Answer"):
        if user_query:
            st.info(f"Searching for answer to: '{user_query}'...")
            # In a real application, you would integrate a knowledge base search/QA model here.
            st.subheader("Answer:")
            st.write("*(This is a simulated answer and a placeholder for actual processing.)*")

            if "workflow for CGTO batch release" in user_query.lower():
                st.write("The standard workflow for CGTO batch release involves several steps including quality checks, documentation review, and final approval by authorized personnel. This process ensures compliance and product integrity. ")
                st.markdown("Reference: CGTO User Guide, Section 3.2, Page 15 ")
                st.markdown("Additional Resources: See Appendix A for a detailed flowchart. ")
            else:
                st.write("I am sorry, I couldn't find a direct answer to your query in the CGTO User Guide. Please try rephrasing your question or refer to the full user guide for more details.")
        else:
            st.warning("Please enter a question to get an answer.")