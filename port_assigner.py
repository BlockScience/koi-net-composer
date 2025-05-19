import json
import os
from pathlib import Path
import subprocess
import importlib
import sys
import inspect
from koi_net.config import NodeConfig

coordinator_port = 8080

_, module_name, port, *args = sys.argv
sys.path.insert(0, os.getcwd())

node_config_module = importlib.import_module(f"{module_name}.config")

config_class = None

for name, obj in inspect.getmembers(node_config_module):
    if obj is NodeConfig: continue
    if inspect.isclass(obj) and issubclass(obj, NodeConfig):
        config_class = obj
        break

if not config_class:
    print("failed to find config class")
    
config = config_class.load_from_yaml("config.yaml")

if "coordinator" in config.koi_net.node_name:
    config.server.port = coordinator_port
    config.save_to_yaml()
    
    coordinator_url = config.koi_net.node_profile.base_url
    
    with open("../coordinator.json", "w") as f:
        json.dump({"url": coordinator_url}, f)
    
else:
    config.server.port = int(port)
    config.koi_net.node_profile.base_url = None
    
    try:
        with open("../coordinator.json", "r") as f:
            coordinator = json.load(f)
            coordinator_url = coordinator["url"]
            config.koi_net.first_contact = coordinator_url
    except FileNotFoundError:
        print("couldn't find coordinator's URL")
        pass
    
    config.save_to_yaml()