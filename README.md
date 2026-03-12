# 🔫 Brazil Homicides Pipeline
Pipeline ETL para análise da relação entre registros de armas de fogo e homicídios no Brasil, utilizando dados públicos do **IPEA** e do **SINARM**.
---
## 📌 Sobre o Projeto
Este projeto implementa um pipeline ETL (Extract, Transform, Load) que consolida e trata dados de duas fontes públicas brasileiras:
- **IPEA (Instituto de Pesquisa Econômica Aplicada):** dados de homicídios totais, por arma de fogo, por gênero e por faixa etária (jovens), desagregados por estado e ano.
- **SINARM (Sistema Nacional de Armas):** registros anuais de armas de fogo emitidos no país.
O objetivo é produzir datasets limpos e prontos para análise, possibilitando explorar padrões temporais e correlações entre armamento civil e índices de violência letal no Brasil.
---
## 🗂️ Estrutura do Projeto
```
brazil-homicides-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── data-ipea/          # CSVs brutos do IPEA
│   │   └── data-sinarm/        # CSVs brutos do SINARM
│   └── processed/              # Datasets tratados (saída do pipeline)
│
├── src/
│   ├── etl_ipea.py             # ETL dos dados de homicídios (IPEA)
│   ├── etl_sinarm.py           # ETL dos registros de armas (SINARM)
│   └── run.py                  # Orquestrador do pipeline completo
│
├── notebooks/
│   └── analysis.ipynb          # Análise exploratória dos dados tratados
│
├── assets/                     # Visualizações geradas na análise
├── .gitignore
├── requirements.txt
└── README.md
```
---
## ⚙️ Como Executar
### 1. Clone o repositório
```bash
git clone https://github.com/vitorbulhoesvieira/brazil-homicides-pipeline.git
cd brazil-homicides-pipeline
```
### 2. Instale as dependências
```bash
pip install -r requirements.txt
```
### 3. Adicione os dados brutos
Coloque os arquivos `.csv` do IPEA em `data/raw/data-ipea/` e os do SINARM em `data/raw/data-sinarm/`.
### 4. Execute o pipeline
```bash
python src/run.py
```
Os arquivos tratados serão salvos em `data/processed/`.
---
## 🔄 Detalhes do Pipeline
### `etl_ipea.py`
- Lê múltiplos CSVs da pasta `data-ipea/` de forma dinâmica
- Concatena, normaliza colunas e remove acentos/caracteres especiais
- Filtra registros a partir do ano 2000
- Cria indicadores percentuais derivados:
  - `pct_homicidios_total_por_armas_de_fogo`
  - `pct_homicidios_mulheres_por_armas_de_fogo`
  - `pct_homicidios_homens_por_armas_de_fogo`
  - `pct_homicidios_jovens_por_armas_de_fogo`
- Exporta `homicidios_brasil_tratado.csv`
### `etl_sinarm.py`
- Lê CSVs com detecção automática de separador (`sep=None`)
- Agrega registros por ano via `groupby`
- Cria métricas temporais:
  - `crescimento_registros` — variação percentual anual (pct_change)
  - `media_movel_3anos` — média móvel de 3 anos (rolling mean)
- Exporta `sinarm_tratado.csv`
### `run.py`
- Orquestra a execução sequencial dos dois ETLs
---
## 📊 Dados de Saída
| Arquivo | Descrição |
|---|---|
| `homicidios_brasil_tratado.csv` | Homicídios por UF e ano, com indicadores percentuais por arma de fogo, gênero e faixa etária |
| `sinarm_tratado.csv` | Registros anuais de armas, com crescimento percentual e média móvel |
---
## 📈 Análise Exploratória
Os dados tratados pelo pipeline são explorados no notebook [`analysis.ipynb`](notebooks/analysis.ipynb), que inclui visualizações produzidas com **Matplotlib** e **Seaborn**.

<!-- Adicione abaixo as imagens dos gráficos gerados. Exemplo:
![Evolução dos Homicídios por Arma de Fogo](assets/homicidios_arma_fogo.png)
![Registros SINARM ao Longo do Tempo](assets/registros_sinarm.png)
-->

---
## 🔍 Fontes de Dados
- [IPEA Data](http://www.ipeadata.gov.br/) — Instituto de Pesquisa Econômica Aplicada
- [SINARM](https://www.gov.br/pf/pt-br/assuntos/armas) — Sistema Nacional de Armas / Polícia Federal
---
## 🛠️ Tecnologias
- Python 3.9.25 
- Pandas 2.3.3
- NumPy 2.0.1
- Matplotlib 3.9.2
- Seaborn 0.13.2
## 📄 Licença
Este projeto utiliza dados públicos do governo brasileiro e é disponibilizado para fins educacionais e de pesquisa.
