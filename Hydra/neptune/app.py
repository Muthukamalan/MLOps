import hydra
from omegaconf import DictConfig, OmegaConf


'''
config_path:: folder path where your configs are present
config_name:: name of yaml file
'''

@hydra.main(version_base=None,config_path="conf",config_name="config.yaml")  
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    print(f"firewall on web:: {cfg.web.firewall}")
    
    
    # print(cfg.web.waldo)  missing value

if __name__ == "__main__":
    my_app()


'''
python app.py 

python app.py web=angular db=postgresql

python app.py web=node ++web.waldo=10000000

python app.py -m web=node,angular db=mysql,postgresql  ## web.waldo assign before call

python app.py -m web=node,angular db=mysql,postgresql web.waldo=1000000000000000000
'''