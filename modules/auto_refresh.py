import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

def AutoRefresh():
    st_autorefresh(interval=600000, key="auto_refresh")