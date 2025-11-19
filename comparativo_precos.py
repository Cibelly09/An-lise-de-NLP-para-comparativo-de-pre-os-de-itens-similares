#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comparativo_precos.py
Versão: 1.0
Autor: Cibelly Viegas

Objetivo:
    Automatizar a comparação de preços entre Smartex e Infomartec,
    usando fuzzy matching para localizar itens similares e gerar um
    relatório final consolidado em Excel.
"""

import os
import sys
import glob
import pandas as pd
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz
from tqdm import tqdm

# ===================== CONFIGURAÇÕES ======================

PASTA_SMARKET = r"K:\Pricing\Indicadores de Promoção\Dados\Infomartec\Encartes Smartex"
PASTA_INFOMARKET = r"K:\Pricing\Indicadores de Promoção\Dados\Infomartec\Base2infomarket"
PASTA_OUTPUT = r"K:\Pricing\Indicadores de Promoção\Dados\Infomartec\Automatizacao\COMPARATIVO"

PERIODO_DIAS = 35
LIMITE_SIMILARIDADE = 60
N_CONCORRENTES = 2

CSV_ENCODING = "utf-8"

# ===========================================================


def extrair_data_arquivo(nome_arquivo):
    import re
    match = re.search(r"(\d{4}_\d{2}_\d{2})", nome_arquivo)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y_%m_%d")
        except:
            return None
    return None


def obter_arquivos_validos(pasta, periodo_dias=PERIODO_DIAS):
    arquivos = []
    hoje = datetime.today()
    limite = hoje - timedelta(days=periodo_dias)

    for f in os.listdir(pasta):
        if not f.lower().endswith(".csv"):
            continue

        caminho = os.path.join(pasta, f)
        data_nome = extrair_data_arquivo(f)

        if data_nome:
            if limite <= data_nome <= hoje:
                arquivos.append(caminho)
        else:
            mtime = datetime.fromtimestamp(os.path.getmtime(caminho))
            if limite <= mtime <= hoje:
                arquivos.append(caminho)

    return arquivos


def ler_e_concatenar(lista):
    dfs = []
    for arq in lista:
        try:
            df = pd.read_csv(arq, encoding=CSV_ENCODING)
            dfs.append(df)
        except:
            pass

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()


def padronizar(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def preparar_base(df, coluna_produto=None):
    if coluna_produto and coluna_produto in df.columns:
        df["produto"] = df[coluna_produto].astype(str).str.upper()
    else:
        txt = df.select_dtypes(include=["object"]).columns
        df["produto"] = df[txt[0]].astype(str).str.upper()
    return df


def encontrar_concorrentes(produto, base_inf):
    escolhas = base_inf["produto"].dropna().unique().tolist()

    matches = process.extract(
        produto,
        escolhas,
        scorer=fuzz.token_sort_ratio,
        limit=30
    )

    resultado = []
    for desc, score, _ in matches:
        if score >= LIMITE_SIMILARIDADE:
            linha = base_inf[base_inf["produto"] == desc].iloc[0]
            resultado.append({
                "produto_concorrente": desc,
                "preco_concorrente": linha.get("price"),
                "rede": linha.get("network"),
                "similaridade": score
            })

        if len(resultado) >= N_CONCORRENTES:
            break

    return resultado


def gerar_relatorio(smartex, infomartec):
    linhas = []

    for _, row in tqdm(smartex.iterrows(), total=len(smartex), desc="Comparando"):
        produto = row["produto"]
        preco_smartex = row.get("price", None)

        concorrentes = encontrar_concorrentes(produto, infomartec)

        if concorrentes:
            for c in concorrentes:
                diferenca = None
                if preco_smartex and c["preco_concorrente"]:
                    diferenca = preco_smartex - c["preco_concorrente"]

                linhas.append({
                    "produto_smartex": produto,
                    "preco_smartex": preco_smarket,
                    "produto_concorrente": c["produto_concorrente"],
                    "preco_concorrente": c["preco_concorrente"],
                    "rede": c["rede"],
                    "similaridade": c["similaridade"],
                    "diferenca_preco": diferenca
                })
        else:
            linhas.append({
                "produto_smartex": produto,
                "preco_smartex": preco_smartex,
                "produto_concorrente": None,
                "preco_concorrente": None,
                "rede": None,
                "similaridade": None,
                "diferenca_preco": None
            })

    return pd.DataFrame(linhas)


def salvar_excel(df):
    os.makedirs(PASTA_OUTPUT, exist_ok=True)
    nome = "comparativo_precos_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"
    path = os.path.join(PASTA_OUTPUT, nome)
    df.to_excel(path, index=False)
    return path


def main():
    print("📥 Carregando arquivos...")

    arquivos_smartex= obter_arquivos_validos(PASTA_SMARTEX)
    arquivos_infomartec = obter_arquivos_validos(PASTA_INFOMARTEC)

    df_smartex = ler_e_concatenar(arquivos_smartex)
    df_inf = ler_e_concatenar(arquivos_infomartec)

    df_smartex = padronizar(df_smartex)
    df_inf = padronizar(df_inf)

    df_smartex = preparar_base(df_smartex)
    df_inf = preparar_base(df_inf)

    print("🔍 Realizando matching fuzzy...")
    relatorio = gerar_relatorio(df_smartex, df_inf)

    print("💾 Salvando relatório...")
    caminho = salvar_excel(relatorio)

    print(f"✅ Processo concluído!\nArquivo gerado: {caminho}")


if __name__ == "__main__":
    main()
