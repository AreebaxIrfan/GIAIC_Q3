import streamlit as st
from utils.chatbot_utils import get_chatbot_response
from components.ui_components import get_text
import logging

def render_consulted():
    st.title("Consulted: Your Farming Assistant" if st.session_state.language == "en" else "مشاورت: آپ کا زرعی معاون")
    st.write("Ask about crops, soil, pests, irrigation, or farm productivity! Powered by Google Gemini." if st.session_state.language == "en" else "فصلوں، مٹی، کیڑوں، ایریگیشن، یا فارم کی پیداوار کے بارے میں پوچھیں! گوگل جیمنی سے تقویت یافتہ۔")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        for sender, message in st.session_state.chat_history[-10:]:
            with st.chat_message(sender.lower()):
                st.write(message)

    user_input = st.chat_input("Your question (e.g., How to improve farm productivity for tomatoes?)" if st.session_state.language == "en" else "آپ کا سوال (مثال کے طور پر، ٹماٹروں کے لیے فارم کی پیداوار کیسے بہتر کریں؟)")
    if user_input:
        with st.spinner("Consulted is thinking..." if st.session_state.language == "en" else "مشاورت سوچ رہا ہے..."):
            try:
                st.session_state.chat_history.append(("You" if st.session_state.language == "en" else "آپ", user_input))
                with chat_container:
                    with st.chat_message("you"):
                        st.write(user_input)
                
                response = get_chatbot_response(user_input)
                if response.startswith("Error:"):
                    st.error(response)
                else:
                    st.session_state.chat_history.append(("Consulted" if st.session_state.language == "en" else "مشاورت", response))
                    with chat_container:
                        with st.chat_message("consulted"):
                            st.write(response)
            except Exception as e:
                logging.error(f"Chatbot response failed: {str(e)}")
                st.error("Error in chatbot. Please check your API or try again." if st.session_state.language == "en" else "چیٹ بوٹ میں خرابی۔ براہ کرم اپنی API کی چیک کریں یا دوبارہ کوشش کریں۔")