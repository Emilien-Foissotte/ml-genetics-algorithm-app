import time

import pandas as pd
import streamlit as st

from toolkit import matPopulation, prettydf, problem

st.set_page_config(
    page_title="🧬 Algorithms",
)


def click_button_generate():
    st.session_state.clicked_generation_evolution = True


def click_button_evolve():
    with st.spinner("Evolution in progress.."):
        ingredients_fillings = st.session_state.population
        ingredients_fillings.evaluate()
        ingredients_fillings.sort()
        for i in range(15):
            ingredients_fillings.enhance()
            if ingredients_fillings.best[-1].fitness == st.session_state.max_capa:
                break
            if (
                i > 6
                and ingredients_fillings.best[-1].fitness
                == ingredients_fillings.best[-2].fitness
                == ingredients_fillings.best[-3].fitness
            ):
                break
    st.session_state.max_iteration = i
    st.session_state.evolved = True


def on_click_another_evolution():
    st.session_state.clicked_generation_evolution = False
    st.session_state.generated_evolution = False
    st.session_state.evolved = False


with st.expander("Idea behind evolution💡"):
    st.caption(
        "The general idea is to create a sample of generated individuals, play with odds "
        " by creating some mutations and feature crossing in genome space, evaluate them. Then we choose a"
        " subsample of individuals with a fitness-based selection law, but with randomnes to explore solutions"
        " and then repeat, until there is no evolution or global maximum have been found."
    )

if "loaded" in st.session_state:
    if st.session_state.generated_random_problem:
        target_problem = st.session_state.problem
    else:
        target_problem = problem

    cell_capacity = 0
    for cell in target_problem["capacity"].keys():
        if cell != "courtyard":
            cell_capacity += target_problem["capacity"][cell]
    st.session_state.max_capa = cell_capacity
    st.metric(label="Max cells capacity", value=st.session_state.max_capa)

    if not st.session_state.generated_evolution:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button(
                "Generate a population",
                on_click=click_button_generate,
                disabled=st.session_state.generated,
            )
        size = st.slider("Choose size of population", 1, 100, 50)
        st.session_state.size = size
        mutation_rate = st.slider("Mutation rate proportion", 0, 100, 50)
        st.session_state.mutation_rate = mutation_rate

    if (
        st.session_state.clicked_generation_evolution
        and not st.session_state.generated_evolution
    ):
        with st.spinner("Generating population.."):
            population = matPopulation(
                problem=target_problem,
                size=st.session_state.size,
                rate_prop=st.session_state.mutation_rate / 100,
            )
            time.sleep(1)
            st.session_state.population = population
            st.session_state.generated_evolution = True
        "...and now we're done!"

    if st.session_state.generated_evolution:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button(
                "Let's Evolve",
                on_click=click_button_evolve,
                disabled=st.session_state.evolved,
            )

    if st.session_state.evolved:
        st.write("Review the evolution process")
        fitness_values = [
            best_ind.fitness for best_ind in st.session_state.population.best
        ]
        target_values = [
            st.session_state.max_capa for best_ind in st.session_state.population.best
        ]
        charts = {
            "iteration": range(len(fitness_values)),
            "fitness_values": fitness_values,
            "target_values": target_values,
        }

        chart_data = pd.DataFrame(data=charts)

        st.line_chart(data=chart_data, x="iteration", color=["#0000FF", "#FF0000"])
        with st.expander("Review best individuals", expanded=True):
            ix = st.slider(
                "Display best element of iteration",
                0,
                min(99, st.session_state.max_iteration + 1),
            )
            data = st.session_state.population.best[ix].state.astype(int)
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
                label="Fitness value",
                value=int(st.session_state.population.best[ix].fitness),
            )
        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("Make another evolution", on_click=on_click_another_evolution)
else:
    st.write("Visit Home page first !")
