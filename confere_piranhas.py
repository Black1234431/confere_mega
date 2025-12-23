import streamlit as st

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

            # Jogos múltiplos (8 números)
            [3, 10, 12, 21, 27, 38, 52, 59],
            [5, 15, 24, 32, 35, 44, 47, 60],
            [7, 14, 18, 23, 31, 41, 48, 56],

            # 🟩 Jogos de 7 dezenas (complemento)
            [3, 12, 21, 34, 41, 52, 59],
            [5, 15, 27, 36, 44, 48, 60],
            [10, 18, 25, 35, 38, 47, 56],
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
