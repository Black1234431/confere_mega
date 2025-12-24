import streamlit as st
import json

st.set_page_config(
    page_title="Confere Bolão",
    page_icon="🎲",
    layout="centered"
)


st.set_page_config(
    page_title="Conferência de Bolões - Mega-Sena",
    layout="centered"
)

st.title("🎰 Conferência de Bolões – Mega-Sena")

st.markdown("""
### 📌 Como usar o conferidor

1️⃣ **Insira manualmente seus bolões**, criando um ou mais bolões com seus respectivos jogos.  
2️⃣ **Salve o arquivo** para poder conferir esses bolões novamente no futuro.  
3️⃣ Com os bolões carregados, **digite os 6 números do sorteio da Mega-Sena**.  
4️⃣ O sistema irá conferir automaticamente todos os jogos e indicar:
- Quantos acertos cada jogo teve  
- Quais apostas foram **premiadas (4 ou mais acertos)**  

💡 Você pode reutilizar o mesmo arquivo de bolões sempre que quiser.
            
Boa sorte! 🍀
""")

# =================================
# Inicializa estado
# =================================
if "boloes" not in st.session_state:
    st.session_state.boloes = {}

# =================================
# Funções
# =================================


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


# =================================
# Upload de JSON
# =================================
st.subheader("📂 Carregar bolões de arquivo")

arquivo = st.file_uploader("Envie um arquivo JSON", type="json")

if arquivo:
    dados = json.load(arquivo)
    st.session_state.boloes.update(dados)
    st.success("Bolões carregados com sucesso!")

# =================================
# Inserção manual (SEM sobrescrever)
# =================================
st.subheader("➕ Adicionar novo bolão manualmente")

nome_bolao = st.text_input("Nome do bolão")

jogos_texto = st.text_area(
    "Jogos (um por linha, números separados por vírgula)",
    placeholder="Ex:\n3,24,26,38,39,41\n4,6,11,19,20,31"
)

if st.button("Adicionar bolão"):
    if not nome_bolao.strip():
        st.error("Informe o nome do bolão.")
    elif not jogos_texto.strip():
        st.error("Informe pelo menos um jogo.")
    else:
        jogos = []
        for linha in jogos_texto.splitlines():
            nums = [int(n.strip())
                    for n in linha.split(",") if n.strip().isdigit()]
            if nums:
                jogos.append(nums)

        if jogos:
            st.session_state.boloes[nome_bolao] = jogos
            st.success(
                f"Bolão '{nome_bolao}' adicionado com {len(jogos)} jogos!")
        else:
            st.error("Nenhum jogo válido encontrado.")

# =================================
# Visualização dos bolões
# =================================
if st.session_state.boloes:
    st.subheader("📋 Bolões carregados")

    for nome, jogos in st.session_state.boloes.items():
        st.write(f"• **{nome}** – {len(jogos)} jogos")

# =================================
# Download do JSON unificado
# =================================
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

# =================================
# Edição de bolões existentes
# =================================
if st.session_state.boloes:
    st.subheader("✏️ Editar bolões existentes")

    bolao_selecionado = st.selectbox(
        "Selecione um bolão para editar",
        options=list(st.session_state.boloes.keys())
    )

    jogos_atual = st.session_state.boloes[bolao_selecionado]

    # Converte jogos para texto
    jogos_texto_edit = "\n".join(
        ", ".join(str(n) for n in jogo) for jogo in jogos_atual
    )

    novo_texto = st.text_area(
        "Edite os jogos (um por linha, números separados por vírgula)",
        value=jogos_texto_edit,
        height=200
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Salvar alterações"):
            novos_jogos = []
            for linha in novo_texto.splitlines():
                nums = [int(n.strip())
                        for n in linha.split(",") if n.strip().isdigit()]
                if nums:
                    novos_jogos.append(nums)

            if novos_jogos:
                st.session_state.boloes[bolao_selecionado] = novos_jogos
                st.success(
                    f"Bolão '{bolao_selecionado}' atualizado com sucesso!")
            else:
                st.error("Nenhum jogo válido encontrado.")

    with col2:
        if st.button("🗑️ Excluir bolão"):
            del st.session_state.boloes[bolao_selecionado]
            st.warning(f"Bolão '{bolao_selecionado}' removido.")
            st.experimental_rerun()

# =================================
# Resultado e conferência
# =================================
if st.session_state.boloes:
    st.subheader("🎯 Resultado do sorteio")

    resultado = st.multiselect(
        "Escolha os 6 números sorteados",
        options=range(1, 61),
        max_selections=6
    )

    if len(resultado) == 6:
        conferir_boloes(st.session_state.boloes, resultado)
