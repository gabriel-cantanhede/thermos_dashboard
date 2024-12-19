import streamlit as st

st.logo("https://www.equatorialenergia.com.br/wp-content/themes/equatorial-energia-child/img/logo-blue.png")

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

pages = {
    "Entrada":[
        st.Page("./views/landing_page.py", title="Página Inicial", default=True),
        st.Page("./views/user_login.py", title="Login de Usuário"),
        ],
    "Dashboard":[
        st.Page("./views/dash.py", title="Indicadores"),
        ],
    "Informe Reputacional":[
        st.Page("./views/view_group.py", title="Visão Grupo"),
        st.Page("./views/view_states.py", title="Visão Estados"),
        ]}

pg = st.navigation(pages)

pg.run()