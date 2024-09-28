import hydra
from omegaconf import DictConfig, OmegaConf


'''
config_path:: folder path where your configs are present
config_name:: name of yaml file

'''

@hydra.main(version_base=None,config_path="conf",config_name="configs.yaml")  
# @hydra.main(config_name="main.yaml",config_path=".",version_base=None)
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()



'''
python app.py
python app.py +web.driver=chromium         # add k-v

python app.py db.pass=sauce                # if k-v already present pass as it is, else use ++ add/override
python app.py ++db.pass=sauce
'''