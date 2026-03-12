#%%
from etl_ipea import run_ipea_etl
from etl_sinarm import run_sinarm_etl

def main():

    print("Rodando ETL IPEA...")
    run_ipea_etl()

    print("Rodando ETL SINARM...")
    run_sinarm_etl()

    print("Pipeline finalizado.")

if __name__ == "__main__":
    main()
# %%