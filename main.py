import os
import json
import pathlib
import shutil
from datetime import datetime
from tqdm import tqdm

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

    if not dest.exists():
        if src.is_file():
            file_size = src.stat().st_size
            chunk_size = 10
            
            with open(str(src), 'rb') as src_file, open(str(dest), 'wb') as dest_file:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Copying {name}") as pbar:
                    while chunk := src_file.read(chunk_size):
                        dest_file.write(chunk)
                        pbar.update(len(chunk))

        elif src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest, dirs_exist_ok=True)
            print(f"Backed up {name} directory to {dest}")

        else:
            print(f"Skipped {name}: file not found")

    else:
        m_time_src = datetime.fromtimestamp(src.stat().st_mtime)
        m_time_dest = datetime.fromtimestamp(dest.stat().st_mtime)

        if m_time_src != m_time_dest:
            if src.is_file():
                shutil.copy(src, dest)
                print(f"Overwriting {name} to {dest}")

            elif src.is_dir():
                for item in src.iterdir():
                    target = dest / item.name
                    
                    if item.is_file():
                        if not target.exists() or item.stat().st_mtime > target.stat().st_mtime:
                            shutil.copy2(item, target)
                    elif item.is_dir():
                        shutil.copytree(item, target, dirs_exist_ok=True)
                
                print(f"Synced {name} directory to {dest}")


