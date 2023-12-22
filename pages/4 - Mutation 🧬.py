import time
from copy import deepcopy

import streamlit as st
import pandas as pd

from toolkit import matIndividual, problem, prettydf, state_generator


def click_button():
    st.session_state.clicked_mutation = True


def on_click_another_mutation():
    st.session_state.mutated = False


def click_button_mutate():
    st.session_state.mutated = True


def on_click_another_ind():
    st.session_state.clicked_mutation = False
    st.session_state.generated_mutation = False
    on_click_another_mutation()


with st.expander("Idea behind mutations 💡"):
    st.caption(
        "The general idea is to, with randomness, move prisoners from cell to courtyard or from"
        "courtyard to cell, whenever it's possible"
    )

if "loaded" in st.session_state:
    if st.session_state.generated_random_problem:
        target_problem = st.session_state.problem
    else:
        target_problem = problem
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button(
            "Generate individual to mutate",
            on_click=click_button,
            disabled=st.session_state.generated_mutation,
        )

    if st.session_state.clicked_mutation and not st.session_state.generated_mutation:
        with st.spinner("Generating..."):
            # Update the progress bar with each iteration.
            ind = matIndividual(problem=target_problem)
            ind.evaluate()
            individual = ind
            time.sleep(1)  # UI smoothness
        st.session_state.individual = individual
        st.session_state.generated_mutation = True
        "...and now we're done!"

    if st.session_state.generated_mutation:
        st.write("Mutate it")
        data = st.session_state.individual.state.astype(int)
        columns = ("Squad %d" % i for i in range(data.shape[1]))
        index = ["Cell %d" % i for i in range(data.shape[0])]
        index[-1] = "Courtyard"
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df_pretty = df.map(lambda x: prettydf(x))

        column_config = {col: st.column_config(disabled=True) for col in columns}

        st.dataframe(df_pretty, use_container_width=True, column_config=column_config)

        st.metric(label="Fitness value", value=int(st.session_state.individual.fitness))
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Regenerate an individual", on_click=on_click_another_ind)

        if not st.session_state.mutated:
            mutation_rate = st.slider("Mutation rate proportion", 0, 100, 100)
            mutation_amount = st.slider("Mutation rate amount", 0, 100, 100)
            st.session_state.mutation_rate = mutation_rate / 100
            st.session_state.mutation_amount = mutation_amount / 100
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                st.button(
                    "Mutate",
                    on_click=click_button_mutate,
                    disabled=st.session_state.mutated,
                )
        else:
            mutated_ind = deepcopy(st.session_state.individual)

            logs = mutated_ind.mutate(
                st.session_state.mutation_rate, st.session_state.mutation_amount
            )
            mutated_ind.evaluate()
            st.session_state.mutated_individual = mutated_ind
            st.session_state.logs = logs
            with st.expander("See mutation logs"):
                st.write(st.session_state.logs)
            data = st.session_state.mutated_individual.state.astype(int)
            columns = ("Squad %d" % i for i in range(data.shape[1]))
            index = ["Cell %d" % i for i in range(data.shape[0])]
            index[-1] = "Courtyard"
            df = pd.DataFrame(data=data, columns=columns, index=index)
            df_pretty = df.map(lambda x: prettydf(x))

            column_config = {col: st.column_config(disabled=True) for col in columns}

            st.dataframe(
                df_pretty, use_container_width=True, column_config=column_config
            )

            st.metric(
                label="New Fitness value",
                value=int(st.session_state.mutated_individual.fitness),
            )
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button("Make another mutation", on_click=on_click_another_mutation)
else:
    st.write("Visit Home page first !")
