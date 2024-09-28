import torch
import lightning as pl 
import hydra 
from hydra.core.hydra_config import HydraConfig
from omegaconf import OmegaConf,DictConfig



class Optimizer:
    algo: str 
    lr: float 
    def __init__(self,algo:str,lr:float) -> None:
        self.algo = algo 
        self.lr   = lr 
    def __str__(self) -> str:
        return f"Optimizer(algo={self.algo},lr={self.lr})"


class Trainer:
    def __init__(self, optimizer: Optimizer) -> None:
        self.optimizer = optimizer

    def __repr__(self) -> str:
        return f"Trainer(\n  optimizer={self.optimizer},\n )"


@hydra.main(version_base=None, config_name="config",config_path=".")
def main(cfg:DictConfig)->None:
    print(HydraConfig.get().job.name)
    print(HydraConfig.get().runtime.version)
    print(HydraConfig.get().runtime.cwd) #${hydra:runtime.cwd}
    print(OmegaConf.to_yaml(cfg))

    optim = hydra.utils.instantiate(cfg.trainer.optimizer)
    print(f"optim::{optim} and type:: {type(optim)}")

    # init trainer
    trainners = hydra.utils.instantiate(cfg.trainer)
    print(f"trainer::{trainners} and type:: {type(trainners)}")


    # override optimizers
    trainners = hydra.utils.instantiate(cfg.trainer,optimizer={'algo':'ADAM','lr':1e-5})
    print(f"trainer::{trainners} and type:: {type(trainners)}")

if __name__=='__main__':
    main()
