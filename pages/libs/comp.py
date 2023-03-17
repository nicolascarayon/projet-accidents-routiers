import streamlit as st

color_titles = "#e28743"
color_green = "green"
color_red = "red"

style_header = f"color:{color_titles};font-size:36px;font-weight:600"
style_subheader = f"color:{color_titles};font-size:28px;font-weight:600"


def sidebar_info():
    st.sidebar.info("""
                    **Nicolas CARAYON** \n
                    https://www.linkedin.com/in/nicolascarayon/ \n
                    DataScientest - Bootcamp DS DEC22
                    """)


def header(text):
    st.markdown(f'<p style={style_header}>{text}</p>', unsafe_allow_html=True)


def subheader(text):
    st.markdown(f'<p style={style_subheader}>{text}</p>', unsafe_allow_html=True)


def text(text, color, fontsize):
    st.markdown(f'<p style="color:{color};font-size:{fontsize}px;font-weight:600">{text}</p>', unsafe_allow_html=True)
