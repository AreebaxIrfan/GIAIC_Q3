import streamlit as st
import pandas as pd
from components.ui_components import get_text
import logging
import os
from datetime import datetime, timedelta
import plotly.express as px

# Set up logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s"
)

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None
    logging.error("FPDF library not installed. PDF generation disabled. Run 'pip install fpdf' to enable.")

def generate_pdf_report(df, filename="data/history_report.pdf"):
    """Generate a PDF report from a DataFrame using FPDF."""
    if not FPDF:
        logging.error("Cannot generate PDF: FPDF library not available")
        st.error(
            "PDF generation unavailable. Install fpdf: pip install fpdf"
            if st.session_state.get("language", "en") == "en" else
            "PDF بنانا دستیاب نہیں ہے۔ fpdf انسٹال کریں: pip install fpdf"
        )
        return None

    try:
        # Check for font files
        font_regular = "NotoSans-Regular.ttf"
        font_bold = "NotoSans-Bold.ttf"
        if not (os.path.exists(font_regular) and os.path.exists(font_bold)):
            logging.error(f"Font files missing: {font_regular} and/or {font_bold}")
            st.error(
                f"Font files missing: {font_regular} and {font_bold}. Download from Google Fonts."
                if st.session_state.get("language", "en") == "en" else
                f"فونٹ فائلیں غائب ہیں: {font_regular} اور {font_bold}۔ گوگل فونٹس سے ڈاؤن لوڈ کریں۔"
            )
            return None

        pdf = FPDF()
        pdf.add_font("NotoSans", "", font_regular)
        pdf.add_font("NotoSans", "B", font_bold)
        pdf.set_font("NotoSans", "", 12)
        pdf.add_page()

        # Title
        title = "Smart AgriPak App Report" if st.session_state.get("language", "en") == "en" else "سمارٹ  پاک ایپ رپورٹ"
        pdf.set_font("NotoSans", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(10)

        # Table Header
        pdf.set_font("NotoSans", "B", 10)
        headers = ["Timestamp", "Action Type", "Details", "Crop", "Location", "User"]
        col_widths = [30, 30, 60, 30, 30, 20]
        for header, width in zip(headers, col_widths):
            pdf.cell(width, 10, header, border=1)
        pdf.ln()

        # Table Data
        pdf.set_font("NotoSans", "", 8)
        for _, row in df.iterrows():
            for col, width in zip(row, col_widths):
                pdf.cell(width, 10, str(col)[:50], border=1)  # Truncate long text
            pdf.ln()

        # Save PDF
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf.output(filename)
        logging.info(f"Generated PDF report: {filename}")
        return filename
    except Exception as e:
        logging.error(f"Failed to generate PDF: {str(e)}", exc_info=True)
        st.error(
            f"Failed to generate PDF: {str(e)}"
            if st.session_state.get("language", "en") == "en" else
            f"PDF بنانے میں ناکامی: {str(e)}"
        )
        return None

def render_reports(farm_manager, crops):
    """Render the Reports page to view and download historical data."""
    logging.info("Rendering Reports page")
    st.title("📊 " + get_text("reports"))
    st.markdown(
        "View and download historical data for weather, mandi prices, irrigation, and crop health."
        if st.session_state.get("language", "en") == "en" else
        "موسم، منڈی کی قیمتوں، ایریگیشن، اور فصل کی صحت کے تاریخی ڈیٹا کو دیکھیں اور ڈاؤن لوڈ کریں۔"
    )

    try:
        # Load history
        history_file = "data/history.csv"
        if not os.path.exists(history_file):
            st.warning(
                "No historical data available."
                if st.session_state.get("language", "en") == "en" else
                "کوئی تاریخی ڈیٹا دستیاب نہیں ہے۔"
            )
            logging.info("No history.csv found")
            return

        df = pd.read_csv(history_file)
        if df.empty:
            st.info(
                "Historical data is empty."
                if st.session_state.get("language", "en") == "en" else
                "تاریخی ڈیٹا خالی ہے۔"
            )
            return

        # Convert timestamp to datetime and log invalid entries
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        invalid_timestamps = df[df["timestamp"].isna()]
        if not invalid_timestamps.empty:
            logging.warning(f"Found {len(invalid_timestamps)} invalid timestamps in history.csv: {invalid_timestamps.to_dict()}")
            st.warning(
                f"Found {len(invalid_timestamps)} invalid timestamps in history.csv. These rows will be excluded from date filtering."
                if st.session_state.get("language", "en") == "en" else
                f"history.csv میں {len(invalid_timestamps)} غلط ٹائم اسٹیمپ ملے۔ یہ قطاریں تاریخ کے فلٹر سے خارج ہوں گی۔"
            )

        # Filters
        st.subheader("Filter Data" if st.session_state.get("language", "en") == "en" else "ڈیٹا فلٹر کریں")
        col1, col2, col3 = st.columns(3)
        with col1:
            action_types = ["All"] + sorted(df["action_type"].unique())
            selected_action = st.selectbox(
                "Action Type" if st.session_state.get("language", "en") == "en" else "عمل کی قسم",
                action_types
            )
        with col2:
            crops_list = ["All"] + sorted(df["crop"].unique())
            selected_crop = st.selectbox(get_text("select_crop"), crops_list)
        with col3:
            # Use valid timestamps for date range
            valid_timestamps = df[df["timestamp"].notna()]
            min_date = valid_timestamps["timestamp"].min().date() if not valid_timestamps.empty else datetime.now().date()
            max_date = valid_timestamps["timestamp"].max().date() if not valid_timestamps.empty else datetime.now().date()
            start_date = st.date_input(
                "Start Date" if st.session_state.get("language", "en") == "en" else "شروع کی تاریخ",
                min_date
            )
            end_date = st.date_input(
                "End Date" if st.session_state.get("language", "en") == "en" else "ختم کی تاریخ",
                max_date
            )

        # Apply filters
        filtered_df = df.copy()
        if selected_action != "All":
            filtered_df = filtered_df[filtered_df["action_type"] == selected_action]
        if selected_crop != "All":
            filtered_df = filtered_df[filtered_df["crop"] == selected_crop]
        
        # Filter by date only for valid timestamps
        filtered_df = filtered_df[
            filtered_df["timestamp"].notna() &  # Exclude NaT
            (filtered_df["timestamp"].dt.date >= start_date) &
            (filtered_df["timestamp"].dt.date <= end_date)
        ]

        # Display data
        st.subheader("Historical Data" if st.session_state.get("language", "en") == "en" else "تاریخی ڈیٹا")
        st.dataframe(
            filtered_df,
            column_config={
                "timestamp": "Timestamp" if st.session_state.get("language", "en") == "en" else "وقت",
                "action_type": "Action Type" if st.session_state.get("language", "en") == "en" else "عمل کی قسم",
                "details": "Details" if st.session_state.get("language", "en") == "en" else "تفصیلات",
                "crop": "Crop" if st.session_state.get("language", "en") == "en" else "فصل",
                "location": "Location" if st.session_state.get("language", "en") == "en" else "مقام",
                "user": "User" if st.session_state.get("language", "en") == "en" else "صارف"
            },
            use_container_width=True
        )

        # Plot action frequency
        if not filtered_df.empty:
            action_counts = filtered_df["action_type"].value_counts().reset_index()
            action_counts.columns = ["action_type", "count"]
            fig = px.bar(
                action_counts,
                x="action_type",
                y="count",
                title="Action Frequency" if st.session_state.get("language", "en") == "en" else "عمل کی تعدد",
                labels={
                    "action_type": "Action Type" if st.session_state.get("language", "en") == "en" else "عمل کی قسم",
                    "count": "Count" if st.session_state.get("language", "en") == "en" else "تعداد"
                }
            )
            fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # Download buttons
        st.subheader("Download Reports" if st.session_state.get("language", "en") == "en" else "رپورٹس ڈاؤن لوڈ کریں")
        col1, col2 = st.columns(2)
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "Download CSV" if st.session_state.get("language", "en") == "en" else "CSV ڈاؤن لوڈ کریں",
                csv,
                "history_report.csv",
                "text/csv"
            )
        with col2:
            if FPDF:
                pdf_file = generate_pdf_report(filtered_df)
                if pdf_file and os.path.exists(pdf_file):
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "Download PDF" if st.session_state.get("language", "en") == "en" else "PDF ڈاؤن لوڈ کریں",
                            f,
                            "history_report.pdf",
                            "application/pdf"
                        )
                else:
                    st.error(
                        "Failed to generate PDF report. Check font files or logs."
                        if st.session_state.get("language", "en") == "en" else
                        "PDF رپورٹ بنانے میں ناکامی۔ فونٹ فائلیں یا لاگ چیک کریں۔"
                    )
            else:
                st.error(
                    "PDF generation unavailable. Install fpdf: pip install fpdf"
                    if st.session_state.get("language", "en") == "en" else
                    "PDF بنانا دستیاب نہیں ہے۔ fpdf انسٹال کریں: pip install fpdf"
                )

    except Exception as e:
        logging.error(f"Reports page failed: {str(e)}", exc_info=True)
        st.error(
            f"Error in reports: {str(e)}. Please check logs/app.log."
            if st.session_state.get("language", "en") == "en" else
            f"رپورٹس میں خرابی: {str(e)}۔ براہ کرم logs/app.log چیک کریں۔"
        )