import time
from copy import deepcopy

import pandas as pd
import streamlit as st

from toolkit import matIndividual, prettydf, problem

st.set_page_config(
    page_title="🧬 Algorithms",
)


def click_button():
    st.session_state.clicked_featurecross = True


def on_click_another_featurecross():
    st.session_state.featurecrossed = False


def click_button_featurecross():
    st.session_state.featurecrossed = True


def on_click_another_ind():
    st.session_state.clicked_featurecross = False
    st.session_state.generated_featurecross = False
    on_click_another_featurecross()


with st.expander("Idea behind feature crossing💡"):
    st.caption(
        "The general idea is to take, with randomness, a cell from parent 1 or from parent 2, starting from parent 1"
        " cells fillings. As sometimes some amount of prisoners lack in some cell, e.g some prisoners from cell of parent 2 are "
        "more or less than parent 1, there is a difference. "
        "Hence the courtyard is analyzed to see if some prisoners can be moved in or out from courtyard to cell to compensate the difference."
    )

if "loaded" in st.session_state:
    if st.session_state.generated_random_problem:
        target_problem = st.session_state.problem
    else:
        target_problem = problem

    col1, col2, col3 = st.columns(3)
    with col2:
        st.button(
            "Generate individual to recombine",
            on_click=click_button,
            disabled=st.session_state.generated_featurecross,
        )

    if (
        st.session_state.clicked_featurecross
        and not st.session_state.generated_featurecross
    ):
        with st.spinner("Generating..."):
            ind_1 = matIndividual(problem=target_problem)
            ind_1.evaluate()
            individual_1 = ind_1
            ind_2 = matIndividual(problem=target_problem)
            ind_2.evaluate()
            individual_2 = ind_2
            time.sleep(1)  # UI smoothness
        st.session_state.individual_1 = individual_1
        st.session_state.individual_2 = individual_2
        st.session_state.generated_featurecross = True
        "...and now we're done!"

    if st.session_state.generated_featurecross:
        st.write("Recombine them")
        parent1_col, parent2_col = st.columns(2)
        with parent1_col:
            st.write("Parent 1")
            data = st.session_state.individual_1.state.astype(int)
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
                label="Fitness value", value=int(st.session_state.individual_1.fitness)
            )
        with parent2_col:
            st.write("Parent 2")
            data = st.session_state.individual_2.state.astype(int)
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
                label="Fitness value", value=int(st.session_state.individual_2.fitness)
            )
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Regenerate parents individuals", on_click=on_click_another_ind)

        if not st.session_state.featurecrossed:
            mutation_rate = st.slider("Mutation rate proportion", 0, 100, 100)
            st.session_state.mutation_rate_featurecross = mutation_rate / 100
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                st.button(
                    "Recombine",
                    on_click=click_button_featurecross,
                    disabled=st.session_state.featurecrossed,
                )
        else:
            child_ind = deepcopy(st.session_state.individual_1)
            mixinInd = deepcopy(st.session_state.individual_2)

            logs = child_ind.crossover(
                mixinInd=mixinInd, rate_prop=st.session_state.mutation_rate_featurecross
            )
            child_ind.evaluate()
            st.session_state.featurecrossed_individual = child_ind
            st.session_state.logs_featurecrossed = logs
            with st.expander("See mutation logs"):
                st.write(["Other: Parent 2 "] + st.session_state.logs_featurecrossed)
            data = st.session_state.featurecrossed_individual.state.astype(int)
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
                value=int(st.session_state.featurecrossed_individual.fitness),
            )
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button(
                    "Make another recombination", on_click=on_click_another_featurecross
                )
else:
    st.write("Visit Home page first !")
