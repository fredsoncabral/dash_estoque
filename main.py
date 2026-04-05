"""
Streamlit App - Posição de Estoque

Autor: Fredson Cabral
Descrição:
Aplicação interativa para análise de posição de estoque com filtros dinâmicos,
métricas agregadas e exportação para Excel.
"""

from pathlib import Path
import datetime
import logging
from io import BytesIO

import pandas as pd
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency, format_decimal


# ------------------------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------------------------

DATA_FILE = Path("data/estoque_mg.xlsx")
LOGO_PATH = Path("tectoy.png")

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)


# ------------------------------------------------------------------------------
# FUNÇÕES UTILITÁRIAS
# ------------------------------------------------------------------------------

def get_last_update(file_path: Path) -> str:
    try:
        timestamp = file_path.stat().st_mtime
        date = datetime.datetime.fromtimestamp(timestamp)
        return date.strftime('%d-%m-%Y')
    except Exception:
        return "N/A"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_FILE)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Ano_Mês"] = df["Data"].dt.to_period("M").astype(str)
    return df


def apply_filters(df: pd.DataFrame, segmentos, depositos, meses) -> pd.DataFrame:
    if segmentos:
        df = df[df["Segmento"].isin(segmentos)]
    if depositos:
        df = df[df["Depósito"].isin(depositos)]
    if meses:
        df = df[df["Mês"].isin(meses)]
    return df


def calculate_stock(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    df = df.sort_values("Data")

    saldo = (
        df.groupby(["Item", "Depósito"])["Quantidade"]
        .sum()
        .reset_index(name="Saldo")
    )

    ultimos = (
        df.groupby(["Item", "Depósito"])
        .last()
        .reset_index()
    )

    df_final = saldo.merge(
        ultimos[["Segmento", "Item", "Depósito", "Descrição", "Custos"]],
        on=["Item", "Depósito"]
    )

    return df_final[df_final["Saldo"] > 0]


def format_brl(x):
    try:
        return f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return "-"


def format_qtd(x):
    try:
        return f"{x:,.0f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return "-"


@st.cache_data
def export_to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Estoque")

        ws = writer.sheets["Estoque"]

        for col in ["D", "E", "F"]:
            for cell in ws[col][1:]:
                if col == "D":
                    cell.number_format = "#,##0"
                else:
                    cell.number_format = "R$ #,##0.00"

    return output.getvalue()


# ------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------

def main():
    st.set_page_config(layout="wide")

    # Header
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        st.title("📦 Posição de Estoque")

    with col2:
        if LOGO_PATH.exists():
            st.image(LOGO_PATH, width=180)

    last_update = get_last_update(DATA_FILE)

    # Load data
    df = load_data()

    # Sidebar filtros
    st.sidebar.header("Filtros")

    segmentos = st.sidebar.multiselect(
        "Segmento", df["Segmento"].unique()
    )
    depositos = st.sidebar.multiselect(
        "Depósito", df["Depósito"].unique()
    )
    meses = st.sidebar.multiselect(
        "Mês", df["Mês"].unique()
    )

    st.sidebar.info(f"Atualizado em: {last_update}")

    # Apply filters
    df_filtered = apply_filters(df, segmentos, depositos, meses)

    # Calculate stock
    df_final = calculate_stock(df_filtered)

    # Metrics
    total_qtd = df_final["Saldo"].sum() if not df_final.empty else 0
    total_valor = (
        (df_final["Saldo"] * df_final["Custos"]).sum()
        if not df_final.empty else 0
    )

    col1, col2 = st.columns(2)

    col1.metric("🔢 Quantidade Total",
                format_decimal(total_qtd, locale="pt_BR"))

    col2.metric("💰 Valor Total (R$)",
                format_currency(total_valor, "BRL", locale="pt_BR"))

    st.divider()

    # Tabela
    st.subheader("📋 Saldo Atual")

    search = st.text_input("Buscar item...")

    if not df_final.empty:
        tabela = df_final.copy()
        tabela["Valor Total (R$)"] = tabela["Saldo"] * tabela["Custos"]

        if search:
            mask = (
                tabela["Item"].str.lower().str.contains(search.lower(), na=False) |
                tabela["Descrição"].str.lower().str.contains(search.lower(), na=False)
            )
            tabela = tabela[mask]

        st.dataframe(
            tabela.style.format({
                "Saldo": format_qtd,
                "Custos": format_brl,
                "Valor Total (R$)": format_brl
            }),
            use_container_width=True
        )

        # Download
        excel_data = export_to_excel(tabela)

        st.download_button(
            "📥 Exportar Excel",
            excel_data,
            "posicao_estoque.xlsx"
        )

    else:
        st.warning("Nenhum dado encontrado.")


# ------------------------------------------------------------------------------
# EXECUÇÃO
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()