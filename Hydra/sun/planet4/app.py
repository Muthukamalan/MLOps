from typing import Any 
from omegaconf import DictConfig,OmegaConf
import hydra


class Optimizer:
    algo:str 
    lr:float
    def __init__(self,algo:str , lr:float) -> None:
        self.algo = algo 
        self.lr = lr 
    def __repr__(self) -> str:
        return f"optimizer=({self.algo}, {self.lr})"
    

class Model:
    def __init__(self,optimizers:Any) -> None:
        self.optimizers = optimizers(lr=0.1)
    def __repr__(self) -> str:
        return f"Model: optimizer=({self.optimizers})"
    
@hydra.main(version_base=None, config_name="config",config_path='.')
def main(cfg:DictConfig)->None:
    print(OmegaConf.to_yaml(cfg))
    model = hydra.utils.instantiate(cfg.model)
    print(model)

if __name__=='__main__':
    main()