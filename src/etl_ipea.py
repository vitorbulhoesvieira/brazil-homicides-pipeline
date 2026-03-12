#%%
#Importando bibliotecas
import pandas as pd 
import os
import numpy as np


#%%
# Extract - Função para ler arquivo csv
def read_file(file_name:str):
    try:                                                            
        df = (pd.read_csv(f"../data/raw/data-ipea/{file_name}.csv", sep=";")
            .rename(columns={"valor":file_name})
            .drop(["cod"], axis=1)
            .set_index(["nome", "período"]))
        return df
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {file_name}.csv")
        raise
    except pd.errors.ParserError:
        print(f"[ERRO] Falha ao parsear o arquivo: {file_name}.csv")
        raise

#%%
#Função para normalizar colunas 

def normalize_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace('período', 'periodo')
        .str.replace('-', '_', regex=True)
        .str.replace(r'_+', '_', regex=True)
        .str.strip('_')
    )

    return df

#Função principal para rodar o ETL

def run_ipea_etl():

    # Laço de repetição para ler arquivos
    file_names = os.listdir("../data/raw/data-ipea/")
    dfs = []

    for i in file_names:
        file_name = i.split(".")[0]
        try:                                                       
            dfs.append(read_file(file_name))
        except Exception as e:
            print(f"[AVISO] Pulando {file_name}: {e}")
            continue

    # Concatena com nome original (com acento)
    df_full = (pd.concat(dfs, axis=1)
               .reset_index()
               .sort_values(["período", "nome"]))  
    

    # Normaliza TODAS as colunas (incluindo alterar "período" para "periodo")

    df_full = normalize_columns(df_full)
    
    # AGORA podemos usar "periodo" com segurança
    print("Colunas após normalização:", df_full.columns.tolist())
    
    # Filtra anos maiores que 2000
    df_full = df_full[df_full["periodo"] >= 2000]

    # Converte colunas float para int
    # Identifica colunas de contagem (não percentuais)
    colunas_contagem = [col for col in df_full.columns 
                       if not col.startswith('pct_') 
                       and col not in ['periodo', 'nome']]
    
    for col in colunas_contagem:
        if col in df_full.columns:
            df_full[col] = pd.to_numeric(df_full[col], errors='coerce').fillna(0).astype(int)

    #Cria percentuais com tratamento de divisão por zero

    # Homicídios totais por arma de fogo
    df_full["pct_homicidios_total_por_armas_de_fogo"] = (
        (df_full["homicidios_por_armas_de_fogo"] / 
         df_full["homicidios"].replace(0, np.nan)) * 100
    ).round(4)

    # Mulheres
    df_full["pct_homicidios_mulheres_por_armas_de_fogo"] = (
        (df_full["homicidios_de_mulheres_por_armas_de_fogo"] / 
         df_full["homicidios_por_armas_de_fogo"].replace(0, np.nan)) * 100
    ).round(4)

    # Homens
    df_full["pct_homicidios_homens_por_armas_de_fogo"] = (
        (df_full["homicidios_de_homens_por_armas_de_fogo"] / 
         df_full["homicidios_por_armas_de_fogo"].replace(0, np.nan)) * 100
    ).round(4)

    # Jovens
    df_full["pct_homicidios_jovens_por_armas_de_fogo"] = (
        (df_full["homicidios_de_jovens_por_armas_de_fogo"] / 
         df_full["homicidios_por_armas_de_fogo"].replace(0, np.nan)) * 100
    ).round(4)

    # Preenche NaN que podem ter surgido das divisões por zero
    df_full = df_full.fillna(0)

    # Load - Salvando o dataset final

    output_path = "../data/processed/homicidios_brasil_tratado.csv"

    try:                                                        
        df_full.to_csv(output_path, index=False)
        print("ETL IPEA finalizado!")
        print(f"Arquivo salvo em: {output_path}")
    except OSError as e:
        print(f"[ERRO] Não foi possível salvar o arquivo: {e}")
        raise

    return df_full


#%%
if __name__ == "__main__":
    run_ipea_etl()