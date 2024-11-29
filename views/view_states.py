import streamlit as st
import plotly.graph_objects as go
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards

with st.sidebar:
    sel_business = st.selectbox(
        "Selecione uma Empresa:",
        ("Distribuição", "Saneamento", "Serviços", "Eólica", "Solar"),
        index=None,
        placeholder="Selecione uma opção",
    )
    sel_place = st.selectbox(
        "Selecione uma Praça:",
        ("AL", "AP", "GO", "MA", "PA", "PI", "RS"),
        index=None,
        placeholder="Selecione uma opção",
    )
    sel_date = st.date_input(
        label="Selecione o dia:",
        value=date.today(),
        min_value=date(2023,9,28),
        max_value=date.today(),
        
    )

st.markdown("# Termômetro Reputacional :thermometer:",unsafe_allow_html=True )
#mockup input field, just to simulate values in the thermometer more flexibly
input_num = st.number_input("Valor", min_value=0, max_value=100)

# Choosing the color of the bullet bar based on the value entered
bullet_color = None
if input_num <=35:
    bullet_color = "red"
elif input_num <= 70:
    bullet_color = "yellow"
else:
    bullet_color = "green" 

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
