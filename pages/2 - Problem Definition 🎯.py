from toolkit import problem, problem_generator


import streamlit as st


def on_click_random_problem():
    st.session_state.generated_random_problem = True
    random_problem = problem_generator(
        num_squads=num_squad, num_cells=num_cell, num_prisoners=num_prisoners
    )
    st.session_state.problem = random_problem


if "loaded" in st.session_state:
    with st.expander("See blog post problem definition"):
        st.write(problem)

    num_squad = st.slider("Number of squads", 4, 7, 4)
    num_prisoners = st.slider("Approx. size of squads", 5, 15, 8)
    num_cell = st.slider("Number of cells", 4, 7, 4)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("Generate custom problem", on_click=on_click_random_problem)
    if st.session_state.generated_random_problem:
        st.write(st.session_state.problem)
else:
    st.write("Visit Home page first !")
