from pathlib import Path
import os
import subprocess
import sys

node_repos = [
    "BlockScience/koi-net-coordinator-node",
    "BlockScience/koi-net-debug-node",
    "BlockScience/koi-net-hackmd-sensor-node",
    "BlockScience/koi-net-slack-sensor-node"
]

starting_port = 8000

for node_repo in node_repos:
    owner, repo_name = node_repo.split("/", 1)
    if not os.path.isdir(repo_name):
        subprocess.run(["git", "clone", f"https://github.com/{node_repo}"])
    else:
        print(f"{repo_name} already exists")

# for node_repo in node_repos:
    owner, repo_name = node_repo.split("/", 1)
    
    os.chdir(repo_name)
    
    if not os.path.isdir(".venv"):
        print("creating virtual environment")
        subprocess.run(["python", "-m", "venv", ".venv"], check=True)
        print("installing dependencies")
        subprocess.run([".venv\\Scripts\\activate.bat", "&&", "pip", "install", "-r", "requirements.txt"], shell=True)
    
    subdirs = [d for d in Path().iterdir() if d.is_dir()]
    node_module = None
    for subdir in subdirs:
        if "node" in str(subdir):
            node_module = str(subdir)
            print(f"identified node module: {subdir}")
            break
    
    if not node_module:
        print(f"Failed to find node module for repo {node_repo}")
        continue
    
    subprocess.run([".venv\\Scripts\\activate.bat", "&&", "python", "..\\port_assigner.py", node_module, str(starting_port)], shell=True)
    
    starting_port += 1
    
    os.chdir("..")
    
    