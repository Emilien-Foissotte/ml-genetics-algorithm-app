import streamlit as st
import pandas as pd
import numpy as np

from toolkit import problem, state_generator


def on_click_reset():
    state_generator(session_state=st.session_state)


st.set_page_config(
    page_title="Home 🏠",
)
st.title("Demonstration of Genetics Algorithms")


st.markdown(
    """
This webpage is a demonstration of use of Genetics Algorithms.  \n  \n
The goal is : 
- To maximize the number of **prisoners** under custody 👤 \n
\n
Knowing that :
- Prisoners are gathered in **squads** 👥
- You can fill a **Cell** ⛓️ with members of same squads
- Prisoners in **courtyard** 🚶 can be mixed from all squads.
- But in courtyard, they can't be watched..
\n
Have fun ! """
)

st.divider()

st.write(
    "Deep dive using tabs on the left, read more about following my blog"
    "post available [here](https://emilien-foissotte.github.io/fr/posts/2023/10/genetic-algorithm/?utm_campaign=GAWebApp)"
)

if "loaded" not in st.session_state:
    state_generator(session_state=st.session_state)
else:
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("Reset experiments", on_click=on_click_reset)
