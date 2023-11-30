import streamlit as st
import pandas as pd
import numpy as np

from toolkit import problem_MANE, state_generator 

def on_click_reset():
    state_generator(session_state=st.session_state)

st.set_page_config(
        page_title="Home 🏠",
)
st.title('Demonstration of Genetics Algorithms')

st.write("This webpage is a demonstration of use of Genetics Algorithms")

st.write(
    "Deep dive using tabs on the left, read more about following my blog"
    "post available [here](https://emilien-foissotte.github.io/fr/posts/2023/10/genetic-algorithm/?utm_campaign=GAWebApp)"
)

if 'loaded' not in st.session_state :
    state_generator(session_state=st.session_state)
else:
    st.button("Reset experiments", on_click=on_click_reset)


with st.expander("See problem definition"):
    st.write(problem)
