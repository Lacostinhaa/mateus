
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Painel Solana + Kamino", layout="wide")

st.title("📊 Painel DeFi - Solana com Kamino")
st.markdown("Este é o painel de análise de pools e empréstimos na rede Solana.")

wallet = st.text_input("Digite o endereço da sua carteira Solana")

# Simulação de valor atual (exemplo)
valor_total_atual = 430.00
data_hoje = date.today()
arquivo_csv = "historico.csv"

# Inicializa o DataFrame com segurança
try:
    if os.path.exists(arquivo_csv):
        historico_df = pd.read_csv(arquivo_csv)
        if historico_df.empty:
            historico_df = pd.DataFrame(columns=["Data", "Valor"])
    else:
        historico_df = pd.DataFrame(columns=["Data", "Valor"])
except Exception as e:
    historico_df = pd.DataFrame(columns=["Data", "Valor"])

# Garante que o dataframe tem as colunas certas
if "Data" not in historico_df.columns or "Valor" not in historico_df.columns:
    historico_df = pd.DataFrame(columns=["Data", "Valor"])

# Adiciona nova linha com concat
nova_linha = pd.DataFrame([{"Data": str(data_hoje), "Valor": valor_total_atual}])
historico_df = pd.concat([historico_df, nova_linha], ignore_index=True)

# Salva o CSV com segurança
try:
    historico_df.to_csv(arquivo_csv, index=False)
except Exception as e:
    st.warning("Erro ao salvar histórico. Verifique permissões de escrita.")

if wallet:
    st.success(f"Analisando carteira: {wallet}")
    st.subheader("🔍 Resultado da análise (simulado)")
    st.write("• Pool: SOL/USDC")
    st.write("• Valor investido: US$ 430.00")
    st.write("• Ganho estimado: US$ 9.85")
    st.write("• Comparação com HOLD: +US$ 4.70")
    st.write("• Impermanent Loss: -1.12%")

    st.markdown("---")
    st.subheader("💼 Kamino Health Zone")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🟢 Safe", "32% LTV", "Tudo certo por aqui")

    with col2:
        st.metric("🟡 Take Care", "55% LTV", "Fique de olho")

    with col3:
        st.metric("🟠 Warning", "71% LTV", "Atenção! Risco médio")

    with col4:
        st.metric("🔴 Run Out", "83% LTV", "Risco crítico!")
