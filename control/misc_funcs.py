import streamlit as st
from time import sleep

# def showProgressBar():
#     progress_text = "Operação em progresso. Aguarde..."
#     my_bar = progress(0, text=progress_text)
#     #time.sleep()
#     for percent_complete in range(100):
#         sleep(0.0001)
#         my_bar.progress(percent_complete + 1, text=progress_text)
#     sleep(1)
#     my_bar.progress(100, text="Operação concluída com sucesso!")
#     sleep(0.1)

def pick_color(value):
    if value < 0.36:
        return "#DA1E00"
    elif value < 0.71:
        return "#FFCC05"
    else:
        return "#00AB03"

def write_footer(logo_style='blue'):
    img_link = f"https://www.equatorialenergia.com.br/wp-content/themes/equatorial-energia-child/img/logo-{logo_style}.png"
    st.divider()
    st.markdown(
        f""":copyright: _Copyright 2024 - Time Inteligência de Dados_ <br>
        Gerência de Comunicação Externa, Marketing e Sustentabilidade <br>
        Diretoria de Clientes, Serviços e Inovação <br> <br>
        <img src={img_link} alt='logo_eqtl' width=150px>""",
        unsafe_allow_html=True)