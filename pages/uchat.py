import streamlit as st
from module import js_test

st.set_page_config(page_title="uchat", page_icon="💬")

js_test.draw_chat()