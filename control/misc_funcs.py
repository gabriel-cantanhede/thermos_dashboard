import streamlit as st
import time

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
        Gerência Corporativa de Comunicação Externa e Marketing <br>
        Diretoria Corporativa de Clientes, Inovação e Serviços <br> <br>
        <img src={img_link} alt='Logomarca do Grupo Equatorial' width=200px>""",
        unsafe_allow_html=True)

@st.dialog("Ops... Ocorreu um erro.")
def redirect_to_login(error:Exception, timer:int = 10):
    st.error(f"Erro ao recuperar os dados do Termômetro. Mensagem de erro: {error}")
    counter_box = st.empty()
    for secs in range(timer,0,-1):
        # mm, ss = secs//60, secs%60
        counter_box.info(f"# Redirecionando para a página de login em {secs:02d}")
        time.sleep(1)
    st.switch_page('views/user_login.py')
