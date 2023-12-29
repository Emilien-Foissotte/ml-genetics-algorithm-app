import streamlit as st

from toolkit import state_generator


def on_click_reset():
    state_generator(session_state=st.session_state)


st.set_page_config(
    page_title="🧬 Algorithms",
)
st.title("Demonstration of Genetics Algorithms")


st.markdown(
    """
This webpage is a demonstration of use of Genetics Algorithms.  \n  \n
The goal is :
- To maximize the number of **prisoners** under custody 👤 \n \n
Knowing that :
- Prisoners are gathered in **squads** 👥
- You can fill a **Cell** ⛓️ with members of same squads
- Prisoners in **courtyard** 🚶 can be mixed from all squads.
- But in courtyard, they can't be watched..
\n
"""
)
st.divider()

st.write(
    "Deep dive using tabs on the left, read more about following my blog"
    "post available [here in french](https://emilien-foissotte.github.io/fr/posts/"
    "2023/10/genetic-algorithm/?utm_campaign=GAWebApp) or [here in english](https://emilien-foissotte.github.io/posts/"
    "2023/10/genetic-algorithm/?utm_campaign=GAWebApp)"
)

st.write("It's on you, don't disappoint Big Brother..")
st.image("pages/img/courtyard.png")

if "loaded" not in st.session_state:
    state_generator(session_state=st.session_state)
else:
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("Reset experiments", on_click=on_click_reset)
