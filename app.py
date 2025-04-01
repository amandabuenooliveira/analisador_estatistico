import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações iniciais da página
st.set_page_config(page_title="Analisador de CSV", layout="wide")
st.title("Analisador de Dados Educacionais (CSV)")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Carregue um arquivo CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"Arquivo carregado com sucesso! Formato: {df.shape[0]} linhas x {df.shape[1]} colunas")

        # Exibição de dados básicos
        with st.expander("👁️ Visualizar Dados"):
            st.dataframe(df.head())

        with st.expander("📊 Estatísticas Básicas"):
            st.write("Tipos de dados:")
            st.write(df.dtypes)
            st.write("Resumo estatístico:")
            st.write(df.describe())
            st.write("Valores ausentes:")
            st.write(df.isnull().sum())

        # Correlação
        with st.expander("📈 Matriz de Correlação"):
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                st.write(corr)
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Não há colunas numéricas para gerar correlação.")

        # Análises por coluna
        colunas = df.columns.tolist()
        st.subheader("🔍 Análises por Coluna")
        coluna_selecionada = st.selectbox("Selecione uma coluna para análise:", colunas)

        if coluna_selecionada:
            st.write(f"Contagem de valores únicos em `{coluna_selecionada}`:")
            st.write(df[coluna_selecionada].value_counts())

            st.write(f"Valores únicos em `{coluna_selecionada}`:")
            st.write(df[coluna_selecionada].unique())

            if df[coluna_selecionada].dtype in [np.int64, np.float64]:
                st.write("Histograma:")
                fig, ax = plt.subplots()
                sns.histplot(df[coluna_selecionada].dropna(), kde=True, ax=ax)
                st.pyplot(fig)

                st.write("Boxplot:")
                fig, ax = plt.subplots()
                sns.boxplot(y=df[coluna_selecionada].dropna(), ax=ax)
                st.pyplot(fig)
            else:
                st.info("Coluna selecionada não é numérica para gerar histograma ou boxplot.")

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.info("Aguardando o upload de um arquivo CSV.")
