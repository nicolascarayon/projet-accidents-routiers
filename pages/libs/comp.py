import streamlit as st

color_titles = "#e28743"

style_header    = f"color:{color_titles};font-size:36px;font-weight:600"
style_subheader = f"color:{color_titles};font-size:28px;font-weight:600"

def sidebar_info():
    # title = "a"
    info = '''
    DataScientest \n
    Bootcamp DS DEC22 \n
    Nicolas CARAYON
    https://www.linkedin.com/in/nicolascarayon/
    '''
    st.sidebar.info(info)


def header(text):
    st.markdown(f'<p style={style_header}>{text}</p>', unsafe_allow_html=True)

def subheader(text):
    st.markdown(f'<p style={style_subheader}>{text}</p>', unsafe_allow_html=True)
