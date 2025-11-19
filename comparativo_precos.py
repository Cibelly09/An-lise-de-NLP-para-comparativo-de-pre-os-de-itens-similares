#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comparativo_precos.py  
Versão: 1.0  
Autor: Cibelly Viegas

Objetivo:
    Automatizar o comparativo de preços entre duas fontes distintas de dados,
    aplicando fuzzy matching para identificar produtos similares e gerar
    um relatório consolidado em Excel.

Dependências:
    pip install pandas rapidfuzz openpyxl tqdm
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz
from tqdm import tqdm

# ===================== CONFIGURAÇÕES ======================

# Pastas genéricas para as duas bases
PASTA_BASE_A = r"C:\caminho\para\base_A"
PASTA_BASE_B = r"C:\caminho\para\base_B"
PASTA_OUTPUT = r"C:\caminho\para\saida"

# Parâmetros da automação
PERIODO_DIAS = 35               # arquivos dos últimos N dias
LIMITE_SIMILARIDADE = 60        # cutoff para fuzzy matching
N_CONCORRENTES = 2              # nº de matches retornados
CSV_ENCODING = "utf-8"          # codificação padrão para leitura

# ===========================================================


def extrair_data(nome_arquivo):
    """Extrai datas no formato AAAA_MM_DD se existirem no nome do arquivo."""
    import re
    m = re.search(r"(\d{4}_\d{2}_\d{2})", nome_arquivo)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y_%m_%d")
        except:
            return None
    return None


def listar_arquivos_validos(pasta, dias=PERIODO_DIAS):
    """Retorna arquivos .csv recentes dentro do período especificado."""
    arquivos = []
    hoje = datetime.today()
    limite = hoje - timedelta(days=dias)

    for f in os.listdir(pasta):
        if f.lower().endswith(".csv"):
            caminho = os.path.join(pasta, f)
            data = extrair_data(f)

            if data:
                if limite <= data <= hoje:
                    arquivos.append(caminho)
            else:
                mtime = datetime.fromtimestamp(os.path.getmtime(caminho))
                if limite <= mtime <= hoje:
                    arquivos.append(caminho)

    return arquivos


def carregar_bases(lista_arquivos):
    """Lê e concatena todas as bases de uma lista de arquivos."""
    frames = []
    for arq in lista_arquivos:
        try:
            df = pd.read_csv(arq, encoding=CSV_ENCODING)
            frames.append(df)
        except:
            pass

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def padronizar_colunas(df):
    """Normaliza nomes de colunas."""
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("-", "_")
    )
    return df


def criar_coluna_produto(df):
    """Cria uma coluna padronizada de produto."""
    cols_texto = df.select_dtypes(include=["object"]).columns

    if len(cols_texto) == 0:
        df["produto"] = ""
    else:
        df["produto"] = df[cols_texto[0]].astype(str).str.upper().str.strip()

    return df


def fuzzy_match(produto, base_b):
    """Encontra produtos similares usando fuzzy matching."""
    candidatos = base_b["produto"].dropna().unique().tolist()

    matches = process.extract(
        produto,
        candidatos,
        scorer=fuzz.token_sort_ratio,
        limit=30
    )

    resultados = []

    for desc, score, _ in matches:
        if score >= LIMITE_SIMILARIDADE:
            linha = base_b[base_b["produto"] == desc].iloc[0]

            resultados.append({
                "produto_b": desc,
                "preco_b": linha.get("price"),
                "similaridade": score
            })

        if len(resultados) >= N_CONCORRENTES:
            break

    return resultados


def gerar_relatorio(base_a, base_b):
    """Gera relatório final consolidado."""
    saida = []

    for _, row in tqdm(base_a.iterrows(), total=len(base_a), desc="Comparando"):
        nome_a = row["produto"]
        preco_a = row.get("price")

        similares = fuzzy_match(nome_a, base_b)

        if similares:
            for s in similares:
                diff = None
                if preco_a and s["preco_b"]:
                    diff = preco_a - s["preco_b"]

                saida.append({
                    "produto_base_a": nome_a,
                    "preco_base_a": preco_a,
                    "produto_base_b": s["produto_b"],
                    "preco_base_b": s["preco_b"],
                    "similaridade": s["similaridade"],
                    "diferenca_preco": diff
                })

        else:
            saida.append({
                "produto_base_a": nome_a,
                "preco_base_a": preco_a,
                "produto_base_b": None,
                "preco_base_b": None,
                "similaridade": None,
                "diferenca_preco": None
            })

    return pd.DataFrame(saida)


def salvar_excel(df):
    """Exporta o resultado como Excel."""
    os.makedirs(PASTA_OUTPUT, exist_ok=True)
    nome = "comparativo_precos_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"
    caminho = os.path.join(PASTA_OUTPUT, nome)
    df.to_excel(caminho, index=False)
    return caminho


def main():
    print("📥 Carregando arquivos...")

    arquivos_A = listar_arquivos_validos(PASTA_BASE_A)
    arquivos_B = listar_arquivos_validos(PASTA_BASE_B)

    base_A = carregar_bases(arquivos_A)
    base_B = carregar_bases(arquivos_B)

    base_A = criar_coluna_produto(padronizar_colunas(base_A))
    base_B = criar_coluna_produto(padronizar_colunas(base_B))

    print("🔄 Executando fuzzy matching...")
    relatorio = gerar_relatorio(base_A, base_B)

    print("💾 Salvando arquivo final...")
    caminho = salvar_excel(relatorio)
    print(f"✅ Processo concluído! Arquivo salvo em:\n{caminho}")


if __name__ == "__main__":
    main()
