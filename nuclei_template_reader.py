import os

files = []
for fpath, _, fnames in os.walk("paths"):
    for f in fnames:
        files.append(f)

paths = []
for file in files:
    with open("paths/" + file) as f:
        raw_file = f.readlines()
    paths.append(raw_file)


if __name__ == "__main__":
    is_reading = True
    while is_reading:
        for idx, file in enumerate(files):
            print(f"[{idx}] - {file} => {len(paths[idx])} files")

        user_choose = input("[Category idx] [File idx] : ")
        try:
            file_idx, yaml_idx = user_choose.split(' ')
            try:
                file_to_open = paths[int(file_idx)][int(yaml_idx)]
                with open(file_to_open.strip()) as f:
                    r = f.read()
                    print(file_to_open)
                    print("=" * 50)
                    print(r)
                    print("="*50)
                    print()
            except:
                print("[x] No Such File or may be OUT OF INDEX")
        except:
            pass
        if user_choose == "q":
            is_reading = False
