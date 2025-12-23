import streamlit as st
import json

st.set_page_config(
    page_title="Confere Bolão",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 Conferidor de Bolões da Mega-Sena")

# Entrada do resultado
resultado = st.multiselect(
    "Digite os 6 números do sorteio:",
    options=range(1, 61),
    max_selections=6
)

if len(resultado) == 6:
    resultado = set(resultado)

    boloes = json.loads(st.secrets["boloes"]["dados"])

    for nome_bolao, jogos in boloes.items():
        st.subheader(nome_bolao)

        premiadas = 0
        for idx, jogo in enumerate(jogos, start=1):
            acertos = len(resultado.intersection(jogo))
            linha = f"Jogo {idx}: {jogo} → {acertos} acertos"

            if acertos >= 4:
                st.success(linha + " 🎉")
                premiadas += 1
            else:
                st.write(linha)

        st.write(f"**Total de premiadas:** {premiadas}")
else:
    st.info("Selecione exatamente 6 números.")
