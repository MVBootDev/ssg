import os, shutil

def distribute(source, dest):
    if not os.path.exists(source):
        print(f"Source directory doesn't exist: {source}")
        return
    if os.listdir(source) == []:
        return
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    _distribute(source, dest)

def _distribute(source, dest):
    tree = os.listdir(source)

    for item in tree:
        item_path = os.path.join(source, item)
        if not os.path.isfile(item_path):
            new_path = os.path.join(dest, item)
            os.mkdir(new_path)
            print(f"Creating directory: {new_path}")
            _distribute(item_path, new_path)
        else:
            shutil.copy(item_path, dest)
            print(f"Copying file: {item_path} -> {dest}")