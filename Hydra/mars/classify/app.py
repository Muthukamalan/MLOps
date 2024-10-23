from typing import Tuple
import os
import hydra
from omegaconf import DictConfig,OmegaConf
import logging
import random
log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path="conf", config_name="mamba")
def classify_it(cfg: DictConfig) -> Tuple[float, float]:
    print(OmegaConf.to_yaml(cfg=cfg))
    log.info(f"config= {cfg=}")
    return random.random()


if __name__=="__main__":
    classify_it()