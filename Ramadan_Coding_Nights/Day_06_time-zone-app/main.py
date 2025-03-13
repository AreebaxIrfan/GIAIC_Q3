import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

TIME_ZONE =[
    "UTC",
    "Asia/Karachi",
    "Asia/Kolkata",
    "America/New_York",
    "Europe/London",
    "Australia/Sydney", 
    "Asia/Tokyo",
    "Asia/Dubai",
    "Europe/Paris",
    "Europe/Berlin",
    "Europe/Moscow",
]


st.title("Time Zone App")
selected_timezone = st.multiselect("Select the Time Zone", TIME_ZONE , default=["UTC", "Asia/Karachi"])

st.subheader("selected TimeZone")

for tz in selected_timezone:
    current_time = datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")
    st.write(f"{tz} : {current_time}")

st.header("Conver time between Timezones")

current_time = st.time_input("Current Time", datetime.now().time())

from_tz = st.selectbox("From Timezone", TIME_ZONE, index= 0)
to_tz = st.selectbox("To Timezone", TIME_ZONE, index= 1)

if st.button("Convert time"):

    bt = datetime.combine(datetime.today() , current_time, tzinfo=ZoneInfo(from_tz))

    converted_time = bt.astimezone(ZoneInfo(to_tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")

    st.success(f"Converted Time in {from_tz} : {converted_time} ")