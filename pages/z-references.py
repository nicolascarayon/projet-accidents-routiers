import pandas as pd
import streamlit as st

st.title("Decision Tree Classifier")

st.header('Header')
st.subheader('Subheader')
st.text('bla bla')
st.markdown('**Hello** world!')
st.markdown("[Google](https://www.google.com)")
st.markdown('---')
st.caption('I am a caption')
st.latex(r"f(x)=3x^2+2x+1")
st.json({'a':'1,2,3', 'b':'4,5,6', 'c':'7,8,9'})
code="""
print("Hellow world")
def func(x):
    return x+1
"""
st.code(code, "python")
st.metric(label="Wind speed", value="120ms-1", delta="-1.4ms-1")

df = pd.DataFrame({'col 1':[1,2,3,4,5], 'col 2':[2,3,4,5,6], 'col 3':[3,4,5,6,7]})
st.table(df)
st.dataframe(df)

st.image("./pics/Illustration-of-random-forest-trees.png", caption="Here's a random forest classifier", width=900)

def change():
    print("Changed")

state = st.checkbox("Text for checkbox", value=True, on_change=change())

if state:
    st.write("Checked")
else:
    st.write("Unchecked")


radio_btn = st.radio(label="This is the question:", options=("answer 1", "Answer 2", "Answer 3"))
print(radio_btn)

st.selectbox("WHat is  you favorite color?", options=('red', 'blue', 'white'))

multi_select = st.multiselect("Select your options", options=('option 1', 'option 2', 'option 3'))
st.write(multi_select)

st.slider("This is a slider")
val = st.text_input('Enter something here', max_chars=100)
st.write(val)

st.text_area('Some description')