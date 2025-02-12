from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import sys
import pytz
from elt.bronze.main import main as run_bronze
from elt.silver.main import main as run_silver
from elt.gold.main import main as run_gold


def run_pipeline():
    print(f"Executando pipeline em {datetime.now(pytz.timezone('America/Sao_Paulo'))}")
    print("==========================================================================")
    print("                       executando a camada bronze                         ")
    print("==========================================================================")
    
    key_permission_bronze = run_bronze()
    if key_permission_bronze == 135:
        print("Execução fora do parazo para inserção dos dados no bonze-storage")
        return 
    
    print("==========================================================================")
    print("                       executando a camada silver                         ")
    print("==========================================================================")
    
    key_permission_silver = run_silver()
    if key_permission_silver == 357:
        print("Não existem novos dados para serem tratados e inseridos na camada silver")
        return 
    
    print("==========================================================================")
    print("                        executando a camada gold                          ")
    print("==========================================================================")
    
    key_permission_gold = run_gold()
    if key_permission_gold == 579:
        print("Não existem novos dados para serem adicionados na camada gold")
        return 
    
    print("==========================================================================")
    print("                          Processo finalizado                             ")
    print("==========================================================================")
    
    

if __name__ == "__main__":
    run_pipeline()
    # brt = pytz.timezone("America/Sao_Paulo")
    # scheduler = BlockingScheduler(timezone=brt)
    
    # run_pipeline()
    # scheduler.add_job(run_pipeline, CronTrigger(day=1, hour=2, minute=0, month="*/2", timezone=brt))
    
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     print("\nInterrompido pelo usuário. Encerrando...")
    #     scheduler.shutdown()
    #     sys.exit(0)
