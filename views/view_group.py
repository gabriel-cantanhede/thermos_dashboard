import streamlit as st
import plotly.graph_objects as go
from datetime import date
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

# TODO Might incorporate a select box where the user chooses which data will be analyzed, and which date to look to (maybe)
view_choice = 'reputacao_grupo_15dias'
# date_to_query = datetime.today().date()
df_response = dbc.load_data(conn, view_choice)
# st.write(df_response) # OG Debugging


# Prepping tables and values to build visualizations
df_big_numbers = df_response[['dia', 'favorabilidade', 'saudabilidade', 'reputacao']].copy()
## Reputation
today_rep = df_big_numbers.iloc[0]['reputacao']
yesterday_rep = df_big_numbers.iloc[1]['reputacao']
color_today_rep = misc.pick_color(today_rep/100)
## Favorability
today_fav = df_big_numbers.iloc[0]['favorabilidade']
yesterday_fav = df_big_numbers.iloc[1]['favorabilidade']
color_today_fav = misc.pick_color(today_fav/100)
## Saudability
today_saud = df_big_numbers.iloc[0]['saudabilidade']
yesterday_saud = df_big_numbers.iloc[1]['saudabilidade']
color_today_saud = misc.pick_color(today_saud/100)


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
    sel_date = st.date_input(
        label="Selecione o dia:",
        value=date.today(),
        min_value=date(2023,9,28),
        max_value=date.today(),
        
        )

st.markdown("# Informe Reputacional - Visão Grupo :thermometer:",unsafe_allow_html=True )
#mockup input field, just to simulate values in the thermometer more flexibly
# input_num = st.number_input("Valor", min_value=0, max_value=100)

# Choosing the color of the bullet bar based on the value entered
bullet_color = misc.pick_color(input_num)

### First part of the core dashboard visuals
col1, col2, col3 = st.columns([0.3,0.3,0.4], gap='small',)
with col1:
    st.markdown(':newspaper: **SAUD**')
    st.metric(label='SAUD', value=65, delta=-15, label_visibility='collapsed')
    style_metric_cards()
with col2:
    st.markdown(':iphone: **FAV**')
    st.metric(label='FAV', value=78, delta=12, label_visibility='collapsed')
with col3:
    #displaying the thermometer in shape of a gauge
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = input_num,
        number= {"suffix":"%"},
        title = {'text': "Como estamos hoje?"},
        uid="favorability_avg",
        gauge = {
            'shape':'angular',
            'axis': {'range': [0, 100], 'tickvals':[0,35,70,100]}, # to place text instead of numbers: ticktext:[text list]
            'bar': {'color': bullet_color, 'thickness':0.8, 'line':{'color':'black', 'width':2}},
            'bordercolor':'white',
            'borderwidth':1,
            'steps': [
                {'range': [0, 35], 'color': 'red'},
                {'range': [35, 70], 'color': 'yellow'},
                {'range': [70, 100], 'color': 'green'}
            ]},
        ))
    gauge_fig.update_layout(height=300, width=300)
    st.plotly_chart(gauge_fig, use_container_width=False)
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
