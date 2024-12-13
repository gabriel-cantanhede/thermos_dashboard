import streamlit as st
import plotly.graph_objects as go
from datetime import date
import control.misc_funcs as misc
import control.db_connection as dbc
import time


# Connecting to Supabase
if '__conn' not in st.session_state.keys():
    conn = dbc.init_connection()
    st.session_state['__conn'] = conn
else:
    conn = st.session_state['__conn']

# Loading data from supabase

try:
    with st.sidebar:
        # sel_business = st.selectbox(
        #     label="Selecione uma Empresa:",
        #     options=("Distribuição", "Saneamento", "Serviços", "Eólica", "Solar"),
        #     index=0,
        #     placeholder="Selecione uma opção",
        # )
        multisel_place = st.multiselect(
            label="Selecione uma Praça:",
            options=("AL", "AP", "GO", "MA", "PA", "PI", "RS"),
            default=("AL", "AP", "GO", "MA", "PA", "PI", "RS"),
            placeholder="Selecione quantas praças deseja ver",
        )
        sel_date = st.date_input(
            label="Selecione o dia:",
            value=date.today(),
            min_value=date(2023,9,28),
            max_value=date.today(),
        )


    st.markdown("# Termômetro Reputacional :thermometer:",unsafe_allow_html=True )
    #mockup input field, just to simulate values in the thermometer more flexibly

    # Choosing the color of the bullet bar based on the value entered
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
        for place in multisel_place:

            st.markdown(f"## **Equatorial - {place}**")
            st.markdown(f"### **Data: :blue[{sel_date.day}/{sel_date.month}/{sel_date.year}]**")

            # input_num = st.number_input("Valor", min_value=0, max_value=100, key=place)
            # bullet_color = misc.pick_color(input_num)

            ### First part of the core dashboard visuals
            col1, col2, col3, col4 = st.columns([0.3,0.2,0.2,0.4], vertical_alignment='center')
            with col1:
                st.markdown("""
                #### :thumbsup: :blue[Pontos Positivos]
                Imprensa: _dolorem ipsum quia dolor sit amet_
                
                Digital: _consectetur, adipisci velit_
                """)
            with col2:
                st.markdown(':newspaper: **SAUD**')
                # st.metric(label='SAUD', value=65, delta=-15, label_visibility='collapsed')
            with col3:
                st.markdown(':iphone: **FAV**')
                # st.metric(label='FAV', value=78, delta=12, label_visibility='collapsed')
            # with col4:
                #displaying the thermometer in shape of a gauge
                # gauge_fig = go.Figure(go.Indicator(
                #     mode = "gauge+number",
                #     value = input_num,
                #     number= {"suffix":"%"},
                #     title = {'text': "Como estamos hoje?"},
                #     uid="favorability_avg",
                #     gauge = {
                #         'shape':'angular',
                #         'axis': {'range': [0, 100], 'tickvals':[0,35,70,100]}, # to place text instead of numbers: ticktext:[text list]
                #         'bar': {'color': bullet_color, 'thickness':0.8, 'line':{'color':'black', 'width':2}},
                #         'bordercolor':'white',
                #         'borderwidth':1,
                #         'steps': [
                #             {'range': [0, 35], 'color': 'red'},
                #             {'range': [35, 70], 'color': 'yellow'},
                #             {'range': [70, 100], 'color': 'green'}
                #         ]},
                #     ))
                # gauge_fig.update_layout(height=400, width=400)
                # st.plotly_chart(gauge_fig, use_container_width=False)
            # st.markdown("""
            #     #### :warning: :orange[Pontos de Atenção]:
            #     Imprensa: _dolorem ipsum quia dolor sit amet_
                
            #     Digital: _consectetur, adipisci velit_
            #     """)
except Exception as e:
    st.error("Falha ao recuperar dados do termômetro, tente logar novamente.")
    time.sleep(5)
    st.switch_page('views/user_login.py')
