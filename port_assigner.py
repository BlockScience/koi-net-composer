import os
from pathlib import Path
import subprocess
import importlib
import sys
import inspect
from koi_net.config import Config


_, module_name, port, *args = sys.argv
sys.path.insert(0, os.getcwd())

node_config_module = importlib.import_module(f"{module_name}.config")

config_class = None

for name, obj in inspect.getmembers(node_config_module):
    if obj is Config: continue
    if inspect.isclass(obj) and issubclass(obj, Config):
        config_class = obj
        break

if not config_class:
    print("failed to find config class")
    
config = config_class.load_from_yaml("config.yaml")

config.server.port = int(port)
config.save_to_yaml()