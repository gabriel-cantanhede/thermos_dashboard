import streamlit as st
from datetime import datetime, timezone
import control.db_connection as dbc
import control.misc_funcs as misc
    

st.markdown("# :thermometer: :blue[Bem-vindo ao Termômetro Reputacional Automático do Grupo Equatorial]")

with st.container(border=True):
    st.markdown(
        """Para monitorar e aprimorar continuamente a reputação do :blue[**Grupo Equatorial**], apresentamos o **Termômetro Reputacional, _versão automatizada_**! <br>
        Esta ferramenta foi desenvolvida para proporcionar uma solução prática e eficiente no acompanhamento e avaliação da reputação do :blue[**Grupo**],
        com base em dados coletados das mídias tradicionais e digitais. <br><br>**Clique no botão :blue-background[_Avançar_] para acessar o app**!
        <br><br> *Obs.: Para solicitar acesso ao app, entre em contato com a administração do app [Time de Inteligência de Dados](mailto:valquiria.silva@equatorialenergia.com.br)*.
        """, unsafe_allow_html=True)

#### Navigation buttons ###
# st.markdown("-----")
# nav_next = st.columns(1, vertical_alignment='bottom')

with st.container():
    _, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
    with nav_next:
        st.page_link("views/user_login.py", label="Avançar 	:arrow_right:",)

# Hacky way of including a custom footer in each page
misc.write_footer()