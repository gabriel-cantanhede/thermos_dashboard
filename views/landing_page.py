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
    st.markdown("""Para acessar os dados do Informe Reputacional, é necessário ter credenciais de acesso ao app. Caso ainda não as tenha, entre em contato com o time de <a href=mailto:gabriel.cantanhede@equatorialenergia.com.br>Inteligência de Dados</a> para obtê-las.""", unsafe_allow_html=True)

#### Navigation buttons ###
# st.markdown("-----")
# nav_next = st.columns(1, vertical_alignment='bottom')

with st.container():
    _, _, nav_next = st.columns([0.4,0.2,0.4], vertical_alignment='bottom')
    with nav_next:
        st.page_link("views/dash.py", label="Avançar 	:arrow_right:",)

# Hacky way of including a custom footer in each page
misc.write_footer()