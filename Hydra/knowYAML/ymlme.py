import yaml
import os 
from omegaconf import OmegaConf
from pprint import pprint

with open(os.path.join( os.path.dirname(__file__),'YAMLme.yml' ), 'r+') as yaml_file:
    file= yaml.safe_load(yaml_file)
    # print(OmegaConf.to_yaml(file))
    pprint(file,indent=2,depth=4,sort_dicts=False,underscore_numbers=False)