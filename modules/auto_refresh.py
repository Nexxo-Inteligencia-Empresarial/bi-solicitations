import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

def AutoRefresh():
    st_autorefresh(interval=600000)
    
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()
    if "refresh_interval" not in st.session_state:
        st.session_state.refresh_interval = 3600
    
    if time.time() - st.session_state.last_update > st.session_state.refresh_interval:
        st.session_state.last_update = time.time()
        st.experimental_rerun()