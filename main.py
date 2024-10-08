import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# criar funçções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes)

#preparar vizualiações = filtros ações
lista_acoes = st.sidebar.multiselect("Ações", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

print(lista_acoes)

# filtros gerais
st.sidebar.header("Filtros")

data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o Período", 
                                   min_value= data_inicial, 
                                   max_value= data_final, 
                                   value=(data_inicial, data_final),
                                   step=timedelta(days=1))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

#criar interface streamlit
st.write("""
# App Preço de Ações
O gráfica abaixo representa a evolução do preço das ações selecionadas ao longo dos anos
         """)

# criar grafico
st.line_chart(dados)