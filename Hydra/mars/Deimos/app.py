from typing import Tuple
import os
import hydra
from omegaconf import DictConfig,OmegaConf
import logging
log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path="config", config_name="sphere")
def save_planet(cfg: DictConfig) -> Tuple[float, float]:
    print(OmegaConf.to_yaml(cfg=cfg))
    x: float = cfg.x
    y: float = cfg.y
    log.info(f"Process ID {os.getpid()} executing task {cfg.task} ... with x::{cfg.x}, y::{cfg.y}")
    v0 = 4 * x**2 + 4 * y**2
    v1 = (x - 5) ** 2 + (y - 5) ** 2
    return v0, v1


if __name__ == "__main__":
    save_planet()