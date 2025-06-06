import streamlit as st

def Header():
    st.markdown("""
        <style>
            #MainMenu, header, footer { visibility: hidden; }
            .main { padding-left: 0rem; padding-right: 0rem; }
            .block-container {
                padding-left: 10rem;
                padding-right: 10rem;
                padding-top: 0;
                padding-bottom: 1rem;
                margin: 0;
                max-width: 100%;
            }
            body { margin: 0; padding: 0; overflow-x: hidden; }
            h1 { margin-top: 0rem; font-size: 40px; }
        </style>
    """, unsafe_allow_html=True)