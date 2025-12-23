
import streamlit as st

st.set_page_config(
    page_title="Bolões dos Campos",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 Bolões dos Campos")

# Entrada do resultado
resultado = st.multiselect(
    "Digite os 6 números do sorteio:",
    options=range(1, 61),
    max_selections=6
)

if len(resultado) == 6:
    resultado = set(resultado)

    boloes = {
        "Bolão da Mega Campos": [
            [3, 24, 26, 38, 39, 41, 46],
            [4, 6, 11, 19, 20, 31, 37],
            [16, 24, 33, 42, 46, 49, 59],
            [6, 8, 23, 25, 36, 52, 53],
            [8, 15, 25, 27, 30, 33, 59]
        ],

        "Bolão dos Campos": [
            [15, 22, 28, 30, 34, 37, 38, 40],
            [10, 32, 38, 41, 45, 47, 51, 53],
            [12, 15, 25, 30, 41, 53, 59, 60],
            [15, 22, 28, 30, 34, 37, 38, 40],
            [10, 13, 19, 23, 35, 37, 53, 55],
            [4, 9, 35, 42, 52, 55, 57],
            [6, 37, 38, 41, 43, 45, 54],
            [12, 15, 29, 41, 45, 51, 58],
            [8, 13, 18, 23, 27, 33, 59],
            [8, 26, 22, 30, 43, 50, 58],
            [10, 16, 29, 37, 38, 56, 60]
        ]
    }

    for nome_bolao, jogos in boloes.items():
        st.subheader(f"🧾 {nome_bolao}")

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
