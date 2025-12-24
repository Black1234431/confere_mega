import streamlit as st
import json

# ==============================
# Configuração da página
# ==============================
st.set_page_config(
    page_title="Confere Bolão",
    page_icon="🎲",
    layout="centered"
)

st.title("🎰 Conferência de Bolões – Mega-Sena")

st.markdown("""
### 📌 Como usar o conferidor

1️⃣ **Insira manualmente seus bolões** ou carregue um arquivo JSON já salvo  
2️⃣ **Salve o arquivo** para conferir esses bolões novamente no futuro  
3️⃣ Com os bolões carregados, **digite os 6 números do sorteio da Mega-Sena**  
4️⃣ O sistema irá conferir automaticamente todos os jogos e indicar:
- Quantos acertos cada jogo teve  
- Quais apostas foram **premiadas (4 ou mais acertos)**  

💡 Você pode reutilizar o mesmo arquivo de bolões sempre que quiser.  
Boa sorte! 🍀
""")

# ==============================
# Estado da aplicação
# ==============================
if "boloes" not in st.session_state:
    st.session_state.boloes = {}

if "modo_edicao" not in st.session_state:
    st.session_state.modo_edicao = False

# ==============================
# Funções
# ==============================


def conferir_boloes(boloes, resultado):
    st.subheader("📊 Resultado da Conferência")

    for nome_bolao, jogos in boloes.items():
        st.markdown(f"### 🧾 {nome_bolao}")

        premiadas = 0

        for idx, jogo in enumerate(jogos, start=1):
            acertos = len(set(jogo) & set(resultado))
            linha = f"Jogo {idx}: {jogo} → **{acertos} acertos**"

            if acertos >= 4:
                st.success("🎉 " + linha)
                premiadas += 1
            else:
                st.write(linha)

        st.write(f"✅ Total de apostas premiadas: **{premiadas}**")
        st.divider()


# ==============================
# Upload de arquivo JSON
# ==============================
st.subheader("📂 Carregar bolões de arquivo")

arquivo = st.file_uploader("Envie um arquivo JSON", type="json")

if arquivo:
    dados = json.load(arquivo)
    st.session_state.boloes.update(dados)
    st.success("Bolões carregados com sucesso!")

# ==============================
# Botão de edição (toggle)
# ==============================
if st.button("✏️ Editar bolões"):
    st.session_state.modo_edicao = not st.session_state.modo_edicao

# ==============================
# Área de edição (condicional)
# ==============================
if st.session_state.modo_edicao:
    st.subheader("➕ Adicionar / Editar bolões")

    nome_bolao = st.text_input("Nome do bolão")

    jogos_texto = st.text_area(
        "Jogos (um por linha, números separados por vírgula)",
        placeholder="Ex:\n3,24,26,38,39,41\n4,6,11,19,20,31"
    )

    if st.button("Adicionar / Atualizar bolão"):
        if not nome_bolao.strip():
            st.error("Informe o nome do bolão.")
        elif not jogos_texto.strip():
            st.error("Informe pelo menos um jogo.")
        else:
            jogos = []
            for linha in jogos_texto.splitlines():
                nums = [
                    int(n.strip())
                    for n in linha.split(",")
                    if n.strip().isdigit()
                ]
                if nums:
                    jogos.append(nums)

            if jogos:
                st.session_state.boloes[nome_bolao] = jogos
                st.success(
                    f"Bolão '{nome_bolao}' salvo com {len(jogos)} jogos!"
                )
            else:
                st.error("Nenhum jogo válido encontrado.")

# ==============================
# Visualização dos bolões
# ==============================
if st.session_state.boloes:
    st.subheader("📋 Bolões carregados")

    for nome, jogos in st.session_state.boloes.items():
        st.write(f"• **{nome}** – {len(jogos)} jogos")

# ==============================
# Download do JSON
# ==============================
if st.session_state.boloes:
    json_str = json.dumps(
        st.session_state.boloes,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        "💾 Baixar arquivo de bolões (JSON)",
        data=json_str,
        file_name="boloes.json",
        mime="application/json"
    )

# ==============================
# Resultado do sorteio
# ==============================
if st.session_state.boloes:
    st.subheader("🎯 Resultado do sorteio")

    resultado = st.multiselect(
        "Escolha os 6 números sorteados",
        options=range(1, 61),
        max_selections=6
    )

    if len(resultado) == 6:
        conferir_boloes(st.session_state.boloes, resultado)
