import streamlit as st

#curr_path = os.getcwd()
#img_name = "eqtlogo_white.png"
#full_path = os.path.join(curr_path, img_name)
#print(full_path)
#st.logo("https://grupoequatorialenergia-my.sharepoint.com/:i:/r/personal/gabriel_cantanhede_equatorialenergia_com_br/Documents/logo_azul.png?csf=1&web=1&e=PBcUzk")
#st.logo("https://grupoequatorialenergia-my.sharepoint.com/:i:/r/personal/gabriel_cantanhede_equatorialenergia_com_br/Documents/logo_branco.png?csf=1&web=1&e=5NLcWc")

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

pages = {
    "Páginas":[
        st.Page("./views/single_selection.py", title="Visão Básica",),
        st.Page("./views/full_selection.py", title="Visão Completa", default=True),
        #st.Page("./views/stakeholder_selection.py", title="Visão Completa", default=True),
    ]}

pg = st.navigation(pages)

pg.run()