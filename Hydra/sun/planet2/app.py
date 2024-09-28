from omegaconf import DictConfig,OmegaConf

import hydra 

class DBConnection:
    def connect(self)->None:
        ... 

class MySQLConnection(DBConnection):
    def __init__(self,host:str,user:str,password:str) -> None:
        self.host = host 
        self.user = user
        self.password = password
    def connect(self) -> None:
        print(f"MySQL connection to {self.host}")



class PostgresSQLConnection(DBConnection):
    def __init__(self,host:str,user:str,password:str) -> None:
        self.host = host 
        self.user = user
        self.password = password
    def connect(self) -> None:
        print(f"PgSQL connection to {self.host}")



@hydra.main(config_name='config',config_path='.',version_base=None)
def main(cfg:DictConfig):
    connection:DBConnection = hydra.utils.instantiate(cfg.db)
    connection.connect()


if __name__=='__main__':
    main()