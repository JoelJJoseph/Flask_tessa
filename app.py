# app.py
import streamlit as st
from multiapp import MultiApp

# CRITICAL CHANGE: st.set_page_config() must be the very first Streamlit command
st.set_page_config(
    page_title="AI Implementation in CGTO (Tessa Project)",
    layout="centered", # or "wide"
    initial_sidebar_state="expanded" # or "collapsed" or "auto"
)

# Import the application modules from their respective subfolders
from Summerization import streamlit_app as summarization_module
from FAQ import streamapp as faq_module

app = MultiApp()

new_title = '<p style="font-family:sans-serif; color:#004d80; font-size: 52px;"><b>AI Implementation in CGTO (Tessa Project)</b></p>'
st.markdown(new_title, unsafe_allow_html=True)

app.add_app("📝 Release Report Summarizer", summarization_module.summarization_app)
app.add_app("❓ FAQ Assistant", faq_module.faq_app)

app.run()