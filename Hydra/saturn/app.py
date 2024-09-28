from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path="conf", config_name="configs")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    print(cfg.db.variable)           # {hydra:runtime.cwd} shows path where  it's called

if __name__ == "__main__":
    my_app()
