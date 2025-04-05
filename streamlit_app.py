
import streamlit as st
import datetime
import requests
import pandas as pd
import os

def get_sol_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        return data['solana']['usd']
    except:
        return 140.50  # fallback

preco_sol_hoje = get_sol_price()

valor_investido_total = 430.00
sol_investido = 0.807689
usdc_investido = 327.92

apr_5m = 268.49
apr_1h = 173.45
apr_6h = 308.21
apr_24h = 182.94

apr_ponderado = (apr_5m * 0.1 + apr_1h * 0.2 + apr_6h * 0.3 + apr_24h * 0.4)
rendimento_diario_real = apr_ponderado / 365
rendimento_conservador = rendimento_diario_real * 0.70
rendimento_otimista = rendimento_diario_real * 1.30

data_hoje = datetime.date.today()
arquivo_csv = "historico_pool.csv"

dias_na_pool = 0
valor_total_atual = valor_investido_total

if os.path.exists(arquivo_csv):
    historico_df = pd.read_csv(arquivo_csv)
    dias_na_pool = len(historico_df)
else:
    historico_df = pd.DataFrame(columns=["Data", "Valor"])

valor_total_atual *= (1 + rendimento_diario_real / 100) ** dias_na_pool
valor_hold = (sol_investido * preco_sol_hoje) + usdc_investido
rendimento_total_percentual = ((valor_total_atual / valor_investido_total) - 1) * 100

if not historico_df.empty and historico_df["Data"].iloc[-1] == str(data_hoje):
    pass
else:
    historico_df = historico_df.append({"Data": str(data_hoje), "Valor": valor_total_atual}, ignore_index=True)
    historico_df.to_csv(arquivo_csv, index=False)

st.set_page_config(page_title="Painel de Pool - Meteora SOL/USDC", layout="wide")
st.title("📊 Painel de Pool de Liquidez - Meteora SOL/USDC")
st.markdown(f"💱 **Preço atual do SOL:** US$ {preco_sol_hoje:.2f}")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Valor Investido (Inicial)", f"US$ {valor_investido_total:.2f}")
    st.metric("📈 Rendimento Estimado Diário", f"{rendimento_diario_real:.2f}%")

with col2:
    st.metric("📊 Valor Atual na Pool", f"US$ {valor_total_atual:.2f}", delta=f"{rendimento_total_percentual:.2f}%")
    st.metric("🗓️ Dias na Pool", f"{dias_na_pool} dias")

with col3:
    comparacao_hold = valor_total_atual - valor_hold
    delta_text = f"+US$ {comparacao_hold:.2f}" if comparacao_hold > 0 else f"-US$ {abs(comparacao_hold):.2f}"
    st.metric("💎 Se tivesse feito HOLD", f"US$ {valor_hold:.2f}", delta=delta_text)

st.markdown("---")
st.subheader("📌 Detalhes da Pool")
st.markdown("- **Par de Tokens:** SOL / USDC")
st.markdown(f"- **Quantidade de SOL investida:** {sol_investido}")
st.markdown(f"- **Quantidade de USDC investida:** {usdc_investido}")
st.markdown(f"- **APR ponderado atual:** {apr_ponderado:.2f}%")
st.markdown("---")

st.subheader("📊 Cenários de Rendimento Diário")
col4, col5, col6 = st.columns(3)
with col4:
    st.metric("📉 Conservador (-30%)", f"{rendimento_conservador:.2f}%")
with col5:
    st.metric("📌 Estimado Atual", f"{rendimento_diario_real:.2f}%")
with col6:
    st.metric("📈 Otimista (+30%)", f"{rendimento_otimista:.2f}%")

st.markdown("---")
st.subheader("📈 Evolução do Valor da Pool")
st.line_chart(historico_df.set_index("Data"))
st.info("📌 Dados atualizados com base no APR e preço do SOL via CoinGecko.")
