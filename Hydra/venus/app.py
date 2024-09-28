from omegaconf import OmegaConf,DictConfig
import hydra 
from hydra.core.hydra_config import HydraConfig


@hydra.main(version_base=None, config_name="config",config_path="conf")
def main(cfg:DictConfig)->None:
    print(HydraConfig.get().job.name)
    print(HydraConfig.get().runtime.version)
    print(HydraConfig.get().runtime.cwd) #${hydra:runtime.cwd}
    print(OmegaConf.to_yaml(cfg))

if __name__=='__main__':
    main()


'''
you've different configuration, but experiment needs set of configs  you can't give one-by-one in cmd line.

way to override.

# @package _global_
- override /key: new-val



python app.py -m +experiment=aplite,nglite
python app.py -m '+experiment=glob(*)'          #sweeps
''' 