import os
import json
import pathlib
import shutil

print("Welcome to pydots!")
def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

config = load_config()

BACKUP_PATH = pathlib.Path(config["backup_dir"]).expanduser()
BACKUP_PATH.mkdir(parents=True, exist_ok=True)

for name, path in config["dotfiles"].items():
    src = pathlib.Path(path).expanduser()
    dest = BACKUP_PATH / src.name

    if src.is_file():
        shutil.copy(src, dest)
        print(f"Backed up {name} to {dest}")
        
    elif src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(f"Backed up {name} directory to {dest}")

    else:
        print(f"Skipped {name}: file not found")
