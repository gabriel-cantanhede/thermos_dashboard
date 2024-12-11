import streamlit as st
from datetime import datetime, timezone


# if "ts_landing" not in st.session_state.keys():
#     st.session_state["ts_landing"] = str(datetime.now(tz=timezone.utc))
    

st.markdown("# :thermometer: :blue[Bem vindo ao Informe Reputacional Automático do Grupo Equatorial]")

with st.container(border=True):
    st.markdown("""Para acessar os dados do Informe Reputacional, é necessário ter credenciais de acesso ao app. Caso ainda não as tenha, entre em contato com o time de <a href=mailto:gabriel.cantanhede@equatorialenergia.com.br>Inteligência de Dados</a> para obtê-las.""", unsafe_allow_html=True)

#### Navigation buttons ###
# st.markdown("-----")
nav_prev, nav_next = st.columns(2, vertical_alignment='bottom')

with nav_next:
    st.page_link("views/user_login.py", label="Avançar",)