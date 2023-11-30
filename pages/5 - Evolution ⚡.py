from toolkit import matPopulation, problem, prettydf

import streamlit as st
import pandas as pd
import time

st.set_page_config(
        page_title="Generation ⚙️",
)

def click_button_generate():
    st.session_state.clicked_generation_evolution = True

def click_button_evolve():
    with st.spinner("Evolution in progress.."):
        ingredients_fillings = st.session_state.population
        ingredients_fillings.evaluate()
        ingredients_fillings.sort()
        for i in range(100):
            ingredients_fillings.enhance()
            if ingredients_fillings.best[-1].fitness == st.session_state.max_capa:
                break
    st.session_state.max_iteration = i
    st.session_state.evolved = True

def on_click_another_evolution():
    st.session_state.clicked_generation_evolution = False
    st.session_state.generated_evolution = False
    st.session_state.evolved = False


if 'loaded' in st.session_state:
    cell_capacity = 0
    for cell in problem["capacity"].keys():
        if cell != "courtyard":
            cell_capacity += problem["capacity"][cell]
    st.session_state.max_capa = cell_capacity
    st.metric(label="Max tanks capacity", value=st.session_state.max_capa)
   
    if not st.session_state.generated_evolution:  
        st.button('Generate a population', on_click=click_button_generate, disabled=st.session_state.generated)
        size = st.slider("Choose size of population", 1, 100, 100)
        st.session_state.size = size

    if st.session_state.clicked_generation_evolution and not st.session_state.generated_evolution:
        with st.spinner("Generating population.."):
            population = matPopulation(problem=problem, size=st.session_state.size)
            time.sleep(1)
            st.session_state.population = population
            st.session_state.generated_evolution = True
        '...and now we\'re done!'

    if st.session_state.generated_evolution:
        st.button("Let's Evolve", on_click=click_button_evolve, disabled=st.session_state.evolved)
        
    if st.session_state.evolved:
        st.write("Review the evolution process")
        fitness_values = [best_ind.fitness for best_ind in st.session_state.population.best]
            
        chart_data = pd.DataFrame(data=fitness_values)
            
        st.line_chart(data=chart_data)
        with st.expander("Review best individuals"): 
            ix = st.slider("Display best element of iteration", 0, min(99, st.session_state.max_iteration + 1))
            data = st.session_state.population.best[ix].state.astype(int)
            columns=("Squad %d" % i for i in range(data.shape[1]))
            index=["Cell %d" % i for i in range(data.shape[0])]
            index[-1] = "Warehouse"
            df =  pd.DataFrame(data=data, columns=columns, index=index)
            df_pretty = df.map(lambda x: prettydf(x))

            column_config = {col: st.column_config(disabled=True) for col in columns}

            st.dataframe(df_pretty, use_container_width=True, column_config=column_config)

            st.metric(
                label="Fitness value",
                value=int(st.session_state.population.best[ix].fitness)
            )
        st.button("Make another evolution", on_click=on_click_another_evolution)
else:
    st.write("Visit Home page first !")






