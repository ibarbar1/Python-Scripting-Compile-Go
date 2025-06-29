import os
import json
import shutil
from subprocess import PIPE, run
import sys


def run_compile_command(command, path):
    cwd= os.getcwd()
    print("before switch working directory:", os.getcwd())
    os.chdir(path)
    print("post switch working directory:", os.getcwd())
    print("running:", command)
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result:", result)
    os.chdir(cwd)

go_file_pointer = ".go"
game_compile_command = ["go","build"]

def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(go_file_pointer):
                code_file_name = file
                break
        break
    if code_file_name is None:
        return
    command = game_compile_command + [code_file_name]
    print("compile command:", command)
    run_compile_command(command, path)

def make_json_metadata(path,game_dirs):
    metadata = {
        "game_names": game_dirs,
        "number_of_games": len(game_dirs)
    }
    
    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)

def copy(source, target):
    shutil.copytree(source, target, dirs_exist_ok=True)
    '''if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(source, target)'''

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def update_pathname(path, value):
    new_names = []
    for dir in path:
        _, dir_name = os.path.split(dir)
        new_dir_name = dir_name.replace(value, "")
        new_names.append(new_dir_name)
    return new_names

game_file_pointer = "game"

def find_all_games_paths(source):
    game_paths = []

    if not os.path.exists(source):
        raise Exception(f"Source path {source} does not exist.")
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if game_file_pointer in directory.lower():
                game_paths.append(os.path.join(source, directory))
        break
    return game_paths

def main(source,target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_games_paths(source_path)
    new_game_paths = update_pathname(game_paths, "_game")

    create_dir(target_path)

    for src, tgt in zip(game_paths, new_game_paths):
        tgt = os.path.join(target_path, tgt)
        copy(src,tgt)
        compile_game_code(tgt)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata(json_path, new_game_paths)

if __name__ == "__main__":
    args = sys.argv
if len(args) != 3:
    raise Exception("You can only make two entries.")
source, target = args[1], args[2]

main(source, target)