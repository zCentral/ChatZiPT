import streamlit as st
from utils.performance import PerformanceMonitor

st.title("ChatZiPT Dashboard")
monitor = PerformanceMonitor()
monitor.start()
st.write("Welcome to the ChatZiPT dashboard.")
st.write(f"PerformanceMonitor: {monitor.elapsed():.4f} seconds")