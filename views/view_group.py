import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
# from streamlit_extras.metric_cards import style_metric_cards
## My custom funcs and py files
import control.misc_funcs as misc
import control.db_connection as dbc

# Sanity check on the db connection object
if "__conn" not in st.session_state:
    conn = dbc.init_connection()
    st.session_state['__conn'] = conn
else:
    conn = st.session_state['__conn']


st.header(":thermometer: Informe Reputacional - Visão Grupo")

# TODO Might incorporate a select box where the user chooses which data will be analyzed, and which date to look to (maybe)
view_choice = 'reputacao_grupo_15dias'
# date_to_query = datetime.today().date()
df_response = dbc.load_data(conn, view_choice)
# df_response['dia'] = pd.to_datetime()

# Prepping tables and values to build visualizations
df_big_numbers = df_response[['dia', 'favorabilidade', 'saudabilidade', 'reputacao']].copy()
df_big_numbers
min_date = df_response['dia'].min().date() # this is necessary to limit dataviz to the existing days in the data 
# st.write(min_date.date())
### User input section
with st.container(border=True):
    # col_place, col_date = st.columns([0.5, 0.5], gap='small', vertical_alignment='top')
    # sel_business = st.selectbox(
    #     "Selecione uma Empresa:",
    #     ("Distribuição", "Saneamento", "Serviços", "Eólica", "Solar"),
    #     index=None,
    #     placeholder="Selecione uma opção",
    # )
    # with col_place:
    #     sel_place = st.selectbox(
    #         "Selecione uma Praça:",
    #         ("AL", "AP", "GO", "MA", "PA", "PI", "RS"),
    #         index=None,
    #         placeholder="Selecione uma opção",
    #     )
    # with col_date:
    # min_date = datetime.fromisoformat(df_response['dia'].min())
    sel_date = st.date_input(
        label="Selecione o dia:",
        value=datetime.today().date(),
        min_value=min_date,
        max_value=datetime.today().date(),
        )
sel_date_dtime = pd.to_datetime(sel_date)
# st.write(test_sel_date.date())
# st.write(pd.to_datetime(sel_date))
# st.write(df_big_numbers['dia'][1].date())
## Reputation
mask_selected_date = df_big_numbers['dia'] == sel_date_dtime
mask_previous_date = df_big_numbers['dia'] == (sel_date_dtime - timedelta(days=1))

today_rep = df_big_numbers[mask_selected_date]['reputacao'].iloc[0]
today_rep
yesterday_rep = df_big_numbers[mask_previous_date]['reputacao'].iloc[0]
yesterday_rep
# color_today_rep = misc.pick_color(today_rep/100)
## Favorability
today_fav = df_big_numbers[mask_selected_date]['favorabilidade'].iloc[0]
yesterday_fav = df_big_numbers[mask_previous_date]['favorabilidade'].iloc[0]
today_fav
yesterday_fav
# color_today_fav = misc.pick_color(today_fav/100)
## Saudability
today_saud = df_big_numbers[mask_selected_date]['saudabilidade'].iloc[0]
yesterday_saud = df_big_numbers[mask_previous_date]['saudabilidade'].iloc[0]
# color_today_saud = misc.pick_color(today_saud/100)

# min_date = datetime.fromisoformat(df_response['dia'].min())
# df_response
# min_date

# Choosing the color of the bullet bar based on the value entered
# bullet_color = misc.pick_color(today_rep)

### First part of the core dashboard visuals
col1, col2, col3 = st.columns([0.3,0.3,0.4], gap='small',)
with col1:
    st.markdown(':newspaper: **FAV**')
    st.metric(label='FAV', value=today_fav, delta="{:.2f}".format(today_fav-yesterday_fav), label_visibility='collapsed')
with col2:
    st.markdown(':iphone: **SAUD**')
    st.metric(label='SAUD', value=today_saud, delta="{:.2f}".format(today_saud-yesterday_saud), label_visibility='collapsed')
with col3:
    pass
    # #displaying the thermometer in shape of a gauge
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
    # gauge_fig.update_layout(height=300, width=300)
    # st.plotly_chart(gauge_fig, use_container_width=False)
col_pos, col_neg = st.columns([0.5, 0.5])
with col_pos:
    st.markdown("""
    #### :thumbsup: :blue[Pontos Positivos]
    **Imprensa**: _dolorem ipsum quia dolor sit amet_

    **Digital**: _consectetur, adipisci velit_
    """)
with col_neg:
    st.markdown("""
        #### :warning: :orange[Pontos de Atenção]: 
        **Imprensa**: _dolorem ipsum quia dolor sit amet_

        **Digital**: _consectetur, adipisci velit_
        """)
