import os
import yaml
import sys

if len(sys.argv) != 2:
    sys.exit()

search = sys.argv[1]
result = ""
count = 0

template_path = "/home/hope/nuclei-templates"
for fpath, _, fnames in os.walk(template_path):
    for f in fnames:
        _, ext = os.path.splitext(f)
        if ext != ".yaml":
            continue
        file_path = f"{fpath}/{f}"

        with open(file_path) as r:
            raw_file = r.read()
            yaml_file = yaml.load(raw_file, Loader=yaml.Loader)
            if "tags" in yaml_file["info"]:
                tags = yaml_file["info"]["tags"]
                if search in tags:
                    print(file_path)
                    result += file_path + "\n"
                    count += 1
print(f"\n\nTotal Templates of {search} - {count}")
if len(result) != 0:
    with open(search, "w") as f:
        f.write(result)
