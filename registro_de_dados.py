import streamlit as st

st.set_page_config(page_title="Registrar Dados", layout="centered")

st.title("📝 Registrar Dados da Pool")

with st.form("dados_form"):
    plataforma = st.selectbox("Plataforma", ["Meteora", "Orca", "Raydium", "Kamino"])
    montante = st.text_input("Montante investido (US$)")
    pool = st.text_input("Par da Pool (ex: SOL/USDC)")
    quantidade = st.text_input("Quantidade de tokens (ex: 0.8 SOL + 327 USDC)")
    data = st.date_input("Data de entrada")
    observacao = st.text_area("Observações adicionais")

    submitted = st.form_submit_button("Salvar Dados")

if submitted:
    st.success("✅ Dados registrados com sucesso!")
    st.balloons()
