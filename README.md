# 📦 Projeto de Análise de Estoque (ETL + Data App)

## 🚀 Visão Geral

Este projeto implementa um pipeline completo de dados para análise de estoque, seguindo boas práticas de engenharia de dados:

* 🔄 ETL com tratamento e padronização de dados
* 📊 Aplicação interativa com Streamlit
* 📁 Exportação de dados tratados
* 📈 Análise dinâmica por filtros

---

## 🏗️ Arquitetura do Projeto

```
data/
│
├── estoque.xlsx                # Fonte (raw data)
├── planilha_final_atualizada.xlsx  # Camada Silver
└── estoque_mg.xlsx             # Camada Gold
├── etl.py                      # Pipeline de transformação
└── main.py                      # Aplicação Streamlit
```
---

## ⚙️ Tecnologias Utilizadas

* 🐍 Python
* 🐼 Pandas
* ⚡ Streamlit
* 📊 Plotly
* 📁 OpenPyXL

---

## 🔄 Pipeline ETL

Principais etapas:

* Leitura de dados Excel
* Tratamento de datas
* Preenchimento de valores (forward fill)
* Mapeamento de tipo de movimentação
* Tratamento de saldo inicial
* Criação de colunas derivadas (Mês)
* Filtros de negócio (depósitos)
* Merge com dados complementares

---

## 📊 Aplicação (Streamlit)

A aplicação permite:

* 🔎 Filtrar por:

  * Segmento
  * Depósito
  * Mês

* 📈 Visualizar:

  * Quantidade total
  * Valor total em estoque

* 📋 Explorar dados:

  * Busca por item
  * Tabela interativa

* 📥 Exportar:

  * Download em Excel formatado

---

## 👨‍💻 Autor

**Fredson Cabral**

* Engenheiro de Dados / Analista de Dados
* Foco em ETL, automação e analytics

---
