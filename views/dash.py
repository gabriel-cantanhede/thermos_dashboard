import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
# from streamlit_extras.metric_cards import style_metric_cards

# My custom funcs and py files
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
today_rep = df_big_numbers.iloc[0]['reputacao']
yesterday_rep = df_big_numbers.iloc[1]['reputacao']
color_today_rep = misc.pick_color(today_rep/100)

#### Visualizations 

### Line chart showing the trends for overall favorability over the year
with st.container(border=True):
    #### Visualizations 
    ### Line chart showing the trends for overall favorability over the year
    fig_line = px.line(
        df_big_numbers,
        x='dia',
        y=['reputacao', 'favorabilidade', 'saudabilidade'],
        labels=dict(variable="KPI",value="Valor", dia="Dia", reputacao="Reputação"),
        hover_data={"dia": "|%m-%d-%Y"},
        color_discrete_sequence=['blue', 'green', 'orange'],
        )
        # text='reputacao')

    count_days = df_big_numbers['dia'].count()

    fig_line.add_trace(go.Scatter(
                            x=df_big_numbers['dia'], 
                            y=[70] * count_days,
                            legendgroup='group2', 
                            mode='lines',
                            name='Média', 
                            line=dict(color='gold', width=4, dash='dashdot')))
    fig_line.add_trace(go.Scatter(
                            x=df_big_numbers['dia'], 
                            y=[35] * count_days,
                            legendgroup='group2',
                            legendgrouptitle_text='Referência',
                            mode='lines',
                            name='Baixa', 
                            line=dict(color='red', width=4, dash='dashdot')))


    name_viz = "Reputação do grupo nos últimos 15 dias" if view_choice == 'reputacao_grupo_15dias' else "Reputação do Grupo"
    st.subheader(name_viz)
    fig_line.update_layout(
        # title={"text":name_viz},
        legend_title_text='KPIs',
        autosize=True,
        # width=800,
        # height=600,
        margin=dict(
            l=100,
            r=100,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(title_text="", ticks="outside"),
        yaxis=dict(title_text="Desempenho (%)", ticks="outside"),)

    # These lines are fucking kickass!! They literally make the line chart fucking lit
    # by adding handy buttons to the top to show certain date intervals, and if that wasn't fucking enought
    # it also adds a sliding window selector to the bottom of the chart, with a fucking miniature of the chart!!!! 
    fig_line.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    # dict(count=1,
                    #      label="YTD",
                    #      step="year",
                    #      stepmode="todate"),
                    # dict(count=1,
                    #      label="1 ano",
                    #      step="year",
                    #      stepmode="backward"),
                    dict(label="Tudo",
                        step="all")
                ])
            ),
            # It's cluttering the visuals a bit, uncomment if deemed necessary
            # rangeslider=dict(
            #     visible=True
            # ),
            type="date"
        ))

    st.plotly_chart(fig_line)



with st.container(border=True):
    st.subheader("Reputação (hoje vs. ontem)")
    fig_today = go.Figure(go.Indicator(
        mode = "number+gauge+delta", value = today_rep,
        domain = {'x': [0.1, 1], 'y': [0, 1]},
        # title = {'text' :"<b>Reputação<br> (hoje <br>vs. <br>ontem)</b> ", 'font':{'size':20}},
        delta = {'reference': yesterday_rep, "valueformat":'.2'},
        number = {'suffix':'%','font':{'size':60}, 'font':{'color':color_today_rep}},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [None, 100]},
            # 'threshold': {
            #     'line': {'color': "black", 'width': 2},
            #     'thickness': 0.75,
            #     'value': yesterday_fav},
            'steps': [
                {'range': [0, 35], 'color': "#F58A67"},
                {'range': [35, 70], 'color': "#F0D16E"},
                {'range': [70, 100], 'color': "#89F067"},
                ],
            'bar': {'color': color_today_rep, 'thickness':0.5, 'line':{'color':'black', 'width':1}}
                }))
    fig_today.update_layout(height = 300, width=1000)
    st.plotly_chart(fig_today)    


# st.dataframe(df_data_thermos)
