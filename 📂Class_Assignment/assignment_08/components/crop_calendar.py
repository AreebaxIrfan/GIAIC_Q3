import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.figure_factory as ff
from components.ui_components import get_text
import logging

def render_crop_calendar(farm_manager, crops):
    st.title("Crop Calendar with AI Alerts" if st.session_state.language == "en" else "فصل کیلنڈر مع اے آئی انتباہات")
    st.write("Plan your sowing, harvesting, and tasks, and get weather-adjusted crop recommendations." if st.session_state.language == "en" else "اپنی بوائی، کٹائی، اور کاموں کی منصوبہ بندی کریں اور موسم کے مطابق فصل کی سفارشات حاصل کریں۔")

    try:
        crop_names = [crop.name for crop in crops]
        selected_crop = st.selectbox(get_text("select_crop"), crop_names)
        city = st.text_input(get_text("city"), "Karachi" if st.session_state.language == "en" else "کراچی")
        sowing_date = st.date_input("Select sowing date" if st.session_state.language == "en" else "بوائی کی تاریخ منتخب کریں", datetime.now()).strftime("%Y-%m-%d")

        if st.button("Generate Crop Calendar" if st.session_state.language == "en" else "فصل کیلنڈر بنائیں"):
            with st.spinner("Generating calendar..." if st.session_state.language == "en" else "کیلنڈر بنایا جا رہا ہے..."):
                schedule = farm_manager.generate_calendar(selected_crop, city, sowing_date)
                st.success(f"Calendar generated for {selected_crop}!" if st.session_state.language == "en" else f"{selected_crop} کے لیے کیلنڈر بنایا گیا!")
                st.subheader("Crop Schedule" if st.session_state.language == "en" else "فصل کا شیڈول")
                st.write(f"Sowing Date: {schedule['sowing_date']}" if st.session_state.language == "en" else f"بوائی کی تاریخ: {schedule['sowing_date']}")
                st.write(f"Harvesting Date: {schedule['harvesting_date']}" if st.session_state.language == "en" else f"کٹائی کی تاریخ: {schedule['harvesting_date']}")
                st.write("Tasks:" if st.session_state.language == "en" else "کام:")
                for task in schedule["tasks"]:
                    st.write(f"- {task['task']}: {task['date']}")

                calendar_data = farm_manager.get_calendar_data(selected_crop)
                st.subheader("Calendar Table" if st.session_state.language == "en" else "کیلنڈر ٹیبل")
                st.dataframe(calendar_data)

                tasks = []
                for _, row in calendar_data.iterrows():
                    tasks.append(dict(
                        Task=row["task_name"],
                        Start=row["task_date"],
                        Finish=row["task_date"],
                        Resource=row["crop_name"]
                    ))
                fig = ff.create_gantt(tasks, title=f"Crop Calendar for {selected_crop}" if st.session_state.language == "en" else f"{selected_crop} کے لیے فصل کیلنڈر")
                st.plotly_chart(fig)

        st.subheader("Seasonal Crop Recommendations" if st.session_state.language == "en" else "موسمی فصل کی سفارشات")
        month = st.slider("Select month" if st.session_state.language == "en" else "مہینہ منتخب کریں", 1, 12, datetime.now().month)
        if st.button("Get Crop Recommendations" if st.session_state.language == "en" else "فصل کی سفارشات حاصل کریں"):
            with st.spinner("Generating recommendations..." if st.session_state.language == "en" else "سفارشات بنائی جا رہی ہیں..."):
                recommendations = farm_manager.recommend_crops(city, month)
                st.subheader("Recommended Crops" if st.session_state.language == "en" else "تجویز کردہ فصلیں")
                rec_df = pd.DataFrame(recommendations)
                st.dataframe(rec_df)

                fig = px.bar(rec_df, x="crop", y="suitability", title=f"Crop Recommendations for {city}, Month {month}" if st.session_state.language == "en" else f"{city}، مہینہ {month} کے لیے فصل کی سفارشات")
                st.plotly_chart(fig)

    except Exception as e:
        logging.error(f"Crop Calendar failed: {str(e)}")
        st.error("Error in crop calendar. Please check logs/app.log." if st.session_state.language == "en" else "فصل کیلنڈر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔")