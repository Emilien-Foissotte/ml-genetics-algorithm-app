from toolkit import matIndividual, problem, prettydf

import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Generation ⚙️",
)


def click_button_generate():
    st.session_state.clicked_generation = True


def click_button_sorted():
    st.session_state.sorted = True
    st.session_state.individuals = sorted(
        st.session_state.individuals, key=lambda indi: indi.fitness, reverse=True
    )


with st.expander("Idea behind generation💡"):
    st.caption(
        "The general idea is to, with randomness, try to populate cells and courtyard, respecting"
        " always the limits of the cells."
    )


if "loaded" in st.session_state:
    if st.session_state.generated_random_problem:
        target_problem = st.session_state.problem
    else:
        target_problem = problem
    col1, col2, col3 = st.columns(3)
    with col2:
        if not st.session_state.generated:
            st.button(
                "Generate individuals",
                on_click=click_button_generate,
                disabled=st.session_state.generated,
            )

    if st.session_state.clicked_generation and not st.session_state.generated:
        st.write("Generating 100 individuals...")

        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)

        individuals = []
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f"Iteration {i+1}")
            bar.progress(i + 1)
            ind = matIndividual(problem=target_problem)
            ind.evaluate()
            individuals.append(ind)
            time.sleep(0.03)  # UI smoothness

        st.session_state.individuals = individuals
        st.session_state.generated = True
        "...and now we're done!"

    if st.session_state.generated:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.write("Review them")
            if not st.session_state.sorted:
                st.button("Sort them", on_click=click_button_sorted)
        ix = st.slider("Display element", 0, 99)
        data = st.session_state.individuals[ix].state.astype(int)
        columns = ("Squad %d" % i for i in range(data.shape[1]))
        index = ["Cell %d" % i for i in range(data.shape[0])]
        index[-1] = "Courtyard"
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df_pretty = df.map(lambda x: prettydf(x))

        column_config = {col: st.column_config(disabled=True) for col in columns}

        st.dataframe(df_pretty, use_container_width=True, column_config=column_config)
        st.metric(
            label="Fitness value", value=int(st.session_state.individuals[ix].fitness)
        )
else:
    st.write("Visit Home page first !")
