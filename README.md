<div align="center">

# 🤖✨ Automação — Comparativo de Preços (Smarket × Infomarket)  
Prova de conceito de automação para comparação de preços entre encartes (fuzzy matching e geração de relatório).

</div>

---

<div align="center">

## 🎯 Objetivo Geral

Demonstrar um processo automatizado que lê bases de preços de duas fontes (Smarket e Infomarket), realiza padronização e fuzzy matching para identificar itens similares, e gera um relatório consolidado com preços concorrentes e diferenças, pronto para análises ou integração em pipelines.

</div>

---

<div align="center">

# 1️⃣ Limpeza e Preparação dos Dados

## 🧹 Objetivo  
Garantir que os arquivos importados fiquem padronizados e prontos para comparação automática entre bases.

<br>

## 📌 Etapas Realizadas  
Leitura automática dos CSVs nas pastas definidas (últimos N dias)  
Padronização de nomes de coluna e formatos  
Criação da coluna 'PRODUTO' padronizada em MAIÚSCULAS  
Remoção de nulos nas colunas chave quando aplicável  

<br>

## 📈 Resultado  
Bases Smarket e Infomarket consolidadas, com colunas essenciais e pronta para executar o processo de matching e gerar relatórios analíticos.

</div>

---

<div align="center">

# 2️⃣ Análises e Visualizações

## 📊 Tipos de Saídas Geradas  
Planilha Excel com o comparativo final contendo:  
Produto Smarket — Preço Smarket — Produto Concorrente — Preço Concorrente — Rede/Encarte — Score Similaridade — Diferença de Preço — Economia (%)

<br>

## 📝 Breve Descrição  
O script realiza fuzzy matching (token_sort_ratio) para encontrar descrições similares entre as bases. Em seguida, calcula diferença de preço e percentual de economia para cada par identificado. Saída em Excel para fácil compartilhamento e análise.

</div>

---

<div align="center">

# 3️⃣ Principais Processos do Código

Leitura automática dos arquivos recentes nas pastas configuradas  
Concatenação e padronização das bases  
Criação de coluna 'produto' em formato consistente  
Fuzzy matching com cutoff configurável (RapidFuzz)  
Cálculo de diferença de preço e economia percentual  
Exportação do resultado final em Excel

</div>

---

<div align="center">

# 4️⃣ Tecnologias Utilizadas

Python  
Pandas  
RapidFuzz  
Tqdm  
Openpyxl

</div>

---

<div align="center">

# ✍️ Autoria  
Cibelly Viegas — 2025

</div>
