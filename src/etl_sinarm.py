#%%
#Importando bibliotecas
import pandas as pd 
import os


#%%
# Extract - Função para leitura de arquivos

def read_file(file_name: str):
    try:
        df = (
            pd.read_csv(
                f"../data/raw/data-sinarm/{file_name}.csv",
                sep=None,
                engine="python",
                encoding="latin1"
            )
            [["ANO_EMISSAO", "TOTAL"]]
        )
        return df
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {file_name}.csv")
        raise
    except pd.errors.ParserError:
        print(f"[ERRO] Falha ao parsear o arquivo: {file_name}.csv")
        raise


#%%
# Função principal do ETL SINARM

def run_sinarm_etl():

    print("Iniciando ETL SINARM...")

    # Leitura automática dos arquivos da pasta
    file_names = os.listdir("../data/raw/data-sinarm")
    dfs = []

    for i in file_names:
        file_name = i.split(".")[0]
        try:
            dfs.append(read_file(file_name))
        except Exception as e:
            print(f"[AVISO] Pulando {file_name}: {e}")
            continue

    # Concatena todos os datasets
    df_full = pd.concat(dfs, axis=0)

    # Padronização de tipos
    df_full["ANO_EMISSAO"] = df_full["ANO_EMISSAO"].astype(int)
    df_full["TOTAL"] = df_full["TOTAL"].astype(float)

    # Agrupa registros por ano e ordena cronologicamente
    df_full = (
        df_full
        .groupby("ANO_EMISSAO")["TOTAL"]
        .sum()
        .reset_index()
        .sort_values("ANO_EMISSAO")
    )

    # Renomeia colunas para padronização semelhante ao IPEA
    df_full = df_full.rename(
        columns={
            "ANO_EMISSAO": "periodo",
            "TOTAL": "registros_armas"
        }
    )

    # Filtra anos a partir de 2000
    df_full = df_full[df_full["periodo"] >= 2000]

    # Cria métricas derivadas com tratamento de NaN

    # Crescimento anual de registros
    df_full["crescimento_registros"] = (
        df_full["registros_armas"].pct_change().round(4)
    )

    # Média móvel de 3 anos
    df_full["media_movel_3anos"] = (
        df_full["registros_armas"].rolling(3).mean().round(4)
    )

    # Preenche NaN que podem ter surgido das métricas derivadas
    df_full = df_full.fillna(0)

    # Validação simples
    print("Colunas após normalização:", df_full.columns.tolist())
    print(df_full.describe())

    # Load - salvando dataset final
    output_path = "../data/processed/sinarm_tratado.csv"

    try:
        df_full.to_csv(output_path, index=False)
        print("ETL SINARM finalizado!")
        print(f"Arquivo salvo em: {output_path}")
    except OSError as e:
        print(f"[ERRO] Não foi possível salvar o arquivo: {e}")
        raise

    return df_full


#%%
if __name__ == "__main__":
    run_sinarm_etl()