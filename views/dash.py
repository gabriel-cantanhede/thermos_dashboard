import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time
# from streamlit_extras.metric_cards import style_metric_cards

# My custom funcs and py files
import control.misc_funcs as misc
import control.db_connection as dbc

conn = None
# Sanity check on the db connection object
if "__conn" not in st.session_state:
    conn = dbc.init_connection()
    st.session_state['__conn'] = conn
else:
    conn = st.session_state['__conn']

try:
    # TODO Might incorporate a select box where the user chooses which data will be analyzed, and which date to look to (maybe)
    view_group_choice = 'reputacao_grupo_15dias'
    # date_to_query = datetime.today().date()
    df_response = dbc.load_data(conn, view_group_choice)
    # df_response['dia'] = pd.to_datetime(df_response['dia']).dt.date.astype('datetime64[ns]')
    # st.write(df_response) # OG Debugging


    # Prepping tables and values to build visualizations
    df_big_numbers = df_response[['dia', 'favorabilidade', 'saudabilidade', 'reputacao']].copy()

    view_states_choice = 'reputacao_estados_15dias'
    df_response_states = dbc.load_data(conn, view_states_choice)
    # df_big_numbers_states

    # Retrieving most recent day in the dataset
    current_day_in_data = df_big_numbers.iat[0,0].date()
    # current_day_in_data

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


    #### Visualizations 
    name_viz = ":chart_with_upwards_trend: KPIs de Reputação (:blue[_últimos 15 dias_])" if view_group_choice == 'reputacao_grupo_15dias' else "Reputação do Grupo"
    st.header(name_viz, divider='blue')

    ### Line chart showing the trends for overall favorability over the year
    with st.container(border=True):
        #### Visualizations 
        ### Line chart showing the trends for overall favorability over the year
        count_days = df_big_numbers['dia'].count()
        fig_line = go.Figure(
            data=[
                go.Scatter(
                    x= df_big_numbers['dia'],
                    y= df_big_numbers['reputacao'],
                    # color=df_big_numbers['reputacao'],
                    name='Reputação',
                    mode='lines',
                    line=dict(color='#0714E1', width=5, dash='solid'),
                    legendgroup= 'group 1',
                    zorder=4,
                ),
                go.Scatter(
                    x= df_big_numbers['dia'],
                    y= df_big_numbers['favorabilidade'],
                    # color=df_big_numbers['reputacao'],
                    name='Favorabilidade',
                    mode='lines',
                    line=dict(color='#C30DE1', width=3, dash='solid'),
                    legendgroup= 'group 1',
                    zorder=3,
                ),
                go.Scatter(
                    x= df_big_numbers['dia'],
                    y= df_big_numbers['saudabilidade'],
                    # color=df_big_numbers['reputacao'],
                    name='Saudabilidade',
                    mode='lines',
                    line=dict(color='#7AE00B', width=3, dash='solid'),
                    legendgroup= 'group 1',
                    zorder=2,
                ),
                go.Scatter(
                    x=df_big_numbers['dia'], 
                    y=[70] * count_days,
                    legendgroup='group2', 
                    mode='lines',
                    name='Média', 
                    line=dict(color='gold', width=4, dash='dashdot'),
                    zorder=1,
                    ),
                go.Scatter(
                    x=df_big_numbers['dia'], 
                    y=[35] * count_days,
                    legendgroup='group2',
                    legendgrouptitle_text='Referência',
                    mode='lines',
                    name='Baixa', 
                    line=dict(color='red', width=4, dash='dashdot'),
                    zorder=0,
                    ),
                ]
            )

        fig_line.update_layout(
            # title={"text":name_viz},
            legend_title_text='Indicadores',
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
            xaxis=dict(title_text="Dias", ticks="outside"),
            yaxis=dict(title_text="Desempenho (%)", ticks="outside"),
            title=dict(
                    text='Desempenho dos indicadores de reputação do Grupo',
                    automargin=True,
                    font=dict(color='darkblue', size=20),
                    x=0.45,
                    y=0.9,
                    xanchor='center',
                    yanchor='top',))

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
                # This is the bit that adds the bottom date range slicing widget
                # It's cluttering the visuals a bit, uncomment if deemed necessary
                # rangeslider=dict(
                #     visible=True
                # ),
                type="date"
            ))
        # Reversing the trace order, for viz purposes
        # fig_line = fig_line.select_traces[:-1]

        st.plotly_chart(fig_line)



    st.header(f':bar_chart: Indicadores do dia :blue[{current_day_in_data:%d/%m/%y}] :gray[(_hoje vs. ontem_)]', divider='blue')
    with st.container(border=True):
        col_fav, col_saud = st.columns([0.5, 0.5], gap='small', vertical_alignment='center')
        ## Favorability Gauge 
        with col_fav:
            # st.subheader("Favorabilidade")
            fig_today_fav = go.Figure(go.Indicator(
                mode = "number+gauge+delta", value = today_fav,
                domain = {'x': [0.1, 1], 'y': [0, 1]},
                # title = {'text' :"<b>Reputação<br> (hoje <br>vs. <br>ontem)</b> ", 'font':{'size':20}},
                delta = {'reference': yesterday_fav, "valueformat":'+.2'},
                number = {'suffix':'%','font':{'size':60}, 'font':{'color':color_today_fav}},
                gauge = {
                    'shape': "bullet",
                    'axis': {'range': [None, 100], 'tickvals': [0,35,70,100]},
                    # 'threshold': {
                    #     'line': {'color': "black", 'width': 2},
                    #     'thickness': 0.75,
                    #     'value': yesterday_fav},
                    'steps': [
                        {'range': [0, 35], 'color': "#F58A67"},
                        {'range': [35, 70], 'color': "#F0D16E"},
                        {'range': [70, 100], 'color': "#89F067"},
                        ],
                    'bar': {'color': color_today_fav, 'thickness':0.5, 'line':{'color':'black', 'width':1}}
                        }))
            fig_today_fav.update_layout(
                height = 250,
                width=1000,
                title=dict(
                    text='Favorabilidade',
                    automargin=True,
                    font=dict(color='darkblue', size=25),
                    x=0.45,
                    y=0.85,
                    xanchor='center',
                    yanchor='top',))
                
            st.plotly_chart(fig_today_fav)

            # "# st.subheader("Saudabilidade")
        with col_saud:
            fig_today_saud = go.Figure(go.Indicator(
                mode = "number+gauge+delta", value = today_saud,
                domain = {'x': [0.1, 1], 'y': [0, 1]},
                # title = {'text' :"<b>Reputação<br> (hoje <br>vs. <br>ontem)</b> ", 'font':{'size':20}},
                delta = {'reference': yesterday_saud, "valueformat":'+.2'},
                number = {'suffix':'%','font':{'size':60}, 'font':{'color':color_today_saud}},
                gauge = {
                    'shape': "bullet",
                    'axis': {'range': [0, 100], 'tickvals': [0,35,70,100],},
                    # 'threshold': {
                    #     'line': {'color': "black", 'width': 2},
                    #     'thickness': 0.75,
                    #     'value': yesterday_fav},
                    'steps': [
                        {'range': [0, 35], 'color': "#F58A67"},
                        {'range': [35, 70], 'color': "#F0D16E"},
                        {'range': [70, 100], 'color': "#89F067"},
                        ],
                    'bar': {'color': color_today_saud, 'thickness':0.5, 'line':{'color':'black', 'width':1}}
                        }))
            fig_today_saud.update_layout(
                height= 250,
                width= 1000,
                title=dict(
                    text='Saudabilidade',
                    automargin=True,
                    font=dict(color='darkblue', size=25),
                    x=0.45,
                    y=0.85,
                    xanchor='center',
                    yanchor='top',))

            st.plotly_chart(fig_today_saud) 

        ## Reputation Gauge
        # st.markdown("### Reputação <br>(hoje vs. ontem)",unsafe_allow_html=True)
        fig_today_rep = go.Figure(go.Indicator(
            mode = "number+gauge+delta", value = today_rep,
            domain = {'x': [0.1, 1], 'y': [0, 1]},
            # title = {'text' :"<b>Reputação<br> (hoje <br>vs. <br>ontem)</b> ", 'font':{'size':20}},
            delta = {'reference': yesterday_rep, "valueformat":'+.2'},
            number = {'suffix':'%','font':{'size':60}, 'font':{'color':color_today_rep}},
            gauge = {
                'shape': "bullet",
                'axis': {'range': [None, 100], 'tickvals': [0,35,70,100]},
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
        fig_today_rep.update_layout(
            height = 280,
            width=1000,
            title=dict(
                text='Reputação',
                automargin=True,
                font=dict(color='darkblue', size=30),
                x=0.45,
                y=0.85,
                xanchor='center',
                yanchor='top',
                ))
        st.plotly_chart(fig_today_rep)
        st.markdown("_Obs.: O valor abaixo de cada percentual é a diferença entre o indicador de hoje e o do dia anterior_")

    
    st.header(":bar_chart: Big Numbers", divider='blue')
    with st.container(border=True):
        # df_big_numbers_states
        numeric_cols_press = [
            'total_noticias',
            'imprensa_positivas',
            'imprensa_negativas',
            ]
        numeric_cols_digital = [
            'total_mencoes',
            'digital_positivas',
            'digital_neutras',
            'digital_negativas',
            ]
        to_group_cols = [
            'dia',
            'estado',
            ]
        column_to_display_press = dict(
            estado='Estado',
            total_noticias='Total de Notícias',
            imprensa_positivas='Notícias Positivas',
            imprensa_negativas='Notícias Negativas',
            )
        column_to_display_dig = dict(
            estado='Estado',
            total_mencoes='Total de Menções (Digital)',
            digital_positivas='Menções Positivas',
            digital_neutras='Menções Neutras',
            digital_negativas='Menções Negativas',
            )
        min_date_num, max_date_num = df_response_states['dia'].min(), df_response_states['dia'].max()

        df_big_numbers_digital = df_response_states[to_group_cols + numeric_cols_digital].copy()
        df_big_numbers_press = df_response_states[to_group_cols + numeric_cols_press].copy()
        df_num_digital_grouped = df_big_numbers_digital.groupby(by=['estado'])
        df_num_press_grouped = df_big_numbers_press.groupby(by=['estado'])

        
        # st.dataframe(df_num_dig_grouped[numeric_cols_digital].sum(), column_config=column_to_display_dig, use_container_width=True,)
        col_bignum1, col_bignum2 = st.columns([0.5, 0.5], gap="small")
        with col_bignum1:
            # st.markdown("### Imprensa")
            # Plotting the big numbers as a stacked bar chart, to better enphasize magnitude
            df_sum_press = df_num_press_grouped[numeric_cols_press].sum().reset_index()

            fig_nums_press = go.Figure(data=[
                go.Bar(
                    name='Negativas',
                    x=df_sum_press['estado'],
                    y=df_sum_press['imprensa_negativas'],
                    text=df_sum_press['imprensa_negativas'], 
                    textposition='auto',
                    marker_color='#DD2100',),
                go.Bar(
                    name='Positivas', 
                    x=df_sum_press['estado'], 
                    y=df_sum_press['imprensa_positivas'], 
                    text=df_sum_press['imprensa_positivas'], 
                    textposition='auto',
                    marker_color='#0049F5',),
                ])
            fig_nums_press.update_layout(
                barmode='stack', 
                height = 550,
                title=dict(
                    text='Quantidade de notícias na imprensa',
                    automargin=True,
                    font=dict(color='darkblue', size=20),
                    x=0.45,
                    y=0.9,
                    xanchor='center',
                    yanchor='top',
                    ),
                yaxis=dict(title="Notícias"),
                xaxis=dict(title='Estados'),
                legend=dict(title='Notícias'),
                )
            
            st.plotly_chart(fig_nums_press)
             
        with col_bignum2:
            # st.markdown("### Digital")
            df_sum_digital = df_num_digital_grouped[numeric_cols_digital].sum().reset_index()
            # df_sum_digital
            fig_nums_dig = go.Figure(data=[
                go.Bar(
                    name='Negativas', 
                    x=df_sum_digital['estado'], 
                    y=df_sum_digital['digital_negativas'],
                    text=df_sum_digital['digital_negativas'],
                    marker_color='#DD2100', 
                    textposition='auto'),
                go.Bar(
                    name='Neutras', 
                    x=df_sum_digital['estado'], 
                    y=df_sum_digital['digital_neutras'],
                    text=df_sum_digital['digital_neutras'],
                    marker_color='#00AFBB', 
                    textposition='auto'),
                go.Bar(
                    name='Positivas', 
                    x=df_sum_digital['estado'], 
                    y=df_sum_digital['digital_positivas'],
                    marker_color='#0049F5',
                    text=df_sum_digital['digital_positivas'], 
                    textposition='auto'),
                ])


            fig_nums_dig.update_layout(
                barmode='stack', 
                height = 550,
                title=dict(
                    text='Quantidade de menções nas mídias digitais',
                    automargin=True,
                    font=dict(color='darkblue', size=20),
                    x=0.45,
                    y=0.9,
                    xanchor='center',
                    yanchor='top',
                    ),
                yaxis=dict(title="Menções"),
                xaxis=dict(title='Estados'),
                legend=dict(title='Menções'),
                )
            st.plotly_chart(fig_nums_dig)
        
        # Footnote for these charts
        st.markdown(f"_Obs.: Valores cumulativos referentes ao período entre :blue[{min_date_num.date():%d/%m}] e :blue[{max_date_num.date():%d/%m/%y}]_")

    ### Navigation Buttons
    with st.container():
        nav_prev, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
        # with nav_prev:
        #     st.page_link("views/dash.py", label=":arrow_left: Voltar",)
        with nav_next:
            st.page_link("views/view_group.py", label="Avançar :arrow_right:",)

except Exception as e:
    st.error("Falha ao recuperar dados do termômetro, tente logar novamente.")
    #TODO spinning wheel with a message (redirecionando em 10s - dynamic coountdown)
    e
#     # time.sleep(10)
#     # st.switch_page('views/user_login.py')

