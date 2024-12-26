import streamlit as st
from datetime import datetime, timezone
import control.misc_funcs as misc

# # My custom funcs and py files
# import control.misc_funcs as misc
# import control.db_connection as dbc

# # Sanity check on the db connection object
# if "__conn" not in st.session_state:
#     conn = dbc.init_connection()
#     st.session_state['__conn'] = conn
# else:
#     conn = st.session_state['__conn']
    

st.markdown("# :thermometer: :blue[Bem-vindo ao Termômetro Reputacional Automático do Grupo Equatorial]")

with st.container(border=True):
    st.markdown(
        """Para monitorar e aprimorar continuamente a nossa reputação, apresentamos o Termômetro Reputacional automatizado! <br>
        Esta ferramenta foi desenvolvida para proporcionar uma solução prática e eficiente no acompanhamento e avaliação da reputação,
        com base em indicadores coletados da imprensa e das plataformas digitais.<br> Clique no botão abaixo para acessar o app!
        """, unsafe_allow_html=True)

#### Navigation buttons ###
# st.markdown("-----")
# nav_next = st.columns(1, vertical_alignment='bottom')

with st.container():
    _, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
    with nav_next:
        st.page_link("views/dash.py", label="Avançar 	:arrow_right:",)

# Hacky way of including a custom footer in each page
misc.write_footer()