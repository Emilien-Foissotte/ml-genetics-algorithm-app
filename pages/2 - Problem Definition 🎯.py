import json

import numpy as np
import pandas as pd
import streamlit as st

from toolkit import prettydf_compatibility, problem, problem_generator

st.set_page_config(
    page_title="🧬 Algorithms",
)


def on_click_random_problem():
    st.session_state.generated_random_problem = True
    random_problem = problem_generator(
        num_squads=num_squad, num_cells=num_cell, num_prisoners=num_prisoners
    )
    st.session_state.problem = random_problem


def on_click_load_problem(file):
    loaded_problem = json.load(file)
    st.session_state.problem = loaded_problem
    st.session_state.generated_random_problem = True


@st.cache_data
def dump_json(file):
    if file is not None:
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return json.dumps(file, indent=2)
    else:
        return ""


if "loaded" in st.session_state:
    with st.expander("See blog post problem definition"):
        st.write(problem)

    num_squad = st.slider("Number of squads", 4, 7, 4)
    num_prisoners = st.slider("Approx. size of squads", 5, 15, 8)
    num_cell = st.slider("Number of cells", 4, 7, 4)
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.session_state.generated_random_problem:
            text_generation = "Regenerate custom problem"
        else:
            text_generation = "Generate custom problem"
        st.button(text_generation, on_click=on_click_random_problem)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        st.write("Or")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.generated_random_problem:
            text_loading = "Reload a custom problem"
        else:
            text_loading = "Load a custom problem"
        uploaded_file = st.file_uploader(text_loading, type="json")
        if uploaded_file is not None:
            on_click_load_problem(uploaded_file)
    with col2:
        if "problem" in st.session_state:
            saved_data = dump_json(st.session_state.problem)
        else:
            saved_data = ""
        st.download_button(
            label="Download data as CSV",
            data=saved_data,
            file_name="saved_problem.json",
            mime="application/json",
            disabled=not st.session_state.generated_random_problem,
        )
    if st.session_state.generated_random_problem:
        with st.expander("Review custom problem"):
            st.write("Population of squads :")
            squads = [num for num in st.session_state.problem["arrest"]]
            mens = [st.session_state.problem["arrest"][squad] for squad in squads]
            chart_data = chart_data = pd.DataFrame(
                {"squads": squads, "population": mens}
            )
            st.bar_chart(chart_data, x="squads", y="population")
            st.write("Matrix compatibility :")
            cells = [cell for cell in st.session_state.problem["cells"]]
            data = np.zeros((len(cells), len(squads)), dtype=int)
            for i, cell in enumerate(cells):
                for j, squad in enumerate(squads):
                    if squad in st.session_state.problem["compatibility"][cell]:
                        data[i][j] = 1
            columns = ("Squad %d" % i for i in range(data.shape[1]))
            index = ["Cell %d" % i for i in range(data.shape[0])]
            index[-1] = "Courtyard"
            df = pd.DataFrame(data=data, columns=columns, index=index)
            df_pretty = df.map(lambda x: prettydf_compatibility(x))
            column_config = {col: st.column_config(disabled=True) for col in columns}
            st.dataframe(
                df_pretty, use_container_width=True, column_config=column_config
            )
            cells.remove("courtyard")

            st.write("Capacity of cells :")
            capas = [st.session_state.problem["capacity"][cell] for cell in cells]
            chart_data = pd.DataFrame({"cells": cells, "capacity": capas})
            st.bar_chart(chart_data, x="cells", y="capacity")
            cell_capacity = 0
            for cell in st.session_state.problem["capacity"].keys():
                if cell != "courtyard":
                    cell_capacity += st.session_state.problem["capacity"][cell]
            st.metric(label="Max cells capacity", value=cell_capacity)

            st.write("Json representation :")
            st.write(st.session_state.problem)

else:
    st.write("Visit Home page first !")
