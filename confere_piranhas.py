import streamlit as st

st.set_page_config(
    page_title="Bolão das piranhas",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 Bolão Piranhas Rycassss")

# Entrada do resultado
resultado = st.multiselect(
    "Digite os 6 números do sorteio:",
    options=range(1, 61),
    max_selections=6
)

if len(resultado) == 6:
    resultado = set(resultado)

    boloes = {
        "Piranhas Rycassss": [

            [3, 5, 10, 12, 21, 27, 38, 52, 59],
            [3, 4, 6, 8, 10, 37, 55],
            [7, 12, 27, 32, 39, 40, 58],
            [4, 22, 24, 43, 51, 60],
            [6, 11, 30, 38, 39, 51],
            [5, 17, 21, 27, 31, 44],
            [6, 21, 29, 34, 35, 48],
            [5, 13, 20, 26, 31, 42],
            [1, 4, 23, 28, 34, 37]
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
