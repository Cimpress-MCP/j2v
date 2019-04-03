import yaml
import os

script_dir = os.path.dirname(__file__)
config_file_path = os.path.join(script_dir, "config.yml")
with open(config_file_path, 'r') as config_file:
    cfg = yaml.load(config_file, Loader=yaml.FullLoader)

generator_config = cfg['program']['generator']
