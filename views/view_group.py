import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
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
try:
    # Querying the adequate view table
    view_choice = 'reputacao_estados_15dias'
    df_response = dbc.load_data(conn, view_choice)
    # df_response

    # Prepping tables and values to build visualizations
    min_date = df_response['dia'].min().date() # this is necessary to limit dataviz to the existing days in the data 
    current_day_in_data = df_response.iat[0,0].date() # Retrieving most recent day in the dataset
    # st.write(min_date.date())

    ### User input section
    with st.container(border=True):
        sel_date = st.date_input(
            label="Selecione o dia:",
            value=current_day_in_data,
            min_value=min_date,
            max_value=datetime.today().date(),
            )
    sel_date_dtime = pd.to_datetime(sel_date)


    try: # Necessary in case the user tries to select today's date, but no analyst has uploaded today's data
        ## Filtering data
        mask_selected_date = df_response['dia'] == sel_date_dtime
        mask_previous_date = df_response['dia'] == (sel_date_dtime - timedelta(days=1))

        df_response_today = df_response[mask_selected_date].copy()
        df_response_yesterday = df_response[mask_previous_date].copy()
        # df_response_today
        # df_response_yesterday

        ## Reputation
        today_rep = df_response_today['reputacao'].mean()
        yesterday_rep = df_response_yesterday['reputacao'].mean()
        color_today_rep = misc.pick_color(today_rep/100)

        ## Favorability
        today_fav = df_response_today[mask_selected_date]['favorabilidade'].mean()
        yesterday_fav = df_response_yesterday[mask_previous_date]['favorabilidade'].mean()
        color_today_fav = misc.pick_color(today_fav/100)

        ## Saudability
        today_saud = df_response_today[mask_selected_date]['saudabilidade'].mean()
        yesterday_saud = df_response_yesterday[mask_previous_date]['saudabilidade'].mean()
        color_today_saud = misc.pick_color(today_saud/100)

        df_textual_today = df_response_today[['estado', 'pontos_positivos', 'pontos_atencao']].copy()

    except Exception as e:
        # TODO do proper exeption handling for the cases where the date selected has no data
        st.write(e)

    # How to do a metric card with formatted outputs
    # st.metric(label='SAUD', value="{:.2f} %".format(today_saud), delta="{:.2f}".format(today_saud-yesterday_saud), label_visibility='collapsed')

    ### First part of the core dashboard visuals
    with st.container(border=True):
        col1, col2, col3 = st.columns([0.3,0.3,0.5], gap='small',)
        with col1:
            st.subheader(":newspaper: :blue[Imprensa]")
            f_string_press = """**{:.1f}% Favorabilidade** <br>:gray-background[{} Notícias] <br>:green-background[{} Positivas] <br>:red-background[{} Negativas]"""
            st.markdown(f_string_press.format(
                df_response_today['favorabilidade'].mean(),
                df_response_today['total_noticias'].sum(),
                df_response_today['imprensa_positivas'].sum(),
                df_response_today['imprensa_negativas'].sum(),
                ), unsafe_allow_html=True)
        with col2:
            st.subheader(":iphone: :blue[Digital]")
            f_string_press = """**{:.1f}% Saudabilidade** <br>:gray-background[{} Menções] <br>:green-background[{} Positivas] <br>:orange-background[{} Neutras] <br>:red-background[{} Negativas]"""
            st.markdown(f_string_press.format(
                df_response_today['saudabilidade'].mean(), 
                df_response_today['total_mencoes'].sum(), 
                df_response_today['digital_positivas'].sum(), 
                df_response_today['digital_neutras'].sum(), 
                df_response_today['digital_negativas'].sum(),
                ), unsafe_allow_html=True)

        with col3:
            # st.markdown("### Reputação <br>(hoje vs. ontem)",unsafe_allow_html=True)
            fig_today_rep = go.Figure(go.Indicator(
                mode = "number+gauge+delta", value = today_rep,
                domain = {'x': [0.1, 1], 'y': [0, 1]},
                # title = {'text' :"<b>Reputação<br> (hoje <br>vs. <br>ontem)</b> ", 'font':{'size':20}},
                delta = {'reference': yesterday_rep, "valueformat":'+.2'},
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
            fig_today_rep.update_layout(
                height = 250,
                width=1000,
                title=dict(
                    text='Reputação <br>(hoje vs. ontem)',
                    automargin=False,
                    font=dict(color='darkblue', size=25),
                    x=0.45,
                    y=0.9,
                    xanchor='center',
                    yanchor='top',
                    ))
            st.plotly_chart(fig_today_rep)


    styles_positive = """{
        border: 1px solid #6b6b6bb3;
        border-radius: 8px;
        display: flex;
        box-sizing: border-box;
        padding-right: calc(-1px + 5rem);
        
        
        background-color: #0901fa3b;
    }
    ul {
        margin: 0px 0px 1rem;
        padding: 0px 0px 1rem;
        text-wrap: inherit;
        word-wrap: break-word;
    }
    """

    col_pos, col_neg = st.columns([0.5, 0.5])
    with col_pos:
        # with stylable_container(key='positive_block', css_styles=styles_positive):
        with st.container(border=True):
            st.markdown("### :thumbsup: **:blue[Pontos Positivos]**:")
            for index, row in df_textual_today.iterrows():
                dict_ppos = eval(row['pontos_positivos'].replace('\\n', ' '))
                f_string = f"- :blue-background[**{row['estado']} -** **_Imprensa_**: {dict_ppos['press']} | **_Digital_**: {dict_ppos['dig']}]"
                st.write(f_string)
    with col_neg:
        with st.container(border=True):
            st.markdown("### :warning: **:orange[Pontos de Atenção]**: ")
            for index, row in df_textual_today.iterrows():
                dict_ppos = eval(row['pontos_atencao'].replace('\\n', ' '))
                f_string = f"- :orange-background[**{row['estado']} -** **_Imprensa_**: {dict_ppos['press']} | **_Digital_**: {dict_ppos['dig']}]"
                st.write(f_string)

    ### Navigation Buttons
    with st.container():
        nav_prev, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
        with nav_prev:
            st.page_link("views/dash.py", label=":arrow_left: Voltar",)
        with nav_next:
            st.page_link("views/view_states.py", label="Avançar :arrow_right:",)
    
    # Hacky way of including a custom footer in each page
    misc.write_footer()

except Exception as e:
    st.error("Falha ao recuperar dados do termômetro, tente logar novamente.")
    time.sleep(5)
    st.switch_page('views/user_login.py')

### Leftover Visualizations
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