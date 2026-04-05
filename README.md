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

src/
├── etl.py                      # Pipeline de transformação
└── app.py                      # Aplicação Streamlit
```

### 🔹 Camadas de Dados

* **Bronze** → Dados brutos (Excel)
* **Silver** → Dados tratados e limpos
* **Gold** → Dataset final para análise

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

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o ETL

```bash
python src/etl.py
```

### 5. Execute o app

```bash
streamlit run src/app.py
```

---

## 📌 Possíveis Melhorias

* 🔄 Orquestração com Airflow
* ☁️ Integração com Data Lake
* ⚡ Migração para PySpark
* 📊 Dashboard em Power BI / Fabric

---

## 👨‍💻 Autor

**Fredson Cabral**

* Engenheiro de Dados / Analista de Dados
* Foco em ETL, automação e analytics

---
