import streamlit as st
import requests, time

BACKEND = "http://backend:8000"

st.set_page_config(page_title="Algo Control")
st.title("NIFTY Algo Control Panel")

if st.button("▶ START"):
    requests.post(f"{BACKEND}/start")

if st.button("⏹ STOP"):
    requests.post(f"{BACKEND}/stop")

status = requests.get(f"{BACKEND}/status").json()
st.metric("Running", "YES" if status["running"] else "NO")
st.metric("State", status["state"])

time.sleep(2)
st.rerun()