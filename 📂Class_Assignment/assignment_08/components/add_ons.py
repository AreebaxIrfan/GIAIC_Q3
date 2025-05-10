import streamlit as st
from utils.chatbot_utils import identify_pest_gemini
from utils.db_utils import log_action
from components.ui_components import get_text
import logging

def render_add_ons():
    st.title("Unique Add-Ons" if st.session_state.language == "en" else "منفرد ایڈ آنز")
    try:
        st.subheader("AR Pest Scanner" if st.session_state.language == "en" else "اے آر کیڑوں کا اسکینر")
        st.write("Upload pest images to identify pests and get management suggestions." if st.session_state.language == "en" else "کیڑوں کی تصویر اپ لوڈ کریں تاکہ کیڑوں کی شناخت ہو اور انتظامی تجاویز حاصل ہوں۔")
        pest_img = st.file_uploader("Upload pest image" if st.session_state.language == "en" else "کیڑوں کی تصویر اپ لوڈ کریں", type=["jpg", "png"])
        if pest_img:
            with st.spinner("Analyzing pest with Gemini AI..." if st.session_state.language == "en" else "جیمنی اے آئی کے ساتھ کیڑوں کا تجزیہ ہو رہا ہے..."):
                pest_result = identify_pest_gemini(pest_img)
                st.image(pest_img, width=200)
                if pest_result.startswith("Error:"):
                    st.error(pest_result)
                else:
                    st.write(f"**Result**: {pest_result}" if st.session_state.language == "en" else f"**نتیجہ**: {pest_result}")
                    log_action("AR Pest Scanner", f"Identified: {pest_result}")
    except Exception as e:
        logging.error(f"AR Pest Scanner failed: {str(e)}")
        st.error("Error in AR Pest Scanner. Please check logs/app.log." if st.session_state.language == "en" else "اے آر کیڑوں کے اسکینر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔")