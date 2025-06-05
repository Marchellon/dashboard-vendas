import streamlit as st
import pandas as pd
import plotly.express as px

# carregar os dados

dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# calcular o faturamento por linha

dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# titulo

st.title('Dashboard de Vendas')
st.divider()

# sidebar

st.sidebar.header("Filtros")

lojas = sorted(dados['Loja'].unique())
produtos_unicos = sorted(dados['Produto'].unique())
produtos_opcoes = ['Todos'] + produtos_unicos

loja_escolhida = st.sidebar.selectbox('Selecione uma loja:', ['Todas'] + lojas)
produtos_selecionados = st.sidebar.multiselect(
    'Selecione um ou mais produtos:',
    options=produtos_opcoes,
    default=['Todos']
)

# logica de filtro

dados_filtrados = dados.copy()

if loja_escolhida != 'Todas':
    dados_filtrados = dados_filtrados[dados_filtrados['Loja'] == loja_escolhida]

if 'Todos' not in produtos_selecionados and produtos_selecionados:
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'].isin(produtos_selecionados)]
    produtos_ativos = produtos_selecionados
else:
    produtos_ativos = produtos_unicos

# faturamento total

faturamento_total = dados_filtrados['Faturamento'].sum()

# resumo

if loja_escolhida != 'Todas' and len(produtos_ativos) == 1:
    st.subheader(f"Na loja **{loja_escolhida}**, o produto **{produtos_ativos[0]}** teve um faturamento total de **R$ {faturamento_total:,.2f}**.")
elif loja_escolhida != 'Todas':
    st.subheader(f"Na loja **{loja_escolhida}**, os produtos selecionados somaram um faturamento de **R$ {faturamento_total:,.2f}**.")
elif len(produtos_ativos) == 1:
    st.subheader(f"O produto **{produtos_ativos[0]}** teve um faturamento total de **R$ {faturamento_total:,.2f}** em todas as lojas.")
else:
    st.subheader(f"O faturamento total considerando todos os filtros aplicados foi de **R$ {faturamento_total:,.2f}**.")

# grafico de pizza

st.sidebar.subheader("Participação dos Produtos")
dados_pizza = (
    dados_filtrados
    .groupby('Produto')['Faturamento']
    .sum()
    .reset_index()
)

if not dados_pizza.empty:
    grafico_pizza = px.pie(
        dados_pizza,
        names='Produto',
        values='Faturamento',
        title='Faturamento por Produto'
    )
    st.sidebar.plotly_chart(grafico_pizza, use_container_width=True)

st.divider()

# tabela

st.subheader("Tabela de Vendas Filtrada")
st.dataframe(dados_filtrados, use_container_width=True)

st.divider()

st.subheader("Faturamento por Loja")
faturamento_por_loja = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Faturamento', ascending=False)
)
grafico_barras = px.bar(
    faturamento_por_loja,
    x='Loja',
    y='Faturamento'
)
st.plotly_chart(grafico_barras, use_container_width=True)