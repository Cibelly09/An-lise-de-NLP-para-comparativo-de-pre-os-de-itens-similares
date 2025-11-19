<div align="center">

# 🤖✨ Automação — Comparativo de Preços entre Fontes de Dados  
Prova de conceito de automação para comparação de preços entre duas bases distintas utilizando fuzzy matching e geração de relatório consolidado.

</div>

---

<div align="center">

## 🎯 Objetivo Geral

Demonstrar um processo automatizado capaz de ler bases de preços de duas fontes diferentes, realizar padronização e aplicar técnicas de fuzzy matching para identificar itens similares, gerando um relatório final com comparações de preços e métricas analíticas.

</div>

---

<div align="center">

# 1️⃣ Limpeza e Preparação dos Dados

## 🧹 Objetivo  
Garantir que os arquivos importados sejam padronizados e estruturados corretamente para permitir a comparação automática entre as bases.

<br>

## 📌 Etapas Realizadas  
Leitura automática dos arquivos CSV localizados nas pastas definidas  
Padronização dos nomes das colunas e tipos de dados  
Criação da coluna padronizada **PRODUTO**  
Tratamento de valores ausentes e inconsistências  

<br>

## 📈 Resultado  
Bases consolidadas, padronizadas e prontas para execução do processo de matching e geração de relatórios comparativos.

</div>

---

<div align="center">

# 2️⃣ Análises e Visualizações

## 📊 Tipos de Saídas Geradas  
Arquivo Excel contendo o comparativo final com:  
Produto Base A — Preço A — Produto Base B (match) — Preço B — Similaridade — Diferença de Preço — Economia (%)

<br>

## 📝 Breve Descrição  
O script utiliza fuzzy matching para localizar produtos equivalentes entre as bases.  
Em seguida, compara preços e calcula indicadores de diferença e economia, resultando em um relatório de fácil análise e integração com outras ferramentas.

</div>

---

<div align="center">

# 3️⃣ Principais Processos do Código

Leitura automatizada dos arquivos mais recentes  
Padronização e concatenação das bases  
Criação da coluna padronizada de descrição  
Aplicação de fuzzy matching configurável  
Cálculo de diferença de preços e economia percentual  
Exportação do relatório consolidado em Excel  

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
