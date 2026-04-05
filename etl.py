"""
ETL - Processamento de dados de estoque

Autor: Fredson Cabral
Descrição:
Pipeline ETL para tratamento, transformação e enriquecimento de dados
de movimentação de estoque a partir de planilhas Excel.
"""

from pathlib import Path
import logging
from typing import Dict, List

import pandas as pd


# ------------------------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------------------------

INPUT_FILE = Path("data/estoque.xlsx")
OUTPUT_FILE = Path("data/planilha_final_atualizada.xlsx")
FINAL_OUTPUT_FILE = Path("data/estoque_mg.xlsx")

COLUNA_REFERENCIA = "Documento"
COLUNA_DATA = "Data"
COLUNA_DEPOSITO = "Depósito"

REGRAS_MAPEAMENTO: Dict[str, str] = {
    "NS": "Saída",
    "TF": "Transferência",
    "DS": "Devolução Saída",
    "NE": "Entrada",
    "DE": "Devolução Entrada",
    "PD": "Recebimento",
    "Saldo inicial": "Saldo Inicial",
}

VALORES_VALIDOS_DEPOSITO = [202, 216, 219]

COLUNAS_RENAME = {
    "Qtd.acumulada": "Saldo"
}

COLUNAS_REMOVER: List[str] = [
    "Data do sistema",
    "Valor trans.",
    "Valor acumulado",
    "Modelo da nota fiscal",
    "Número da nota fiscal",
    "Série da nota fiscal",
    "Subsérie da nota fiscal",
    "Código NCM",
    "CFOP",
    "Data do documento",
]


# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ------------------------------------------------------------------------------
# FUNÇÕES DE TRANSFORMAÇÃO
# ------------------------------------------------------------------------------

def load_data(file_path: Path) -> pd.DataFrame:
    logging.info(f"Carregando arquivo: {file_path}")
    return pd.read_excel(file_path, dtype={COLUNA_REFERENCIA: str})


def preprocess_dates(df: pd.DataFrame) -> pd.DataFrame:
    if COLUNA_DATA in df.columns:
        df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], errors="coerce")
    return df


def forward_fill_columns(df: pd.DataFrame, num_cols: int = 3) -> pd.DataFrame:
    logging.info("Aplicando forward fill nas colunas iniciais")
    cols = df.columns[:num_cols]
    df[cols] = df[cols].ffill()
    return df


def map_tipo_movimentacao(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Mapeando tipo de movimentação")

    df["Tipo Movimentação"] = None

    for chave, valor in REGRAS_MAPEAMENTO.items():
        mask = df[COLUNA_REFERENCIA].str.contains(chave, na=False)
        df.loc[mask, "Tipo Movimentação"] = valor

    return df


def process_saldo_inicial(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Processando saldo inicial")

    for i in range(len(df) - 1):
        if df.at[i, COLUNA_REFERENCIA] == "Saldo inicial":
            df.at[i, "Quantidade"] = df.at[i, "Qtd.acumulada"]

            for col in ["Data", "Custos"]:
                if col in df.columns:
                    df.at[i, col] = df.at[i + 1, col]

    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Criando coluna de mês")

    mapa_meses = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    df["Mês"] = df[COLUNA_DATA].dt.month.map(mapa_meses)
    return df


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Aplicando filtros")

    df = df.dropna(subset=[COLUNA_REFERENCIA])
    df = df[df[COLUNA_DEPOSITO].isin(VALORES_VALIDOS_DEPOSITO)]

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Renomeando colunas")
    return df.rename(columns=COLUNAS_RENAME)


def save_data(df: pd.DataFrame, path: Path):
    logging.info(f"Salvando arquivo: {path}")
    df.to_excel(path, index=False)


# ------------------------------------------------------------------------------
# PIPELINE PRINCIPAL
# ------------------------------------------------------------------------------

def run_etl():
    df = load_data(INPUT_FILE)

    df = (
        df
        .pipe(preprocess_dates)
        .pipe(forward_fill_columns)
        .pipe(map_tipo_movimentacao)
        .pipe(process_saldo_inicial)
        .pipe(create_month_column)
        .pipe(filter_data)
        .pipe(rename_columns)
    )

    save_data(df, OUTPUT_FILE)

    return df


def merge_data():
    logging.info("Executando merge com base de segmentos")

    df1 = pd.read_excel(OUTPUT_FILE)
    df2 = pd.read_excel(INPUT_FILE, sheet_name="segmento")

    df = pd.merge(df1, df2, on="Item", how="left")
    df = df.drop(columns=COLUNAS_REMOVER, errors="ignore")

    save_data(df, FINAL_OUTPUT_FILE)


# ------------------------------------------------------------------------------
# EXECUÇÃO
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        run_etl()
        merge_data()
        logging.info("✅ Pipeline executado com sucesso!")

    except Exception as e:
        logging.exception(f"Erro no pipeline: {e}")