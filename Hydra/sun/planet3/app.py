from typing import List 
import hydra
from omegaconf import DictConfig,OmegaConf





class Driver:
    def __init__(self,name:str , age:int ) -> None:
        self.name = name 
        self.age  = age 
    def __repr__(self) -> str:
        return f"driver=({self.name}, {self.age})"

class Wheel:
    def __init__(self,r:int, w:int) -> None:
        self.r = r 
        self.w = w 
    def __repr__(self) -> str:
        return f"wheel=({self.r}, and {self.w})"

class Car:
    def __init__(self,driver:Driver, wheel:List[Wheel]) -> None:
        self.driver = driver 
        self.wheel  = wheel
    def __repr__(self) -> str:
        return f"wheel=({self.driver.name}, and wheels:{len(self.wheel)})"


@hydra.main(version_base=None,config_name='config',config_path='.')
def main(cfg:DictConfig):
    print(OmegaConf.to_yaml(cfg))
    car = hydra.utils.instantiate(cfg.car)
    print(car)

    mrf = hydra.utils.instantiate(cfg.car.wheel)
    print(mrf)

if __name__=='__main__':
    main()